/*******************************************************************************
 * @file trading_unit.cpp
 * @brief 交易单元
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "trading_unit.h"

namespace TqSdk2 {

TradingUnit::TradingUnit() : m_default_unit_id(ktrading_unit_unset), m_db_file(std::string()) {}

void TradingUnit::EnableTradingUnit(int unit_id) {
  if (unit_id < 1 || unit_id > 99) {
    throw std::invalid_argument("交易单元指定错误, 交易单元仅支持 1 - 99 中的数字类型.");
  }
  m_default_unit_id = unit_id;

  fs::path trade_unit_path = exe_path() / ".tqsdk2/data";
  fs::create_directories(trade_unit_path);
  fs::path trade_unit_db_file = trade_unit_path / "trade_unit.db";
  m_db_file = trade_unit_db_file.string();
}

int TradingUnit::GetDefaultUnitID() {
  return m_default_unit_id;
}

bool TradingUnit::IsEnable() {
  return m_default_unit_id != ktrading_unit_unset;
}

std::string TradingUnit::GetTradeUnitPath() {
  return m_db_file;
}

}  // namespace TqSdk2