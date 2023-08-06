/*******************************************************************************
 * @file tq_kq.cpp
 * @brief 快期模拟
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "tq_kq.h"

namespace TqSdk2 {
TqKq::TqKq(int trading_unit, const std::string& _td_url) {
  m_td_url = _td_url.empty() ? "wss://otg-sim.shinnytech.com/trade" : _td_url;
  m_account_type = TqAccountType::kKq;
  EnableTradingUnit(trading_unit);
}

void TqKq::Login(std::shared_ptr<TqApi> api, std::shared_ptr<TqAuth> auth) {
  m_api = api;
  m_user_key = auth->GetUserID();

  m_login_req = std::make_shared<future::ReqLogin>(m_user_key);
  m_login_req->otg.front_url = m_td_url;
  m_login_req->bid = "快期模拟";
  m_login_req->backend = BackEnd::kOtg;
  m_login_req->user_key = m_user_key;
  m_login_req->user_id = m_user_key;
  m_login_req->password = m_user_key;

  // 若登录用户不在可交易账户中，则尝试自动绑定.
  if (!auth->HasAccountGranted(m_login_req->user_id)) {
    TqHttpClient cli(auth);
    cli.BindAccount(m_login_req->user_id);
  }

  // 登录账户
  TqSyncRequest(api, m_login_req);
  if (m_login_req->result_code != 0) {
    throw std::exception(std::logic_error("用户登录失败, " + m_login_req->result_msg));
  }

  RunUntilReady(api, [&]() -> bool {
    auto login_node = api->DataDb()->GetNode<future::LoginContent>(m_user_key);
    return login_node && login_node->Snap()->account_ready && login_node->Snap()->position_ready;
  });
}

}  // namespace TqSdk2
