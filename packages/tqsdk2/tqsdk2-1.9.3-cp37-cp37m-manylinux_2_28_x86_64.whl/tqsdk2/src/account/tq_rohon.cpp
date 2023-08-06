/*******************************************************************************
 * @file tq_rohon.cpp
 * @brief 融航资管
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "tq_rohon.h"

namespace TqSdk2 {

TqRohon::TqRohon(const std::string& front_url, const std::string& front_broker, const std::string& app_id,
  const std::string& auth_code, const std::string& account_id, const std::string& password, int trading_unit) {
  m_user_key = account_id;
  m_login_req = std::make_shared<future::ReqLogin>(m_user_key);
  m_login_req->bid = front_broker;
  m_login_req->broker.ctp_broker_id = front_broker;
  m_login_req->broker.trading_fronts.push_back(front_url);
  m_login_req->broker.product_info = std::string("shinny_tqsdk_01");
  m_login_req->broker.app_id = app_id;
  m_login_req->broker.auth_code = auth_code;
  m_login_req->user_id = account_id;
  m_login_req->password = password;
  m_login_req->user_key = m_user_key;
  m_login_req->backend = BackEnd::kRohon;

  m_account_type = TqAccountType::kRohon;
  // 启用交易单元
  EnableTradingUnit(trading_unit);
}

void TqRohon::Login(std::shared_ptr<TqApi> api, std::shared_ptr<TqAuth> auth) {
  m_api = api;
  if (!auth->HasGrant(kAuthRohon)) {
    std::string msg = "您的账户不支持直连融航资管柜台，需要购买专业版本后使用。升级网址：" + kAccountUrl;
    throw std::exception(std::logic_error(msg.c_str()));
  }

  //若登录用户不在可交易账户中，则尝试自动绑定.
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

  // 确认结算单, 融航资管无需确认结算单
}

}  // namespace TqSdk2
