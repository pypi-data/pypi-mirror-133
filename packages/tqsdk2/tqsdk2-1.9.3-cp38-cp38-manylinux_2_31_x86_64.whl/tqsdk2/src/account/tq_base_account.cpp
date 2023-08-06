/*******************************************************************************
 * @file tq_base_account.cpp
 * @brief 期货账户基类
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "tq_base_account.h"
#include "../field_mapping.h"

namespace TqSdk2 {
TqBaseAccount::TqBaseAccount() : m_latest_local_order_id(0), m_trading_unit(std::make_shared<TradingUnit>()) {}

void TqBaseAccount::SubscribeNotice(std::shared_ptr<TqApi> api, std::function<void(const std::string&)> notify) {
  notify("通知: 账户 " + m_user_key + " 与交易服务器的网络连接已建立.");

  m_notice_view = api->DataDb()->CreateView<Notice>();
  m_notice_view->AfterCommit(std::to_string((int64_t)this), [=](std::shared_ptr<const NoticeNode> node) -> void {
    notify("通知: 账户 " + m_user_key + " " + node->Latest()->content);
  });
}

void TqBaseAccount::TrackOrderStatus(std::function<void(const std::string&)> notify) {
  m_alive_order_view = m_api->DataDb()->CreateView<TqApiViewKey, Order>(TqApiViewKey::kAliveOrder);
  m_alive_order_view->AfterCommit(std::to_string((int64_t)this), [=](std::shared_ptr<OrderNode> node) -> void {
    if (node->Latest()->user_key == m_user_key) {
      std::string msg = "通知: 账户 " + m_user_key + ", 订单号:" + node->Snap()->order_id
        + ", 开平:" + g_offset_mapping.GetEnumValue(node->Snap()->offset)
        + ", 方向:" + g_direction_mapping.GetEnumValue(node->Snap()->direction) + std::string(", 委托数量:")
        + std::to_string(node->Snap()->volume_orign) + std::string(", 未成交数量:")
        + std::to_string(node->Snap()->volume_left) + std::string(", 价格:") + std::to_string(node->Snap()->limit_price)
        + std::string(", 状态:") + g_order_status.GetEnumValue(node->Latest()->status);
      if (!node->Snap()->status_msg.empty()) {
        msg += std::string(", 信息:") + node->Latest()->status_msg;
      }
      notify(msg);
    }
  });
}

std::shared_ptr<future::OrderNode> TqBaseAccount::InsertOrder(
  std::shared_ptr<future::InsertOrder> req, std::function<void(const std::string&)> notify) {
  TqSyncRequest(m_api, req);

  auto order_node = m_api->DataDb()->GetNode<future::Order>(m_user_key + "|" + req->order_id);
  if (req->result_code != 0) {
    if (order_node == nullptr) {
      auto o = std::make_shared<future::Order>();
      o->order_id = "tqsdk2|" + std::to_string((int64_t)this) + "|" + std::to_string(++m_latest_local_order_id);
      o->exchange_id = req->exchange_id;
      o->instrument_id = req->instrument_id;
      o->direction = req->direction;
      o->price_type = req->price_type;
      o->limit_price = req->limit_price;
      o->offset = req->offset;
      o->time_condition = req->time_condition;
      o->volume_condition = req->volume_condition;
      o->volume_orign = req->volume;
      o->volume_left = req->volume;
      o->status = OrderStatus::kDead;
      o->status_msg = req->result_msg;
      o->user_key = m_user_key;
      return m_api->DataDb()->ReplaceRecord<Order>(o);
    }

    notify("通知: 账户:" + m_user_key + " 下单失败, 委托单编号:" + req->order_id + ", " + req->result_msg);
  }

  return order_node;
}

void TqBaseAccount::CancelOrder(const std::string& order_id, std::function<void(const std::string&)> notify) {
  auto req = std::make_shared<future::CancelOrder>(m_user_key);
  req->order_id = order_id;
  TqSyncRequest(m_api, req);
  if (req->result_code != 0) {
    notify("通知: 账户:" + m_user_key + " 撤单失败, 委托单号:" + order_id + ", " + req->result_msg);
  }
}

std::shared_ptr<future::OrderNode> TqBaseAccount::GetOrder(const std::string& order_id) {
  return m_api->DataDb()->GetNode<future::Order>(m_user_key + "|" + order_id);
}

const std::map<std::string, std::shared_ptr<OrderNode>>& TqBaseAccount::GetOrders(int unit_id) {
  auto trading_unit_id = GetCurrentUnitID(unit_id);
  auto view_key = m_user_key + "|" + std::to_string(trading_unit_id);

  if (m_orders_views.find(view_key) != m_orders_views.end()) {
    return m_orders_views[view_key]->GetNodes();
  }

  m_orders_views[view_key] = m_api->DataDb()->CreateView<Order>(
    [=](std::shared_ptr<const Order> o) {
      return o->user_key == m_user_key && (trading_unit_id == ktrading_unit_unset ? 1 : trading_unit_id == o->unit_id);
    },
    [&](std::shared_ptr<const Order> o) {
      return o->order_id;
    });

  return m_orders_views[view_key]->GetNodes();
}

std::shared_ptr<future::TradeNode> TqBaseAccount::GetTrade(const std::string& trade_id) {
  return m_api->DataDb()->GetNode<future::Trade>(m_user_key + "|" + trade_id);
}

const std::map<std::string, std::shared_ptr<TradeNode>>& TqBaseAccount::GetTrades(int unit_id) {
  auto trading_unit_id = GetCurrentUnitID(unit_id);
  auto view_key = m_user_key + "|" + std::to_string(trading_unit_id);

  if (m_trades_views.find(view_key) != m_trades_views.end()) {
    return m_trades_views[view_key]->GetNodes();
  }

  m_trades_views[view_key] = m_api->DataDb()->CreateView<Trade>(
    [=](std::shared_ptr<const Trade> t) {
      return t->user_key == m_user_key && (trading_unit_id == ktrading_unit_unset ? 1 : t->unit_id == trading_unit_id);
    },
    [&](std::shared_ptr<const Trade> t) {
      return t->exchange_trade_id;
    });

  return m_trades_views[view_key]->GetNodes();
}

std::shared_ptr<future::PositionNode> TqBaseAccount::GetPosition(const std::string& symbol, int unit_id) {
  auto trading_unit_id = GetCurrentUnitID(unit_id);

  std::string position_key = m_user_key + "|" + std::to_string(trading_unit_id) + "|" + symbol;
  m_positions_views[position_key] = m_api->DataDb()->CreateView<Position>([=](std::shared_ptr<const Position> content) {
    return content->unit_id == trading_unit_id && content->user_key == m_user_key && content->symbol() == symbol;
  });

  auto position_node = m_positions_views[position_key]->GetNodes();
  if (position_node.empty()) {
    return m_api->DataDb()->ReplaceRecord(GeneratePosition(symbol, trading_unit_id));
  }

  return position_node.at(position_key);
}

const std::map<std::string, std::shared_ptr<PositionNode>>& TqBaseAccount::GetPositions(int unit_id) {
  auto trading_unit_id = GetCurrentUnitID(unit_id);
  auto view_key = m_user_key + "|" + std::to_string(trading_unit_id);

  if (m_positions_views.find(view_key) != m_positions_views.end()) {
    return m_positions_views[view_key]->GetNodes();
  }

  if (trading_unit_id != ktrading_unit_unset) {
    m_positions_views[view_key] = m_api->GetTradeUnitService()->GetTradingUnitNodeDb()->CreateView<Position>(
      [=](std::shared_ptr<const Position> content) {
        return content->unit_id == trading_unit_id && content->user_key == m_user_key;
      },
      [&](std::shared_ptr<const Position> content) {
        return content->symbol();
      });
  } else {
    m_positions_views[view_key] = m_api->DataDb()->CreateView<Position>(
      [=](std::shared_ptr<const Position> content) {
        return content->user_key == m_user_key;
      },
      [&](std::shared_ptr<const Position> content) {
        return content->symbol();
      });
  }

  return m_positions_views[view_key]->GetNodes();
}

std::shared_ptr<future::AccountNode> TqBaseAccount::GetAccount(int unit_id) {
  auto trading_unit_id = GetCurrentUnitID(unit_id);
  std::string account_key = m_user_key + "|" + std::to_string(trading_unit_id) + "|CNY";

  if (m_account_views.find(account_key) == m_account_views.end()) {
    m_account_views[account_key] =
      m_api->DataDb()->CreateView<future::Account>([=](std::shared_ptr<const Account> content) {
        return content->user_key == m_user_key;
      });
  }

  return m_account_views[account_key]->GetNodes().at(account_key);
}

void TqBaseAccount::EnableTradingUnit(int trading_unit) {
  if (trading_unit != ktrading_unit_unset) {
    m_trading_unit->EnableTradingUnit(trading_unit);
  }
}

int TqBaseAccount::GetCurrentUnitID(int unit_id) {
  if (unit_id != ktrading_unit_unset && (unit_id < 1 || unit_id > 99)) {
    throw std::invalid_argument("交易单元指定错误, 交易单元仅支持 1 - 99 中的数字类型.");
  }

  if (m_trading_unit->IsEnable() && !m_auth->HasGrant(kAuthTradingUnit)) {
    throw std::invalid_argument("您的账户暂不支持交易单元功能, 需要购买专业版本后继续使用。升级网址：" + kAccountUrl);
  }

  if (unit_id != ktrading_unit_unset && m_login_req->backend == BackEnd::kLocalSim) {
    throw std::invalid_argument("本地模拟账户 TqSim 暂不支持交易单元功能.");
  }

  if (!m_trading_unit->IsEnable() && unit_id != ktrading_unit_unset) {
    throw std::invalid_argument("交易单元功能未启用, 请在初始化账户实例时指定默认交易单元.");
  }

  return unit_id == ktrading_unit_unset ? m_trading_unit->GetDefaultUnitID() : unit_id;
}

std::shared_ptr<Position> TqBaseAccount::GeneratePosition(const std::string& symbol, int unit_id) {
  auto p = std::make_shared<Position>();
  p->user_key = m_user_key;
  p->unit_id = unit_id;
  p->investor_id = m_user_key;
  p->exchange_id = symbol.substr(0, symbol.find("."));
  p->instrument_id = symbol.substr(symbol.find(".") + 1);
  p->ins_pointer.key = symbol;
  p->ins_pointer.node = m_api->DataDb()->GetNode<Instrument>(symbol);
  return p;
}

// 股票接口
std::shared_ptr<security::AccountNode> TqBaseAccount::GetStockAccount() {
  return m_api->DataDb()->GetNode<security::Account>(m_user_key + "|CNY");
}

std::shared_ptr<security::OrderNode> TqBaseAccount::GetStockOrder(const std::string& order_id) {
  auto order_key = m_user_key + "|" + order_id;
  return m_api->DataDb()->GetNode<security::Order>(order_key);
}

const std::map<std::string, std::shared_ptr<security::OrderNode>>& TqBaseAccount::GetStockOrders() {
  return m_api->DataDb()->GetNodeMap<security::Order>();
}

std::shared_ptr<security::TradeNode> TqBaseAccount::GetStockTrade(const std::string& trade_id) {
  return m_api->DataDb()->GetNode<security::Trade>(trade_id);
}

const std::map<std::string, std::shared_ptr<security::TradeNode>>& TqBaseAccount::GetStockTrades() {
  return m_api->DataDb()->GetNodeMap<security::Trade>();
}

std::shared_ptr<security::PositionNode> TqBaseAccount::GetStockPosition(const std::string& symbol) {
  std::string key = m_user_key + "|" + symbol;
  return m_api->DataDb()->GetNode<security::Position>(key);
}

const std::map<std::string, std::shared_ptr<security::PositionNode>>& TqBaseAccount::GetStockPositions() {
  return m_api->DataDb()->GetNodeMap<security::Position>();
}

std::shared_ptr<security::OrderNode> TqBaseAccount::InsertStockOrder(
  std::shared_ptr<security::InsertOrder> req, std::function<void(const std::string&)> notify) {
  TqSyncRequest(m_api, req);
  auto view_key = m_user_key + "|" + req->order_id;
  auto insert_order_node = m_api->DataDb()->GetNode<security::Order>(view_key);
  if (req->result_code != 0 && insert_order_node == nullptr) {
    auto o = std::make_shared<security::Order>();
    o->order_id = "tqsdk2|" + std::to_string((int64_t)this) + "|" + std::to_string(++m_latest_local_order_id);
    o->exchange_id = req->exchange_id;
    o->instrument_id = req->instrument_id;
    o->direction = req->direction;
    o->price_type = req->price_type;
    o->limit_price = req->limit_price;
    o->volume_orign = req->volume;
    o->volume_left = req->volume;
    o->status = security::OrderStatus::kDead;
    o->status_msg = req->result_msg;
    o->user_key = m_user_key;
    notify("通知: 下单失败, 委托单ID:" + o->order_id + ", " + req->result_msg);
    return m_api->DataDb()->ReplaceRecord<security::Order>(o);
  }

  return insert_order_node;
}

void TqBaseAccount::CancelStockOrder(const std::string& order_id, std::function<void(const std::string&)> notify) {
  auto req = std::make_shared<security::CancelOrder>(m_user_key);
  req->order_id = order_id;
  TqSyncRequest(m_api, req);
  if (req->result_code != 0) {
    notify("通知: 撤单失败, 委托单号:" + order_id + ", " + req->result_msg);
  }
}

}  // namespace TqSdk2
