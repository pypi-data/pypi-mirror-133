/*******************************************************************************
 * @file tq_account.cpp
 * @brief 中继账户类
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "tq_account.h"

namespace TqSdk2 {

TqAccount::TqAccount(const std::string& broker_id, const std::string& account_id, const std::string& password,
  int trading_unit, const std::string& _td_url) {
  m_user_key = account_id;
  m_login_req = std::make_shared<future::ReqLogin>(m_user_key);
  m_login_req->bid = broker_id;
  m_login_req->client_app_id = "SHINNY_TQ_1.0";
  m_login_req->user_id = account_id;
  m_login_req->password = password;
  m_login_req->user_key = m_user_key;
  m_login_req->otg.front_url = _td_url;
  m_login_req->backend = BackEnd::kOtg;

  m_td_url = _td_url.empty() ? "" : _td_url;
  m_account_type = TqAccountType::kOtg;

  EnableTradingUnit(trading_unit);
}

void TqAccount::Login(std::shared_ptr<TqApi> api, std::shared_ptr<TqAuth> auth) {
  m_api = api;

  if (!auth->HasAccountGranted(m_login_req->user_id)) {
    TqHttpClient cli(auth);
    cli.BindAccount(m_login_req->user_id);
  }

  if (m_login_req->otg.front_url.empty()) {
    TqHttpClient cli(auth);
    m_login_req->otg.front_url = cli.GetTradeUrl(m_login_req->bid);
  }

  // 确认交易服务器连接完成
  TqSyncRequest(api, m_login_req);
  if (m_login_req->result_code != 0) {
    throw std::exception(std::logic_error("用户登录失败, " + m_login_req->result_msg));
  }

  RunUntilReady(api, [&]() -> bool {
    auto login_node = api->DataDb()->GetNode<future::LoginContent>(m_user_key);
    return login_node && login_node->Snap()->account_ready && login_node->Snap()->position_ready;
  });

  // 确认结算单
  auto req = std::make_shared<ConfirmSettlementInfo>(m_user_key);
  TqSyncRequest(api, req);
}

}  // namespace TqSdk2
