/*******************************************************************************
 * @file api_impl.cpp
 * @brief api python 接口
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "api_impl.h"

#include <math.h>
#include <algorithm>

#include "time.h"
#include <boost/iostreams/filter/lzma.hpp>
#include <boost/iostreams/filtering_stream.hpp>
#include <pybind11/embed.h>

#include "utils/common.h"
#include "obj.h"
#include "field_mapping.h"
#include "backtest/backtest_report.h"
#include "account/tq_sim.h"
#include "account/tq_kq.h"
#include "account/tq_account.h"
#include "account/tq_ctp.h"
#include "account/tq_rohon.h"
#include "account/tq_kq_stock.h"

namespace TqSdk2 {

structlog::Logger logger = structlog::Logger::Root();
std::ofstream g_log_file;
boost::iostreams::filtering_ostream g_log_stream;
using namespace boost::property_tree;

TqPythonApi::TqPythonApi(py::object& py_account, py::object& py_auth, py::object& py_backtest, py::object& py_gui,
  py::object& py_log, bool disable_print, const std::string& md_url, int srandom, int64_t mock_date_time)
  : m_md_url(md_url)
  , m_web_helper(nullptr)
  , m_disable_print(disable_print)
  , m_is_backtest(false)
  , m_sub_instruments(std::make_shared<Subscribed>())
  , random(srandom ? srandom : time(nullptr)) {
  py::print(
    "在使用天勤量化之前，默认您已经知晓并同意以下免责条款，如果不同意请立即停止使用：https://www.shinnytech.com/blog/"
    "disclaimer/");

  try {
    if (mock_date_time) {
      MockDateTime(mock_date_time);
    }

    SetupLogger(py_log, structlog::LogLevel::Info);

    SetupAuth(py_auth);

    SetupAccount(py_account);

    SetupBackTest(py_backtest);

    SetupApi();

    SubscribeInstrumentsInfo();

    Login();

    SetupWebGui(py_gui);

    SetupTradingStatus();

    AliasFuncWhenSecurities();

  } catch (std::exception& ex) {
    Close();
    throw std::exception(std::logic_error(ex.what()));
  }
}

void TqPythonApi::Close() {
  if (m_auth) {
    m_auth->Logout();
    m_auth = nullptr;
  }

  if (m_api) {
    m_api->CleanUp();
    m_api = nullptr;
  }

  structlog::SetOutput(nullptr);
  boost::iostreams::close(g_log_stream);
  g_log_file.close();
}

bool TqPythonApi::RunOnce(double timeout) {
  if (!m_is_backtest && (std::fabs(timeout - 0) > 0.000001) && (NowAsEpochNano() / 1e9) >= timeout)
    return false;

  auto result = m_api->RunOnce();

  for (auto& [symbol, tick] : m_tick_serial_map) {
    tick->RunOnce();
  }

  for (auto& [_, kline] : m_kline_serial_map) {
    kline->RunOnce();
  }

  for (auto& strategy : m_market_maker_strategys) {
    strategy->RunOnce();
  }

  for (auto& [key, task] : m_target_pos_task_map) {
    if (task->RunOnce() < 0) {
      throw std::exception(std::logic_error(task->m_status_msg.c_str()));
    }
  }

  if (m_trading_status_worker) {
    m_trading_status_worker->RunOnce();
  }

  if (m_is_backtest) {
    if (BackTestServiceStatus::kStopped == m_options.backtest_service->GetStatus()) {
      for (auto [k, v] : m_accounts) {
        BacktestReport cal(m_api, m_disable_print, v->m_user_key, v->m_init_balance);
        auto report = cal.GetReport();
      }

      Close();
      throw BacktestFinished("回测结束!");
    }

    if (!result && BackTestServiceStatus::kAdvancing == m_options.backtest_service->GetStatus())
      m_options.backtest_service->UpdateDateTime();
  }

  return true;
}

TqPythonApi::~TqPythonApi() {
  this->Close();
}

bool TqPythonApi::IsPythonFieldEqual(const py::object& object, const py::str& field) {
  // 内部对象定义个 _get_{field}() 方法，该方法可以获取field的 snap 和 history 的值
  py::object get_field_value = object.attr("_get_{}"_s.format(field));
  // 浮点型数据需要单独进行判断
  std::string type = get_field_value(true).attr("__class__").attr("__name__").cast<std::string>();
  if (type == "float" || type == "double") {
    return !DoubleEqual(get_field_value(true).cast<double>(), get_field_value(false).cast<double>());
  }
  // 比较字段的 snap 和 history 是否相同
  return !get_field_value(true).is(get_field_value(false));
}

bool TqPythonApi::IsChanging(py::object obj, py::str fields) {
  std::string object_classname = obj.attr("__class__").attr("__name__").cast<std::string>();
  if (object_classname == "DataFrame" || object_classname == "Series") {
    auto object_key = obj.attr("_key").cast<std::string>();

    if (obj.attr("_df_type").cast<std::string>() == "tick") {
      return m_tick_serial_map[object_key]->m_tick_series_node->m_snap_version < m_api->DataRoot()->m_snap_version
        ? false
        : true;
    } else {
      auto field = fields.cast<std::string>();
      return m_kline_serial_map[object_key]->m_is_kline_changed
        || std::get<0>(m_kline_serial_map[object_key]->m_latest_fields[field]);
    }
  } else if (object_classname == "Account") {
    std::string user_key = obj.attr("_user_key").cast<std::string>();
    if (m_accounts.find(user_key) == m_accounts.end()) {
      throw py::key_error("账户对象异常: 账户信息缺失");
    }

    std::string object_key = obj.attr("_key").cast<std::string>();
    if (m_accounts[user_key]->m_account_views[object_key]->GetCommitNodes().size()) {
      return IsPythonFieldEqual(obj, fields);
    }
  } else if (object_classname == "Quote") {
    std::string object_key = obj.attr("_key").cast<std::string>();

    if (m_quotes_view[object_key]->GetCommitNodes().size()) {
      return IsPythonFieldEqual(obj, fields);
    }
  } else if (object_classname == "Order") {
    std::string user_key = obj.attr("_user_key").cast<std::string>();
    if (m_accounts.find(user_key) == m_accounts.end()) {
      throw py::key_error("委托单对象异常, 委托单账户信息缺失.");
    }

    std::string order_id = obj.attr("order_id").cast<std::string>();
    int unit_id = obj.attr("unit_id").cast<int>();
    for (auto& [key, node] : m_accounts[user_key]->m_alive_order_view->GetCommitNodes()) {
      if (node->Latest()->unit_id == unit_id && node->Latest()->order_id == order_id) {
        return IsPythonFieldEqual(obj, fields);
      }
    }
  } else if (object_classname == "Position") {
    std::string user_key = obj.attr("_user_key").cast<std::string>();
    if (m_accounts.find(user_key) == m_accounts.end()) {
      throw py::key_error("持仓对象异常: 账户信息缺失");
    }

    std::string object_key = obj.attr("_key").cast<std::string>();
    if (m_accounts[user_key]->m_positions_views[object_key]->GetCommitNodes().size()) {
      return IsPythonFieldEqual(obj, fields);
    }
  }

  return false;
}

bool TqPythonApi::IsChanging(py::object obj, py::list fields_list) {
  for (auto item : fields_list) {
    if (IsChanging(obj, py::str(item))) {
      return true;
    }
  }
  return false;
}

bool TqPythonApi::IsChanging(py::object obj) {
  std::string object_classname = obj.attr("__class__").attr("__name__").cast<std::string>();

  if (object_classname == "DataFrame" || object_classname == "Series") {
    auto key = obj.attr("_key").cast<std::string>();
    auto df_type = obj.attr("_df_type").cast<std::string>();
    if (df_type == "tick") {
      if (!m_tick_serial_map[key]->m_tick_series_node)
        return false;
      return m_tick_serial_map[key]->m_tick_series_node->m_snap_version < m_api->DataRoot()->m_snap_version ? false
                                                                                                            : true;
    } else {
      // Kline 推进一根或者最后一根任一字段发生变化均返回 true
      auto is_changed = m_kline_serial_map[key]->m_is_kline_changed;
      for (auto [field, changed] : m_kline_serial_map[key]->m_latest_fields) {
        is_changed = is_changed || std::get<0>(changed);
      }
      return is_changed;
    }
  } else if (object_classname == "Quote") {
    std::string object_key = obj.attr("_key").cast<std::string>();
    return m_quotes_view[object_key]->GetCommitNodes().size();
  } else if (object_classname == "Account") {
    std::string user_key = obj.attr("_user_key").cast<std::string>();
    if (m_accounts.find(user_key) == m_accounts.end()) {
      throw py::key_error("账户对象异常: 属性 user_key 缺失或错误");
    }

    std::string object_key = obj.attr("_key").cast<std::string>();
    return m_accounts[user_key]->m_account_views[object_key]->GetCommitNodes().size();
  } else if (object_classname == "Order") {
    auto user_key = obj.attr("_user_key").cast<std::string>();
    if (m_accounts.find(user_key) == m_accounts.end()) {
      throw py::key_error("委托单对象异常, 属性 user_key 缺失或错误");
    }

    int unit_id = obj.attr("unit_id").cast<int>();
    auto order_id = obj.attr("order_id").cast<std::string>();
    for (auto [k, node] : m_accounts[user_key]->m_alive_order_view->GetCommitNodes()) {
      if (node->Latest()->unit_id == unit_id && node->Latest()->order_id == order_id) {
        return true;
      }
    }
    return false;
  } else if (object_classname == "Orders") {
    auto user_key = obj.attr("_user_key").cast<std::string>();
    if (user_key.empty()) {
      return false;
    }

    if (m_accounts.find(user_key) == m_accounts.end()) {
      throw py::key_error("委托单对象异常, 属性 user_key 缺失或错误");
    }

    return m_accounts[user_key]->m_alive_order_view->GetCommitNodes().size();
  } else if (object_classname == "Trades") {
    auto user_key = obj.attr("_user_key").cast<std::string>();
    if (user_key.empty()) {
      return false;
    }

    if (m_accounts.find(user_key) == m_accounts.end()) {
      throw py::key_error("成交对象异常, 属性 user_key 缺失或错误");
    }

    int unit_id = obj.attr("_unit_id").cast<int>();
    auto view_key = user_key + "|" + std::to_string(unit_id);
    return m_accounts[user_key]->m_trades_views[view_key]->GetCommitNodes().size();
  } else if (object_classname == "Position") {
    auto user_key = obj.attr("_user_key").cast<std::string>();
    if (m_accounts.find(user_key) == m_accounts.end()) {
      throw py::key_error("持仓对象异常, 属性 user_key 缺失或错误");
    }

    std::string object_key = obj.attr("_key").cast<std::string>();

    return m_accounts[user_key]->m_positions_views[object_key]->GetCommitNodes().size();
  } else if (object_classname == "Positions") {
    auto user_key = obj.attr("_user_key").cast<std::string>();
    if (user_key.empty()) {
      return false;
    }

    if (m_accounts.find(user_key) == m_accounts.end()) {
      throw py::key_error("持仓对象异常, 属性 user_key 缺失或错误");
    }

    int unit_id = obj.attr("_unit_id").cast<int>();
    auto view_key = user_key + "|" + std::to_string(unit_id);
    return m_accounts[user_key]->m_positions_views[view_key]->GetCommitNodes().size();
  } else {
    throw std::logic_error("当前数据结构暂不支持 ischanging 用法.");
  }
}

std::shared_ptr<InstrumentNode> TqPythonApi::GetQuote(const std::string& symbol) {
  // 合约校验.
  auto node = EnsureInsValid(symbol);

  if (m_quotes_view.find(symbol) != m_quotes_view.end()) {
    return node;
  }

  // 订阅行情
  auto req = std::make_shared<md::SubscribeQuote>();
  req->subscribe_id = std::to_string(random());
  req->symbol_set = m_sub_instruments->SubQuote(symbol).quotes;
  TqSyncRequest(m_api, req);

  // 创建一个视图用于判断该对象的 is_changing .
  m_quotes_view[symbol] = m_api->DataDb()->CreateView<Instrument>([=](std::shared_ptr<const Instrument> q) {
    return q->symbol == symbol;
  });

  // 等待行情数据就绪
  RunUntilReady(m_api, [&]() {
    auto node = m_api->DataDb()->GetNode<Instrument>(symbol);
    return !node->Snap()->exchange_time_str.empty();
  });

  return node;
}

std::vector<std::shared_ptr<md::InstrumentNode>> TqPythonApi::GetQuoteList(
  const std::vector<std::string>& symbol_list) {
  std::vector<std::shared_ptr<md::InstrumentNode>> quote_list;

  for (auto symbol : symbol_list) {
    quote_list.push_back(GetQuote(symbol));
  }

  return quote_list;
}

std::shared_ptr<TickWrapper> TqPythonApi::GetTickSerial(const std::string& symbol, int data_length) {
  EnsureInsValid(symbol);

  if (data_length <= 0) {
    auto msg = "Tick 数据序列长度 " + std::to_string(data_length) + " 错误, 请检查序列长度是否填写正确.";
    throw std::invalid_argument(msg.c_str());
  }

  if (m_tick_serial_map.find(symbol) != m_tick_serial_map.end())
    return m_tick_serial_map[symbol];

  auto tick = std::make_shared<TickWrapper>(data_length);
  m_tick_serial_map[symbol] = tick;

  // 订阅 Tick 数据
  auto req_subscribe_tick = std::make_shared<md::SubscribeChartLatest>();
  req_subscribe_tick->subscribe_id = "tqsdk2_sub_tick_" + TrimSymbol(symbol) + std::to_string(random());
  req_subscribe_tick->dur_nano = 0;
  req_subscribe_tick->symbol_list.push_back(symbol);
  req_subscribe_tick->view_width = data_length;
  SyncRequest(m_api, req_subscribe_tick);
  if (req_subscribe_tick->result_code != 0) {
    logger.Info("req_subscribe_tick failed");
    return m_tick_serial_map[symbol];
  }

  std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
  while (tick->m_last_id == -1) {
    if (std::chrono::steady_clock::now() - start > std::chrono::seconds(60)) {
      auto msg = std::string("获取 ") + symbol + std::string(" 的 Tick 超时, 请检查客户端及网络是否正常.");
      throw std::exception(std::logic_error(msg.c_str()));
    }
    m_api->RunOnce();

    // 回测模式下, 回测状态为 kAdvancing 时, 回测模块才就绪
    if (m_is_backtest && m_options.backtest_service->GetStatus() == md::BackTestServiceStatus::kSubscribed)
      continue;

    auto ticks_root = m_api->DataRoot()->GetChild<ApiTreeKey::kMarketData>()->GetChild<md::MdTreeKey::kTicks>();
    tick->m_tick_series_node = ticks_root->GetChild(symbol);
    tick->RunOnce();
  }

  return m_tick_serial_map[symbol];
}

std::shared_ptr<KlineWrapper> TqPythonApi::GetKlineSerial(const std::string& symbol, int duration, int data_length) {
  EnsureInsValid(symbol);

  if (data_length <= 0)
    throw std::invalid_argument("K 线数据序列长度错误, 请检查参数是否填写正确.");

  if (duration <= 0 || (duration > 86400 && duration % 86400 != 0)) {
    throw std::invalid_argument("K 线数据周期 " + std::to_string(duration) + " 错误, 请检查参数是否填写正确.");
  }

  auto kline_key = symbol + std::to_string(duration);
  if (m_kline_serial_map.find(kline_key) != m_kline_serial_map.end())
    return m_kline_serial_map[kline_key];

  m_kline_serial_map[kline_key] = std::make_shared<KlineWrapper>(duration, data_length);

  auto req_subscribe_kline = std::make_shared<md::SubscribeChartLatest>();
  req_subscribe_kline->subscribe_id = "tqsdk2_sub_kline_" + TrimSymbol(kline_key) + std::to_string(random());
  req_subscribe_kline->dur_nano = duration * 1000000000LL;
  req_subscribe_kline->symbol_list.push_back(symbol);
  req_subscribe_kline->view_width = data_length;
  SyncRequest(m_api, req_subscribe_kline);
  if (req_subscribe_kline->result_code != 0) {
    logger.Info("req_subscribe_kline failed");
    return m_kline_serial_map[kline_key];
  }

  std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
  while (m_kline_serial_map[kline_key]->m_last_id == -1) {
    if (std::chrono::steady_clock::now() - start > std::chrono::seconds(60)) {
      auto msg = "获取 " + symbol + " (" + std::to_string(duration) + ") 的K线超时，请检查客户端及网络是否正常.";
      throw std::exception(std::logic_error(msg.c_str()));
    }

    m_api->RunOnce();
    // 1 - 回测模式下, 回测状态为 kAdvancing 时, 回测模块才就绪
    if (m_is_backtest && m_options.backtest_service->GetStatus() == md::BackTestServiceStatus::kSubscribed)
      continue;

    auto node =
      m_api->DataRoot()->GetChild<ApiTreeKey::kMarketData>()->GetChild<md::MdTreeKey::kKlines>()->GetChild(symbol);
    if (node)
      m_kline_serial_map[kline_key]->m_kline_series_node = node->GetChild(req_subscribe_kline->dur_nano);

    m_kline_serial_map[kline_key]->RunOnce();
  }

  return m_kline_serial_map[kline_key];
}

std::shared_ptr<future::OrderNode> TqPythonApi::InsertOrder(const std::string& symbol, const std::string& direction,
  const std::string& offset, int volume, py::object& py_price, const py::object& py_account, int unit_id) {
  // 获取当前账户实例
  auto account_ptr = GetAccountPtrFromPythonObject(py_account);

  // 当行情信息不存在时, 订阅行情数据
  auto node = EnsureInsValid(symbol);
  if (node->Snap()->exchange_time_str.empty()) {
    GetQuote(symbol);
  }

  // 校验下单数量是否正确
  if (volume <= 0) {
    throw std::invalid_argument("下单数量 " + std::to_string(volume) + " 错误, 请检查 volume 是否填写正确.");
  }
  m_auth->HasTdGrant(symbol, node->Latest()->product_class);

  // 组装下单指令包
  auto user_key = account_ptr->m_user_key;
  auto req = std::make_shared<future::InsertOrder>(user_key);
  req->unit_id = account_ptr->GetCurrentUnitID(unit_id);
  req->direction = g_direction_mapping.GetEnum(direction);
  req->offset = g_offset_mapping.GetEnum(offset);
  req->exchange_id = symbol.substr(0, symbol.find("."));
  req->instrument_id = symbol.substr(symbol.find(".") + 1);
  if (py_price.is_none()) {
    if (AnyOne(req->exchange_id, "CFFEX", "SHFE", "INE", "SSE", "SZSE")) {
      throw std::invalid_argument(symbol + " 不支持市价单, 请使用 limit_price 参数指定价格.");
    }
    req->price_type = future::PriceType::kAny;
    req->time_condition = future::OrderTimeCondition::kIoc;
  } else {
    double price = py_price.cast<double>();
    if (std::isnan(price)) {
      throw std::invalid_argument("合约价格非法, 请检查价格是否填写正确.");
    }
    req->limit_price = price;
    req->price_type = future::PriceType::kLimit;
    req->time_condition = future::OrderTimeCondition::kGfd;
  }
  req->volume = volume;
  req->volume_condition = future::OrderVolumeCondition::kAny;

  return account_ptr->InsertOrder(req, [&](const std::string& msg) {
    Notify(msg);
  });
}

void TqPythonApi::CancelOrder(const py::object& py_order_or_order_id, const py::object& py_account) {
  if (py_order_or_order_id.is_none()) {
    throw std::invalid_argument("撤单失败, 委托或委托单号不能为空.");
  }

  std::string name = py_order_or_order_id.attr("__class__").attr("__name__").cast<std::string>();
  auto order_id = name == "Order" ? py_order_or_order_id.attr("order_id").cast<std::string>()
                                  : py_order_or_order_id.cast<std::string>();

  auto account_ptr = GetAccountPtrFromPythonObject(py_account);

  return account_ptr->CancelOrder(order_id);
}

std::shared_ptr<future::AccountNode> TqPythonApi::GetAccount(const py::object& py_account, int unit_id) {
  auto account_ptr = GetAccountPtrFromPythonObject(py_account);
  return account_ptr->GetAccount(unit_id);
}

std::shared_ptr<future::PositionNode> TqPythonApi::GetPosition(
  const std::string& symbol, const py::object& py_account, int unit_id) {
  auto account_ptr = GetAccountPtrFromPythonObject(py_account);
  return account_ptr->GetPosition(symbol, unit_id);
}

const std::map<std::string, std::shared_ptr<PositionNode>>& TqPythonApi::GetPositions(
  const py::object& py_account, int unit_id) {
  auto account_ptr = GetAccountPtrFromPythonObject(py_account);
  return account_ptr->GetPositions(unit_id);
}

std::shared_ptr<future::OrderNode> TqPythonApi::GetOrder(
  const std::string& order_id, const py::object& py_account, int unit_id) {
  auto account_ptr = GetAccountPtrFromPythonObject(py_account);
  return account_ptr->GetOrder(order_id);
}

const std::map<std::string, std::shared_ptr<future::OrderNode>>& TqPythonApi::GetOrders(
  const py::object& py_account, int unit_id) {
  auto account_ptr = GetAccountPtrFromPythonObject(py_account);
  return account_ptr->GetOrders(unit_id);
}

std::shared_ptr<future::TradeNode> TqPythonApi::GetTrade(
  const std::string& trade_id, const py::object& py_account, int unit_id) {
  auto account_ptr = GetAccountPtrFromPythonObject(py_account);
  return account_ptr->GetTrade(trade_id);
}

const std::map<std::string, std::shared_ptr<future::TradeNode>>& TqPythonApi::GetTrades(
  const py::object& py_account, int unit_id) {
  auto account_ptr = GetAccountPtrFromPythonObject(py_account);
  return account_ptr->GetTrades(unit_id);
}

void TqPythonApi::SetupAuth(const py::object& auth) {
  if (py::isinstance<TqAuth>(auth)) {
    m_auth = std::make_shared<TqAuth>(auth.cast<TqAuth&>());
  } else if (py::isinstance<py::str>(auth)) {
    auto user = py::str(auth).cast<std::string>();
    m_auth = std::make_shared<TqAuth>(user.substr(0, user.find(",")), user.substr(user.find(",") + 1));
  } else {
    throw std::invalid_argument("用户权限认证失败, 请输入正确的信易账户信息.");
  }
}

void TqPythonApi::SetupAccount(const py::object& account) {
  if (py::isinstance<py::list>(account)) {
    for (auto item : account) {
      auto account_ptr = PyObjectToAccount(item.cast<py::object>());
      m_accounts[account_ptr->m_user_key] = account_ptr;
    }
  } else {
    auto account_ptr = PyObjectToAccount(account);
    m_accounts[account_ptr->m_user_key] = account_ptr;
  }
}

std::shared_ptr<TqBaseAccount> TqPythonApi::PyObjectToAccount(const py::object& account) {
  if (account.is_none()) {
    return std::make_shared<TqSim>(kSimInitBalance, "TQSIM");
  } else if (py::isinstance<TqSim>(account)) {
    return std::make_shared<TqSim>(account.cast<TqSim&>());
  } else if (py::isinstance<TqAccount>(account)) {
    return std::make_shared<TqAccount>(account.cast<TqAccount&>());
  } else if (py::isinstance<TqKq>(account)) {
    return std::make_shared<TqKq>(account.cast<TqKq&>());
  } else if (py::isinstance<TqCtp>(account)) {
    return std::make_shared<TqCtp>(account.cast<TqCtp&>());
  } else if (py::isinstance<TqRohon>(account)) {
    return std::make_shared<TqRohon>(account.cast<TqRohon&>());
  } else if (py::isinstance<TqKqStock>(account)) {
    return std::make_shared<TqKqStock>(account.cast<TqKqStock&>());
  } else {
    throw std::invalid_argument("账户类型填写错误, 请检查参数是否输入正确.");
  }
}

void TqPythonApi::SetupLogger(const py::object& log, structlog::LogLevel level) {
  structlog::SetLevel(level);

  auto conf = py::str(log).cast<std::string>();
  if (conf.compare("False") != 0) {
#ifdef _WIN32
    fs::path log_path = fs::current_path() / "tqsdk2" / "logs";
#else
    fs::path log_path = "/tmp/tqsdk2/logs";
#endif
    fs::create_directories(log_path);
    fs::path log_file = log_path / conf;
    if (!conf.compare("True")) {
      log_file = log_path / (NowAsString() + "-" + std::to_string(GetPID()) + ".log");
    }
    g_log_file = std::ofstream(log_file.string(), std::ios_base::out | std::ios::binary);
    g_log_stream.push(g_log_file);
  }
  structlog::SetOutput(&g_log_stream);
}

void TqPythonApi::SetupBackTest(const py::object& backtest) {
  if (!py::isinstance<BackTest>(backtest))
    return;

  for (auto [user_key, account_ptr] : m_accounts) {
    if (account_ptr->m_account_type != TqAccountType::kSim) {
      throw std::invalid_argument("回测时, 账户类型必须为 TqSim.");
    }
  }

  m_is_backtest = true;
  m_options.backtest_service = backtest.cast<BackTest&>().GetService();
}

void TqPythonApi::SetupApi() {
  // 交易单元不支持多账户, 默认使用第一个账户
  m_options.trade_unit_path = m_accounts.begin()->second->m_trading_unit->GetTradeUnitPath();
  m_options.md_url = m_md_url;
  m_options.enable_sync_position_volume = true;
  m_options.access_token = m_auth->GetAccessToken();
  m_options.his_record_mode = true;
  m_api = TqApi::Create(m_options, &logger);
}

void TqPythonApi::SubscribeInstrumentsInfo() {
  if (m_is_backtest)
    return;

  auto req = std::make_shared<md::SubscribeObjectInfo>();
  req->subscribe_id = std::to_string(random());
  req->time_out_interval = 30000;
  req->product_class_filter = {md::ProductClass::kFuture, md::ProductClass::kStock};
  req->expired_type = ExpiredType::kBoth;
  TqSyncRequest(m_api, req);
  if (req->result_code != 0) {
    throw std::exception(std::logic_error("订阅合约信息失败."));
  }
  logger.Info("合约信息订阅完成.");
}

void TqPythonApi::Login() {
  for (auto [_, account_ptr] : m_accounts) {
    // 订阅绑定交易通知信息
    account_ptr->SubscribeNotice(m_api, [&](const std::string& msg) {
      Notify(msg);
    });

    account_ptr->Login(m_api, m_auth);

    account_ptr->TrackOrderStatus([&](const std::string& msg) {
      Notify(msg);
    });
  }

  // 确认行情服务器连接完成
  RunUntilReady(m_api, [&]() -> bool {
    auto md_session = m_api->DataDb()->GetNode<md::Session>("md_session");
    if (md_session == nullptr) {
      return false;
    }

    if (m_is_backtest && !md_session->Snap()->error_msg.compare(0, 26, "Backtest Permission Denied")) {
      throw std::exception(std::logic_error(
        "免费账户每日可以回测3次，今日暂无回测权限，需要购买专业版本后使用。升级网址：" + kAccountUrl));
    }

    return md_session->Snap()->session_status == md::SessionStatus::kLogined;
  });
  Notify("通知: 与合约服务器的网络连接已建立.");
}

void TqPythonApi::Notify(const std::string& msg) {
  if (m_disable_print)
    return;

  // 回测模式下, 通知时间为回测的时间
  auto current_dt = m_is_backtest ? m_options.backtest_service->GetCurrentDateTime() : NowAsEpochNano();

  py::gil_scoped_acquire acquire;
  py::print(EpochNanoToHumanTime(current_dt), "-", msg);
  py::gil_scoped_release release;
}

void TqPythonApi::SetupWebGui(const py::object& web_gui) {
  // auto web_conf = py::str(web_gui).cast<std::string>();
  // if (!web_conf.compare("False"))
  //  return;

  // auto& u = m_account.cast<TqUser&>();
  // m_web_helper = std::make_shared<CWebHelper>(m_api, u.m_login_req->bid, u.m_login_req->user_id, m_user_key);
  // m_web_helper->SetBacktest(m_options.backtest_service).SetSubscribles(m_sub_instruments).Run(web_conf);
}

void TqPythonApi::SetupTradingStatus() {
  m_trading_status_worker = std::make_shared<TradingStatusWorker>(m_api, logger, m_auth->GetAccessToken());
}

std::vector<int> TqPythonApi::GetTradingUnits() {
  std::vector<int> units;
  auto positions_view =
    m_api->GetTradeUnitService()->GetTradingUnitNodeDb()->CreateView<Position>([&](std::shared_ptr<const Position> p) {
      return p->user_key == m_accounts.begin()->first;
    });

  for (auto [key, node] : positions_view->GetNodes()) {
    if (std::find(units.begin(), units.end(), node->Snap()->unit_id) != units.end())
      continue;
    units.push_back(node->Snap()->unit_id);
  }

  return units;
}

void TqPythonApi::DeleteTradingUnits(const py::object& py_unit_id) {
  // 交易单元暂时不支持多账户
  if (m_accounts.begin()->second->m_trading_unit->IsEnable() && !m_auth->HasGrant(kAuthTradingUnit))
    throw std::invalid_argument("您的账户暂不支持交易单元功能, 需要购买专业版本后使用。升级网址：" + kAccountUrl);

  if (py::isinstance<py::str>(py_unit_id) && py_unit_id.cast<std::string>() == "ALL") {
    m_api->GetTradeUnitService()->DeleteTradingUnit(m_accounts.begin()->first);
    return;
  }

  auto delete_unit_id = py_unit_id.cast<int>();
  if (delete_unit_id != ktrading_unit_unset && (delete_unit_id < 1 || delete_unit_id > 99))
    throw std::invalid_argument("交易单元指定错误, 交易单元仅支持 1 - 99 中的数字类型.");

  m_api->GetTradeUnitService()->DeleteTradingUnit(m_accounts.begin()->first, delete_unit_id);
}

void TqPythonApi::AddMarketMakerStrategy(std::shared_ptr<extension::MarketMakerStrategy> mm) {
  if (!m_auth->HasGrant(kAuthMarketMaker)) {
    std::string msg = "您的账户不支持做市模块，需要购买专业版本后使用。升级网址：https://account.shinnytech.com";
    throw std::invalid_argument(msg.c_str());
  }

  if (std::find(m_market_maker_strategys.begin(), m_market_maker_strategys.end(), mm) != m_market_maker_strategys.end())
    return;

  m_market_maker_strategys.push_back(mm);
}

py::object TqPythonApi::GetDataFrame(const std::string& df_type, const std::string& key, int row, int column,
  std::vector<double>& data, const py::list& column_list, py::object& obj) {
  py::object pandas = py::module::import("pandas");
  py::object df = pandas.attr("DataFrame")(
    py::array_t<double>({row, column}, {column * sizeof(double), sizeof(double)}, data.data(), obj), "copy"_a = false,
    "columns"_a = column_list);

  py::object origin_constructor = df.attr("_constructor_sliced");
  df.attr("_constructor_sliced") = py::cpp_function([=](py::args args, py::kwargs kwargs) {
    auto series = origin_constructor(*args, **kwargs);
    series.attr("_key") = key;
    series.attr("_df_type") = df_type;
    return series;
  });
  df.attr("_key") = key;
  df.attr("_df_type") = df_type;

  return df;
}

inline std::shared_ptr<ContentNode<Instrument>> TqPythonApi::EnsureInsValid(const std::string& symbol) {
  auto exchange_id = symbol.substr(0, symbol.find("."));
  if (AnyOne(exchange_id, "SHFE", "DCE", "CZCE", "INE", "CFFEX", "KQ", "SSWE") && !m_auth->HasGrant("futr")) {
    throw std::exception(
      std::logic_error("您的账户不支持期货行情，需升级后使用。升级网址：https://account.shinnytech.com."));
  }

  if (AnyOne(exchange_id, "SSE", "SZSE") && !m_auth->HasGrant("sec")) {
    throw std::exception(
      std::logic_error("您的账户不支持股票行情，需升级后使用。升级网址：https://account.shinnytech.com."));
  }

  if (AnyOne(symbol, "SSE.000016", "SSE.000300", "SSE.000905") && !m_auth->HasGrant("lmt_idx")) {
    throw std::exception(
      std::logic_error("您的账户不支持指数行情，需升级后使用。升级网址：https://account.shinnytech.com."));
  }

  auto symbol_node = m_api->DataDb()->GetNode<Instrument>(symbol);
  if (!symbol_node && !SubscribleInstrumens(symbol)) {
    throw std::invalid_argument("合约代码 " + symbol + " 不存在, 请检查合约代码是否填写正确.");
  }

  if (!m_api->DataDb()->GetNode<Instrument>(symbol)) {
    throw std::invalid_argument("合约代码 " + symbol + " 不存在, 请检查合约代码是否填写正确.");
  }

  return m_api->DataDb()->GetNode<Instrument>(symbol);
}

std::vector<std::string> TqPythonApi::QueryQuotes(const std::string& ins_class, const std::string& exchange_id,
  const std::string& product_id, py::object& expired, py::object& has_night) {
  std::vector<ProductClass> product_class;
  if (ins_class.empty()) {
    product_class = {ProductClass::kFuture, ProductClass::kCont, ProductClass::kIndex};
  } else {
    product_class.push_back(g_ins_class.GetEnum(ins_class));
  }

  // 订阅指定合约.
  SubscribleInstrumens("", product_id, exchange_id, product_class, expired, has_night);
  // 查询指定视图.
  auto view = m_api->DataDb()->CreateView<Instrument>([=](std::shared_ptr<const Instrument> ins) {
    if (!ins_class.empty() && ins->product_class != g_ins_class.GetEnum(ins_class))
      return false;

    if (!exchange_id.empty() && ins->exchange_id != exchange_id)
      return false;

    if (!expired.is_none() && ins->expired != expired.cast<bool>())
      return false;

    bool cond = true;
    if (!product_id.empty()) {
      // 主连和指数 product_id 信息采用 instrument_id 进行比较.
      if (ins->product_class == ProductClass::kIndex || ins->product_class == ProductClass::kCont) {
        cond = cond && ins->instrument_id.substr(ins->instrument_id.find(".") + 1) == product_id;
      } else {
        cond = cond && ins->product_id == product_id;
      }
    }

    if (!has_night.is_none())
      cond = cond && (has_night.cast<bool>() ? !ins->trading_time.night.empty() : ins->trading_time.night.empty());

    return cond;
  });

  std::vector<std::string> symbols = {};
  std::transform(view->GetNodes().begin(), view->GetNodes().end(), back_inserter(symbols), RetrieveKey());

  return symbols;
};

std::vector<std::string> TqPythonApi::QueryContQuotes(
  const std::string& exchange_id, const std::string& product_id, py::object& has_night) {
  // 订阅指定合约.
  SubscribleInstrumens("", product_id, "", {ProductClass::kCont, ProductClass::kFuture}, py::none(), has_night);

  // 筛选符合条件的视图
  auto view = m_api->DataDb()->CreateView<Instrument>([=](std::shared_ptr<const Instrument> ins) {
    if (ins->product_class != ProductClass::kCont)
      return false;
    if (!exchange_id.empty() && ins->underlying_pointer.node->Snap()->exchange_id != exchange_id)
      return false;
    if (!product_id.empty() && ins->instrument_id.substr(ins->instrument_id.find(".") + 1) != product_id)
      return false;
    if (!has_night.is_none() && has_night.cast<bool>() != !ins->trading_time.night.empty())
      return false;
    return true;
  });

  std::vector<std::string> symbols = {};
  for (auto& kv : view->GetNodes()) {
    symbols.push_back(kv.second->Snap()->underlying_pointer.key);
  }

  return symbols;
}

std::vector<std::string> TqPythonApi::QueryOptions(const std::string& underlying_symbol,
  const std::string& option_class, int exercise_year, int exercise_month, double strike_price, py::object& expired,
  py::object& has_A) {
  // 订阅指定合约.
  SubscribleOptions(underlying_symbol);
  auto m = m_api->DataDb()->CreateView<Instrument>([=](std::shared_ptr<const Instrument> ins) {
    if (ins->underlying_pointer.key.empty() || ins->product_class != ProductClass::kOption) {
      return false;
    }

    if (!underlying_symbol.empty() && ins->underlying_pointer.key != underlying_symbol) {
      return false;
    }

    if (!option_class.empty() && ins->option_class != g_option_class_mapping.GetEnum(option_class)) {
      return false;
    }

    int ins_exercise_year = std::stoi(ins->last_exercise_day_str.substr(0, 4).c_str());
    if (exercise_year && ins_exercise_year != exercise_year) {
      return false;
    }

    int ins_exercise_month = std::stoi(ins->last_exercise_day_str.substr(4, 2).c_str());
    if (exercise_month && ins_exercise_month != exercise_month) {
      return false;
    }

    if (!DoubleEqual(strike_price, 0.0) && !DoubleEqual(ins->strike_price, strike_price)) {
      return false;
    }

    if (!expired.is_none() && ins->expired != expired.cast<bool>()) {
      return false;
    }

    bool cond = true;
    if (!has_A.is_none()) {
      cond = cond && has_A.cast<bool>() ? ins->english_name.find('A') != std::string::npos
                                        : ins->english_name.find('A') == std::string::npos;
    }

    return cond;
  });

  std::vector<std::string> symbols = {};
  for (auto& kv : m->GetNodes()) {
    symbols.push_back(kv.first);
  }

  return symbols;
}

std::vector<std::vector<std::string>> TqPythonApi::QueryAllLevelOptions(const std::string& underlying_symbol,
  double underlying_price, const std::string& option_class, int exercise_year, int exercise_month, py::object& has_A) {
  // 订阅指定合约
  SubscribleOptions(underlying_symbol);

  // 条件筛选
  auto m = m_api->DataDb()->CreateView<Instrument>([=](std::shared_ptr<const Instrument> ins) {
    if (ins->underlying_pointer.key.empty() || ins->product_class != ProductClass::kOption) {
      return false;
    }

    if (!underlying_symbol.empty() && ins->underlying_pointer.key != underlying_symbol) {
      return false;
    }

    if (!option_class.empty() && ins->option_class != g_option_class_mapping.GetEnum(option_class)) {
      return false;
    }

    int ins_exercise_year = std::stoi(ins->last_exercise_day_str.substr(0, 4).c_str());
    if (exercise_year && ins_exercise_year != exercise_year) {
      return false;
    }

    int ins_exercise_month = std::stoi(ins->last_exercise_day_str.substr(4, 2).c_str());
    if (exercise_month && ins_exercise_month != exercise_month) {
      return false;
    }

    if (ins->expired == true) {
      return false;
    }

    bool cond = true;
    if (!has_A.is_none()) {
      cond = cond && has_A.cast<bool>() ? ins->english_name.find('A') != std::string::npos
                                        : ins->english_name.find('A') == std::string::npos;
    }

    return cond;
  });

  // 按照行权价格排序
  std::vector<std::pair<std::string, double>> symbols_with_strike_price = {};
  for (auto& [k, node] : m->GetNodes()) {
    symbols_with_strike_price.push_back(std::make_pair(k, node->Latest()->strike_price));
  }
  std::sort(symbols_with_strike_price.begin(), symbols_with_strike_price.end());
  // 根据标的价格确定平值期权索引
  int min_dvalue_pos = 0;
  double min_dvalue = 20482048;
  for (size_t index = 0; index < symbols_with_strike_price.size(); ++index) {
    auto d = std::abs(symbols_with_strike_price.at(index).second - underlying_price);
    if (d < min_dvalue) {
      min_dvalue = d;
      min_dvalue_pos = index;
    }
  }

  // 返回实值期权、平值期权、虚值期权的结构化绑定

  std::vector<std::string> in_money_options = {};
  std::vector<std::string> at_money_options = {};
  std::vector<std::string> out_of_money_options = {};

  for (size_t index = 0; index < symbols_with_strike_price.size(); ++index) {
    if (index < min_dvalue_pos) {
      if (option_class == "CALL") {
        in_money_options.push_back(symbols_with_strike_price.at(index).first);
      } else {
        out_of_money_options.push_back(symbols_with_strike_price.at(index).first);
      }
    } else if (index == min_dvalue_pos) {
      at_money_options.push_back(symbols_with_strike_price.at(index).first);
    } else {
      if (option_class == "CALL") {
        out_of_money_options.push_back(symbols_with_strike_price.at(index).first);
      } else {
        in_money_options.push_back(symbols_with_strike_price.at(index).first);
      }
    }
  }

  // 虚值期权
  return {in_money_options, at_money_options, out_of_money_options};
}

bool TqPythonApi::SubscribleInstrumens(const std::string& symbol, const std::string& product_id,
  const std::string& exchange_id, std::vector<ProductClass> product_class, py::object include_expired,
  py::object has_night) {
  auto req = std::make_shared<md::SubscribeObjectInfo>();
  req->subscribe_id = std::to_string(random());

  if (!product_class.empty())
    req->product_class_filter = product_class;

  if (!symbol.empty())
    req->instrument_id.push_back(symbol);

  if (!exchange_id.empty())
    req->exchange_id.push_back(exchange_id);

  if (!product_id.empty())
    req->product_id.push_back(product_id);

  if (include_expired.is_none()) {
    req->expired_type = ExpiredType::kBoth;
  } else {
    req->expired_type = include_expired.cast<bool>() ? ExpiredType::kBoth : ExpiredType::kNotExpired;
  }

  if (!has_night.is_none())
    req->has_night = has_night.cast<bool>() ? HasNight::kHasNight : HasNight::kHasNoNight;

  req->timestamp = m_is_backtest ? m_options.backtest_service->GetCurrentDateTime() : -1;
  TqSyncRequest(m_api, req);
  if (req->result_code) {
    logger.Error("合约信息订阅失败, " + req->result_msg);
    return false;
  }
  return true;
}

bool TqPythonApi::SubscribleOptions(const std::string& underlying_symbol) {
  auto req = std::make_shared<md::SubscribeOptionsByUnderlyingSymbol>();
  req->subscribe_id = std::to_string(random());
  req->symbol = {underlying_symbol};
  req->timestamp = m_is_backtest ? m_options.backtest_service->GetCurrentDateTime() : -1;
  TqSyncRequest(m_api, req);
  if (req->result_code != 0) {
    logger.Error("合约信息订阅失败, " + req->result_msg);
    return false;
  }
  return true;
}

std::shared_ptr<TradingStatus> TqPythonApi::GetTradingStatus(const std::string& symbol) {
  m_trading_status_worker->ConnectServer()->SubInstruments(symbol);

  RunUntilReady(m_api, [&]() {
    m_trading_status_worker->RunOnce();
    return !m_trading_status_worker->m_trading_status[symbol]->status.empty();
  });

  return m_trading_status_worker->m_trading_status[symbol];
}

std::shared_ptr<extension::TargetPosAgent> TqPythonApi::GetTargetPosAgent(const std::string& symbol,
  const std::string& price, const std::string& priority, int unit_id, const py::object& py_account,
  const py::object& price_func) {
  auto account_ptr = GetAccountPtrFromPythonObject(py_account);
  auto user_key = account_ptr->m_user_key;
  auto key = symbol + "-" + price + "-" + priority + "-" + user_key + "-" + std::to_string(unit_id);

  if (m_target_pos_task_map.find(key) == m_target_pos_task_map.end()) {
    EnsureInsValid(symbol);

    if (price_func.is_none()) {
      m_target_pos_task_map[key] = TargetPosAgent::Create(m_api, user_key, symbol, unit_id, price, priority);
    } else {
      m_target_pos_task_map[key] = TargetPosAgent::Create(
        m_api, user_key, symbol, unit_id, price, priority, [price_func](const future::Direction& direction) {
          std::string dir = direction == future::Direction::kBuy ? "BUY" : "SELL";
          return price_func(dir).cast<double>();
        });
    }
  }

  return m_target_pos_task_map[key];
}

std::shared_ptr<TqBaseAccount> TqPythonApi::GetAccountPtrFromPythonObject(const py::object& account) {
  // 获取账户实例, 单账户时, 返回唯一的账户实例; 多账户时, 返回入参对应的账户实例
  if (m_accounts.size() == 1) {
    return m_accounts.begin()->second;
  } else if (m_accounts.size() > 1) {
    if (account.is_none()) {
      throw std::invalid_argument("多账户模式下, 需要指定账户实例 account");
    }

    auto user_key = account.attr("_account_key").cast<std::string>();
    if (m_accounts.find(user_key) == m_accounts.end()) {
      throw std::invalid_argument("无该账户实例, 请确认账户实例参数 account 是否正确");
    }
    return m_accounts[user_key];
  }

  return nullptr;
}

void TqPythonApi::AliasFuncWhenSecurities() {
  if (m_accounts.size() > 1) {
    return;
  }
  // 单账户模式，且唯一账户为股票账户
  if (m_accounts.size() == 1 && m_accounts.begin()->second->m_account_type == TqAccountType::kKqStock) {
    py::exec(R"(
        TqApi.get_account = TqApi._get_stock_account
        TqApi.get_order = TqApi._get_stock_order
        TqApi.get_trade = TqApi._get_stock_trade
        TqApi.get_position = TqApi._get_stock_position
        TqApi.insert_order = TqApi._insert_stock_order
        TqApi.cancel_order = TqApi._cancel_stock_order
    )");
  }
}

std::shared_ptr<security::AccountNode> TqPythonApi::GetStockAccount() {
  return m_accounts.begin()->second->GetStockAccount();
}

std::shared_ptr<security::OrderNode> TqPythonApi::GetStockOrder(const std::string& order_id) {
  return m_accounts.begin()->second->GetStockOrder(order_id);
}

const std::map<std::string, std::shared_ptr<security::OrderNode>>& TqPythonApi::GetStockOrders() {
  return m_accounts.begin()->second->GetStockOrders();
}

std::shared_ptr<security::TradeNode> TqPythonApi::GetStockTrade(const std::string& trade_id) {
  return m_accounts.begin()->second->GetStockTrade(trade_id);
}

const std::map<std::string, std::shared_ptr<security::TradeNode>>& TqPythonApi::GetStockTrades() {
  return m_accounts.begin()->second->GetStockTrades();
}

std::shared_ptr<security::PositionNode> TqPythonApi::GetStockPosition(const std::string& symbol) {
  return m_accounts.begin()->second->GetStockPosition(symbol);
}

const std::map<std::string, std::shared_ptr<security::PositionNode>>& TqPythonApi::GetStockPositions() {
  return m_accounts.begin()->second->GetStockPositions();
}

std::shared_ptr<security::OrderNode> TqPythonApi::InsertStockOrder(
  const std::string& symbol, const std::string& direction, int volume, py::object& limit_price) {
  if (volume <= 0) {
    throw std::invalid_argument("下单股数 " + std::to_string(volume) + " 错误, 请检查 volume 是否填写正确.");
  }

  auto node = EnsureInsValid(symbol);
  if (node->Snap()->exchange_time_str.empty()) {
    GetQuote(symbol);
  }

  m_auth->HasTdGrant(symbol, node->Latest()->product_class);

  auto req = std::make_shared<security::InsertOrder>(m_accounts.begin()->first);
  req->exchange_id = symbol.substr(0, symbol.find("."));
  req->instrument_id = symbol.substr(symbol.find(".") + 1);
  req->direction = direction == "BUY" ? security::Direction::kBuy : security::Direction::kSell;
  if (limit_price.is_none()) {
    req->price_type = security::PriceType::kAny;
  } else {
    double price = limit_price.cast<double>();
    if (std::isnan(price)) {
      throw std::invalid_argument("委托价格非法, 请检查价格是否填写正确.");
    }
    req->limit_price = price;
    req->price_type = security::PriceType::kLimit;
  }
  req->volume = volume;
  return m_accounts.begin()->second->InsertStockOrder(req, [&](const std::string& msg) {
    Notify(msg);
  });
}

void TqPythonApi::CancelStockOrder(py::object& o) {
  if (o.is_none())
    throw std::invalid_argument("撤单失败, 委托或委托单号不能为空.");

  std::string name = o.attr("__class__").attr("__name__").cast<std::string>();
  auto order_id = name == "SecuritiesOrder" ? o.attr("order_id").cast<std::string>() : o.cast<std::string>();

  return m_accounts.begin()->second->CancelStockOrder(order_id, [&](const std::string& msg) {
    Notify(msg);
  });
}

}  // namespace TqSdk2
