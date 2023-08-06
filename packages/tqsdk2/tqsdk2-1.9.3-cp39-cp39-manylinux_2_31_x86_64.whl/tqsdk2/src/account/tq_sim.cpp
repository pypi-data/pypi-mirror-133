/*******************************************************************************
 * @file account.cpp
 * @brief TqSDK2 账户实例声明
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "tq_sim.h"

namespace TqSdk2 {

TqSim::TqSim(double init_balance, const std::string& user_key) {
  m_user_key = user_key.empty() ? std::to_string((int64_t)this) : user_key;
  m_init_balance = init_balance;
  m_login_req = std::make_shared<future::ReqLogin>(m_user_key);
  m_login_req->bid = "TqSim";
  m_login_req->user_id = m_user_key;
  m_login_req->backend = BackEnd::kLocalSim;

  m_account_type = TqAccountType::kSim;
}

void TqSim::Login(std::shared_ptr<TqApi> api, std::shared_ptr<TqAuth> auth) {
  m_api = api;
  // 确认交易服务器连接完成
  TqSyncRequest(api, m_login_req);
  if (m_login_req->result_code != 0) {
    throw std::exception(std::logic_error("用户登录失败, " + m_login_req->result_msg));
  }

  RunUntilReady(api, [&]() -> bool {
    auto login_node = api->DataDb()->GetNode<future::LoginContent>(m_user_key);
    return login_node && login_node->Snap()->account_ready && login_node->Snap()->position_ready;
  });

  // 模拟账户初始化资金通过银期接口完成
  auto req = std::make_shared<TransferMoney>(m_user_key);
  req->is_deposit = m_init_balance > kSimInitBalance;
  req->amount = std::abs(m_init_balance - kSimInitBalance);
  TqSyncRequest(api, req);
}

double TqSim::SetCommission(const std::string& symbol, double commission) {
  auto req = std::make_shared<SetCommissionRate>(m_user_key);
  req->instrument_id = symbol.substr(symbol.find(".") + 1);
  req->volume_commission = commission;
  TqSyncRequest(m_api, req);

  return commission;
}

double TqSim::GetCommission(const std::string& symbol) {
  auto instrument_id = symbol.substr(symbol.find(".") + 1);
  auto rate_node = m_api->DataDb()->GetNode<Rate>(m_user_key + "|" + instrument_id);
  if (rate_node && !rate_node->Latest()->commission_rates.empty()
    && !isnan(rate_node->Latest()->commission_rates[0].volume_rate))
    return rate_node->Latest()->commission_rates[0].volume_rate;

  return m_api->DataDb()->GetNode<md::Instrument>(symbol)->Latest()->commission;
}

double TqSim::SetMargin(const std::string& symbol, double margin) {
  auto req = std::make_shared<SetMarginRate>(m_user_key);
  req->instrument_id = symbol.substr(symbol.find(".") + 1);
  req->volume_margin = margin;
  TqSyncRequest(m_api, req);

  return margin;
}

double TqSim::GetMargin(const std::string& symbol) {
  auto instrument_id = symbol.substr(symbol.find(".") + 1);
  auto rate_node = m_api->DataDb()->GetNode<Rate>(m_user_key + "|" + instrument_id);
  if (rate_node && !rate_node->Latest()->margin_rates.empty()
    && !isnan(rate_node->Latest()->margin_rates[0].volume_rate))
    return rate_node->Latest()->margin_rates[0].volume_rate;

  return m_api->DataDb()->GetNode<md::Instrument>(symbol)->Latest()->margin;
}

std::shared_ptr<OrderNode> TqSim::GetOrder(const std::string& order_id, int unit_id) {
  return m_api->DataDb()->GetNode<Order>(m_user_key + "|" + order_id);
}

}  // namespace TqSdk2
