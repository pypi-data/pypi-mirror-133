/*******************************************************************************
 * @file binding.cpp
 * @brief 天勤 2 账户类
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "tq_base_account.h"
#include "tq_sim.h"
#include "tq_account.h"
#include "tq_sim.h"
#include "tq_kq.h"
#include "tq_ctp.h"
#include "tq_rohon.h"
#include "tq_kq_stock.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace TqSdk2 {

void BindingTqAccount(py::module_& m) {
  py::class_<TqBaseAccount> base_account(m, "TqBaseAccount");
  base_account.def_property_readonly(
    "_account_key",
    [](const TqBaseAccount& base_account) {
      return base_account.m_user_key;
    },
    "账户 user_key");

  /**
   * 中继账户类
   */
  py::class_<TqAccount> tqaccount(m, "TqAccount", base_account);
  tqaccount.def(py::init<const std::string&, const std::string&, const std::string&, int, const std::string&>(),
    py::arg("broker_id"), py::arg("account_id"), py::arg("password"),
    py::arg("default_trading_unit") = ktrading_unit_unset, py::arg("_td_url") = std::string(),
    R"pbdoc(
      天勤2实盘类,  通过中继服务器接入券商柜台.

      Args:
        broker_id (str):            [必填] 期货公司, 支持的期货公司列表见 https://www.shinnytech.com/blog/tq-support-broker/.

        account_id (str):           [必填] 帐号.

        password (str):             [必填] 密码.

        default_trading_unit (int): [可选] 默认交易单元, 如果指定该参数, 后续下单查询等操作均视为对该交易单元的操作.

     )pbdoc");

  /**
   * 快期模拟
   */
  py::class_<TqKq> tqkq(m, "TqKq", base_account);
  tqkq.def(py::init<int, const std::string&>(), py::arg("default_trading_unit") = ktrading_unit_unset,
    py::arg("_td_url") = std::string(), R"pbdoc( 
      天勤2 快期模拟交易类, 快期模拟账户与信易账户相匹配, 该账户的信息在快期PC、快期App、天勤和天勤2不同产品之间也是同步的.

      Args:
        default_trading_unit (int): [可选] 默认交易单元, 如果指定该参数, 后续下单查询等操作均视为对该交易单元的操作.
    )pbdoc");

  /**
   * TqSim 本地模拟类
   */
  py::class_<TqSim> tqsim(m, "TqSim", base_account);

  tqsim.def(py::init<double, const std::string&>(), py::arg("init_balance") = 10000000.0,
    py::arg("account_id") = std::string(), R"pbdoc( 
      天勤2模拟交易类.

        该类实现了一个本地的模拟账户，并且在内部完成撮合交易，在回测模式下，只能使用 TqSim 账户来交易。

      Args:
        init_balance (float): [可选]初始资金, 默认为 1000 万

        account_id (str):     [可选]帐号, 默认为 TQSIM

     )pbdoc");

  tqsim.def("set_margin", &TqSim::SetMargin, py::arg("symbol"), py::arg("margin"), R"pbdoc( 
      设置指定合约模拟交易的每手保证金。

      Args:
        symbol (str): 合约代码 (只支持期货合约)

        margin (float): 每手保证金

      Returns:
        float: 设置的每手保证金

      Example::

          from tqsdk2 import TqApi, TqAuth, TqSim
          sim = TqSim()
          api = TqApi(sim, auth=TqAuth("信易账户", "账户密码"))
          sim.set_margin("SHFE.cu2201", 26000)
          print(sim.get_margin("SHFE.cu2201"))
          api.close()

     )pbdoc");

  tqsim.def("get_margin", &TqSim::GetMargin, py::arg("symbol"), R"pbdoc( 
      获取指定合约模拟交易的每手保证金。

      Args:
        symbol (str): 合约代码 (只支持期货合约)

      Returns:
        float: 返回合约模拟交易的每手保证金

     )pbdoc");

  tqsim.def("set_commission", &TqSim::SetCommission, py::arg("symbol"), py::arg("commission"), R"pbdoc( 
      设置指定合约模拟交易的每手手续费。

      Args:
        symbol (str): 合约代码 (只支持期货合约)

        commission (float): 每手手续费

      Returns:
        float: 设置的每手手续费

      Example::

          from tqsdk2 import TqApi, TqAuth, TqSim
          sim = TqSim()
          api = TqApi(sim, auth=TqAuth("信易账户", "账户密码"))
          sim.set_commission("SHFE.cu2201", 50)
          print(sim.get_commission("SHFE.cu2201"))
          api.close()

     )pbdoc");

  tqsim.def("get_commission", &TqSim::GetCommission, py::arg("symbol"), R"pbdoc( 
      获取指定合约模拟交易的每手手续费。

      Args:
        symbol (str): 合约代码 (只支持期货合约)

      Returns:
        float: 返回合约模拟交易的每手手续费

     )pbdoc");

  /**
   * 直连 CTP 账户类
   */
  py::class_<TqCtp> tqctp(m, "TqCtp", base_account);

  tqctp.def(py::init<const std::string&, const std::string&, const std::string&, const std::string&, const std::string&,
              const std::string&, int>(),
    py::arg("td_url") = std::string(), py::arg("broker_id") = std::string(), py::arg("app_id") = std::string(),
    py::arg("auth_code") = std::string(), py::arg("user_name") = std::string(), py::arg("password") = std::string(),
    py::arg("default_trading_unit") = ktrading_unit_unset, R"pbdoc( 
      天勤2 实盘(直连CTP)账户类.

        创建天勤实盘(直连CTP)实例。

      Args:
        td_url (str):               [必填]CTP柜台地址.

        broker_id (str):            [必填]CTP交易前置的Broker ID, eg: 2020.

        app_id (str):               [必填]期货公司授权ID.

        auth_code (str):            [必填]期货公司授权码.

        user_name (str):            [必填]帐号.

        password (str):             [必填]密码.

        default_trading_unit (int): [可选] 默认交易单元, 如果指定该参数, 后续下单查询等操作均视为对该交易单元的操作.
     )pbdoc");

  /**
   * 融航资管账户类
   */
  py::class_<TqRohon> tqrohon(m, "TqRohon", base_account);
  tqrohon.def(py::init<const std::string&, const std::string&, const std::string&, const std::string&,
                const std::string&, const std::string&, int>(),
    py::arg("td_url") = std::string(), py::arg("broker_id") = std::string(), py::arg("app_id") = std::string(),
    py::arg("auth_code") = std::string(), py::arg("user_name") = std::string(), py::arg("password") = std::string(),
    py::arg("default_trading_unit") = ktrading_unit_unset, R"pbdoc( 
      天勤2 融航资管账户类.

        创建融航资管账户实例。

      Args:
        td_url (str):               [必填]CTP柜台地址.

        broker_id (str):            [必填]CTP交易前置的Broker ID, eg: 2020.

        app_id (str):               [必填]期货公司授权ID.

        auth_code (str):            [必填]期货公司授权码.

        user_name (str):            [必填]帐号.

        password (str):             [必填]密码.

        default_trading_unit (int): [可选] 默认交易单元, 如果指定该参数, 后续下单查询等操作均视为对该交易单元的操作.

      Example::

          # 登录融航资管
          from tqsdk2 import TqApi, TqAuth, TqRohon
          account = TqRohon(td_url="tcp://129.211.138.170:10001", broker_id="RohonDemo", app_id="融航模拟的appid", auth_code= "融航模拟authcode", user_name="融航模拟账户", password="融航模拟账户密码")
          api = TqApi(account = account, auth= TqAuth("信易账户","账户密码"))

     )pbdoc");

  py::class_<TqKqStock>(m, "TqKqStock", base_account)
    .def(py::init<int, const std::string&>(), py::arg("default_trading_unit") = ktrading_unit_unset,
      py::arg("_td_url") = std::string(), R"pbdoc( 
      天勤2 快期股票模拟交易类, 快期模拟账户与信易账户相匹配

      Args:
        default_trading_unit (int): [可选] 默认交易单元, 如果指定该参数, 后续下单查询等操作均视为对该交易单元的操作.
    )pbdoc");
}

}  // namespace TqSdk2
