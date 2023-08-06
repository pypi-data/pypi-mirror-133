/*******************************************************************************
 * @file tq_kq_stock.cpp
 * @brief 天勤股票模拟
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "tq_kq_stock.h"

namespace TqSdk2 {

TqKqStock::TqKqStock(int trading_unit, const std::string& _td_url) {
  m_td_url = _td_url.empty() ? "wss://otg-sim-securities.shinnytech.com/trade" : _td_url;
  m_account_type = TqAccountType::kKqStock;
  EnableTradingUnit(trading_unit);
}

void TqKqStock::Login(std::shared_ptr<TqApi> api, std::shared_ptr<TqAuth> auth) {
  m_api = api;
  m_user_key = auth->GetUserID() + "-sim-securities";

  m_stock_login_req = std::make_shared<security::ReqLogin>(m_user_key);
  m_stock_login_req->otg.front_url = m_td_url;
  m_stock_login_req->bid = "快期股票模拟";
  m_stock_login_req->user_key = m_user_key;
  m_stock_login_req->user_id = m_user_key;
  m_stock_login_req->password = m_user_key;
  m_stock_login_req->backend = security::BackEnd::kOtg;

  // 登录账户
  TqSyncRequest(api, m_stock_login_req);
  if (m_stock_login_req->result_code != 0) {
    throw std::logic_error("用户登录失败, " + m_login_req->result_msg);
  }

  RunUntilReady(api, [&]() -> bool {
    auto login_ready = api->DataDb()->GetNode<security::LoginContent>(m_user_key);
    return login_ready && login_ready->Snap()->account_ready && login_ready->Snap()->position_ready;
  });
}

}  // namespace TqSdk2
