/*******************************************************************************
 * @file filed_mapping.cpp
 * @brief tqsdk2 和 fclib 部分字段映射声明文件
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "field_mapping.h"

#include "utils/common.h"

namespace TqSdk2 {
FieldMapping<md::ProductClass> g_ins_class({
  {md::ProductClass::kFuture, ("FUTURE")},
  {md::ProductClass::kCont, ("CONT")},
  {md::ProductClass::kOption, ("OPTION")},
  {md::ProductClass::kCombine, ("COMBINE")},
  {md::ProductClass::kIndex, ("INDEX")},
  {md::ProductClass::kSpot, ("SPOT")},
  {md::ProductClass::kStock, ("STOCK")},
  {md::ProductClass::kBond, ("BOND")},
  {md::ProductClass::kFund, ("FUND")},
});

FieldMapping<future::PriceType> g_price_type({
  {future::PriceType::kLimit, ("LIMIT")},
  {future::PriceType::kAny, ("ANY")},
  {future::PriceType::kBest, ("BEST")},
  {future::PriceType::kFiveLevel, ("FIVELEVEL")},
  {future::PriceType::kInvalid, ("INVALID")},
});

FieldMapping<future::OrderVolumeCondition> g_order_volume_condition({
  {future::OrderVolumeCondition::kAny, "ANY"},
  {future::OrderVolumeCondition::kMin, "MIN"},
  {future::OrderVolumeCondition::kAll, "ALL"},
  {future::OrderVolumeCondition::kInvalid, "INVALID"},
});

FieldMapping<future::OrderTimeCondition> g_order_time_condition({
  {future::OrderTimeCondition::kIoc, "IOC"},
  {future::OrderTimeCondition::kGfs, "GFS"},
  {future::OrderTimeCondition::kGfd, "GFD"},
  {future::OrderTimeCondition::kGtd, "GTD"},
  {future::OrderTimeCondition::kGtc, "GTC"},
  {future::OrderTimeCondition::kGfa, "GFA"},
  {future::OrderTimeCondition::kInvalid, "INVALID"},
});

FieldMapping<future::OrderStatus> g_order_status({
  {future::OrderStatus::kAlive, ("ALIVE")},
  {future::OrderStatus::kDead, ("FINISHED")},
});

FieldMapping<future::Direction> g_direction_mapping({
  {future::Direction::kBuy, "BUY"},
  {future::Direction::kSell, "SELL"},
  {future::Direction::kInvalid, "INVALID"},
});

FieldMapping<future::Offset> g_offset_mapping({
  {future::Offset::kOpen, ("OPEN")},
  {future::Offset::kClose, ("CLOSE")},
  {future::Offset::kCloseToday, ("CLOSETODAY")},
  {future::Offset::kOpenAndClose, ("OPENANDCLOSE")},
  {future::Offset::kCloseAndOpen, ("CLOSEANDOPEN")},
  {future::Offset::kInvalid, ("INVALID")},
});

FieldMapping<md::OptionClass> g_option_class_mapping({
  {md::OptionClass::kCall, ("CALL")},
  {md::OptionClass::kPut, ("PUT")},
});

FieldMapping<md::OptionExerciseType> g_option_exe_class_mapping({
  {md::OptionExerciseType::kAmerican, ("A")},
  {md::OptionExerciseType::kEurope, ("E")},
});

std::map<future::Direction, const char*>& DefineEnum(FieldSerializer* ss, const Direction& c) {
  static std::map<future::Direction, const char*> MAP = g_direction_mapping.get();
  return MAP;
}

std::map<future::Offset, const char*>& DefineEnum(FieldSerializer* ss, const future::Offset& o) {
  static std::map<future::Offset, const char*> MAP = g_offset_mapping.get();
  return MAP;
}

std::map<md::ProductClass, const char*>& DefineEnum(FieldSerializer* ss, const md::ProductClass& p) {
  static std::map<md::ProductClass, const char*> MAP = g_ins_class.get();
  return MAP;
}

std::map<md::OptionClass, const char*>& DefineEnum(FieldSerializer* ss, const md::OptionClass& o) {
  static std::map<md::OptionClass, const char*> MAP = g_option_class_mapping.get();
  return MAP;
}

std::map<md::OptionExerciseType, const char*>& DefineEnum(FieldSerializer* ss, const md::OptionExerciseType& o) {
  static std::map<md::OptionExerciseType, const char*> MAP = g_option_exe_class_mapping.get();
  return MAP;
}

std::map<future::PriceType, const char*>& DefineEnum(FieldSerializer* ss, const future::PriceType& p) {
  static std::map<future::PriceType, const char*> MAP = g_price_type.get();
  return MAP;
}

std::map<future::OrderVolumeCondition, const char*>& DefineEnum(
  FieldSerializer* ss, const future::OrderVolumeCondition& p) {
  static std::map<future::OrderVolumeCondition, const char*> MAP = g_order_volume_condition.get();
  return MAP;
}

std::map<future::OrderTimeCondition, const char*>& DefineEnum(
  FieldSerializer* ss, const future::OrderTimeCondition& o) {
  static std::map<future::OrderTimeCondition, const char*> MAP = g_order_time_condition.get();
  return MAP;
}

std::map<future::OrderStatus, const char*>& DefineEnum(FieldSerializer* ss, const future::OrderStatus& o) {
  static std::map<future::OrderStatus, const char*> MAP = g_order_status.get();
  return MAP;
}

void FieldSerializer::DefineStruct(md::Instrument& d) {
  std::string dt = EpochNanoToHumanTime(d.exchange_time);
  AddItem(dt, "datetime");
  AddItem(d.ask_price[0], "ask_price1");
  AddItem(d.ask_volume[0], "ask_volume1");
  AddItem(d.bid_price[0], "bid_price1");
  AddItem(d.bid_volume[0], "bid_volume1");
  AddItem(d.ask_price[1], "ask_price2");
  AddItem(d.ask_volume[1], "ask_volume2");
  AddItem(d.bid_price[1], "bid_price2");
  AddItem(d.bid_volume[1], "bid_volume2");
  AddItem(d.ask_price[2], "ask_price3");
  AddItem(d.ask_volume[2], "ask_volume3");
  AddItem(d.bid_price[2], "bid_price3");
  AddItem(d.bid_volume[2], "bid_volume3");
  AddItem(d.ask_price[3], "ask_price4");
  AddItem(d.ask_volume[3], "ask_volume4");
  AddItem(d.bid_price[3], "bid_price4");
  AddItem(d.bid_volume[3], "bid_volume4");
  AddItem(d.ask_price[4], "ask_price5");
  AddItem(d.ask_volume[4], "ask_volume5");
  AddItem(d.bid_price[4], "bid_price5");
  AddItem(d.bid_volume[4], "bid_volume5");
  AddItem(d.last_price, "last_price");
  AddItem(d.highest, "highest");
  AddItem(d.lowest, "lowest");
  AddItem(d.open, "open");
  AddItem(d.close, "close");
  AddItem(d.average, "average");
  AddItem(d.volume, "volume");
  AddItem(d.amount, "amount");
  AddItem(d.open_interest, "open_interest");
  AddItem(d.settlement, "settlement");
  AddItem(d.upper_limit, "upper_limit");
  AddItem(d.lower_limit, "lower_limit");
  AddItem(d.pre_open_interest, "pre_open_interest");
  AddItem(d.pre_settlement, "pre_settlement");
  AddItem(d.pre_close, "pre_close");
  AddItem(d.price_tick, "price_tick");
  AddItem(d.price_decs, "price_decs");
  AddItem(d.volume_multiple, "volume_multiple");
  AddItem(d.max_limit_order_volume, "max_limit_order_volume");
  AddItem(d.max_market_order_volume, "max_market_order_volume");
  std::string underlying_symbol =
    d.underlying_pointer.node && d.underlying_pointer.node->Snap() ? d.underlying_pointer.node->Snap()->symbol : "";
  AddItem(underlying_symbol, "underlying_symbol");
  AddItem(d.strike_price, "strike_price");
  AddItem(d.product_class, "ins_class");
  AddItem(d.instrument_id, "instrument_id");
  AddItem(d.instrument_name, "instrument_name");
  AddItem(d.exchange_id, "exchange_id");
  AddItem(d.expired, "expired");
  double expire_datetime = d.expire_datetime / 1e9;
  AddItem(expire_datetime, "expire_datetime");
  AddItem(d.delivery_year, "delivery_year");
  AddItem(d.delivery_month, "delivery_month");
  double last_exercise_datetime = d.last_exercise_day / 1e9;
  AddItem(last_exercise_datetime, "last_exercise_datetime");
  if (d.option_class == md::OptionClass::kCall || d.option_class == md::OptionClass::kPut) {
    AddItem(d.option_class, "option_class");
  }
  if (d.exercise_type == md::OptionExerciseType::kAmerican || d.exercise_type == md::OptionExerciseType::kEurope) {
    AddItem(d.exercise_type, "exercise_type");
  }
  AddItem(d.product_id, "product_id");
  AddItem(d.margin, "margin");
  AddItem(d.commission, "commission");
}

void FieldSerializer::DefineStruct(future::Account& d) {
  AddItem(d.currency, "currency");
  AddItem(d.pre_balance, "pre_balance");
  AddItem(d.balance, "balance");
  AddItem(d.available, "available");
  AddItem(d.float_profit, "float_profit");
  AddItem(d.position_profit, "position_profit");
  AddItem(d.close_profit, "close_profit");
  AddItem(d.frozen_margin, "frozen_margin");
  AddItem(d.margin, "margin");
  AddItem(d.frozen_commission, "frozen_commission");
  AddItem(d.commission, "commission");
  AddItem(d.frozen_premium, "frozen_premium");
  AddItem(d.premium, "premium");
  AddItem(d.deposit, "deposit");
  AddItem(d.withdraw, "withdraw");
  AddItem(d.risk_ratio, "risk_ratio");
  AddItem(d.option_market_value, "market_value");
}

void FieldSerializer::DefineStruct(future::Position& d) {
  AddItem(d.exchange_id, "exchange_id");
  AddItem(d.instrument_id, "instrument_id");
  AddItem(d.subpos_long_spec.volume_his, "pos_long_his");
  AddItem(d.subpos_long_spec.volume_today, "pos_long_today");
  AddItem(d.subpos_short_spec.volume_his, "pos_short_his");
  AddItem(d.subpos_short_spec.volume_today, "pos_short_today");
  AddItem(d.subpos_long_spec.volume_today, "volume_long_today");
  AddItem(d.subpos_long_spec.volume_his, "volume_long_his");
  int32_t volume_long = d.volume_long();
  AddItem(volume_long, "volume_long");
  AddItem(d.subpos_long_spec.volume_today_frozen, "volume_long_frozen_today");
  AddItem(d.subpos_long_spec.volume_his_frozen, "volume_long_frozen_his");
  int32_t volume_long_frozen = d.subpos_long_spec.volume_today_frozen + d.subpos_long_spec.volume_his_frozen;
  AddItem(volume_long_frozen, "volume_long_frozen");
  AddItem(d.subpos_short_spec.volume_today, "volume_short_today");
  AddItem(d.subpos_short_spec.volume_his, "volume_short_his");
  int32_t volume_short = d.subpos_short_spec.volume_today + d.subpos_short_spec.volume_his;
  AddItem(volume_short, "volume_short");
  AddItem(d.subpos_short_spec.volume_today_frozen, "volume_short_frozen_today");
  AddItem(d.subpos_short_spec.volume_his_frozen, "volume_short_frozen_his");
  int32_t volume_short_frozen = d.subpos_short_spec.volume_his_frozen + d.subpos_short_spec.volume_today_frozen;
  AddItem(volume_short_frozen, "volume_short_frozen");
  AddItem(d.subpos_long_spec.open_price, "open_price_long");
  AddItem(d.subpos_short_spec.open_price, "open_price_short");
  AddItem(d.subpos_long_spec._open_cost, "open_cost_long");
  AddItem(d.subpos_short_spec._open_cost, "open_cost_short");
  AddItem(d.subpos_long_spec.position_price, "position_price_long");
  AddItem(d.subpos_short_spec.position_price, "position_price_short");
  AddItem(d.subpos_long_spec._position_cost, "position_cost_long");
  AddItem(d.subpos_short_spec._position_cost, "position_cost_short");
  AddItem(d.subpos_long_spec.float_profit, "float_profit_long");
  AddItem(d.subpos_short_spec.float_profit, "float_profit_short");
  double float_profit = d.float_profit();
  AddItem(float_profit, "float_profit");
  AddItem(d.subpos_long_spec.position_profit, "position_profit_long");
  AddItem(d.subpos_short_spec.position_profit, "position_profit_short");
  double position_profit = d.position_profit();
  AddItem(position_profit, "position_profit");
  AddItem(d.subpos_long_spec.margin, "margin_long");
  AddItem(d.subpos_short_spec.margin, "margin_short");
  double margin = d.margin();
  AddItem(margin, "margin");
  AddItem(d.subpos_long_spec.market_value, "market_value_long");
  AddItem(d.subpos_short_spec.market_value, "market_value_short");
  int32_t pos = d.volume_net();
  AddItem(pos, "pos");
  int32_t pos_long = d.volume_long();
  AddItem(pos_long, "pos_long");
  int32_t pos_short = d.volume_short();
  AddItem(pos_short, "pos_short");
  AddItem(d.last_price, "last_price");
  AddItem(d.unit_id, "unit_id");
}

void FieldSerializer::DefineStruct(future::Order& d) {
  AddItem(d.order_id, "order_id");
  AddItem(d.exchange_order_id, "exchange_order_id");
  AddItem(d.exchange_id, "exchange_id");
  AddItem(d.instrument_id, "instrument_id");
  AddItem(d.direction, "direction");
  AddItem(d.offset, "offset");
  AddItem(d.volume_orign, "volume_orign");
  AddItem(d.volume_left, "volume_left");
  AddItem(d.limit_price, "limit_price");
  AddItem(d.price_type, "price_type");
  AddItem(d.volume_condition, "volume_condition");
  AddItem(d.time_condition, "time_condition");
  AddItem(d.insert_date_time, "insert_date_time");
  AddItem(d.status_msg, "last_msg");
  AddItem(d.status, "status");
  AddItem(d.user_id, "user_id");
  // TODO 需要 fclib 补充该字段
  // AddItem(d.frozen_margin, "frozen_margin");
  // AddItem(d.frozen_premium, "frozen_premium");
  AddItem(d.unit_id, "unit_id");
}

void FieldSerializer::DefineStruct(future::Trade& d) {
  auto trade_id = d.exchange_trade_id + "|" + d.order_id;
  AddItem(trade_id, "trade_id");
  AddItem(d.order_id, "order_id");
  AddItem(d.exchange_trade_id, "exchange_trade_id");
  AddItem(d.exchange_id, "exchange_id");
  AddItem(d.instrument_id, "instrument_id");
  AddItem(d.direction, "direction");
  AddItem(d.offset, "offset");
  AddItem(d.price, "price");
  AddItem(d.volume, "volume");
  AddItem(d.trade_date_time, "trade_date_time");
  AddItem(d.user_id, "user_id");
  AddItem(d.commission, "commission");
}

void FieldSerializer::DefineStruct(security::Account& d) {
  AddItem(d.user_id, "user_id");
  AddItem("CNY", "currency");
  AddItem(d.available, "available");
  AddItem(d.available_his, "available_his");
  AddItem(d.buy_frozen_balance, "buy_frozen_balance");
  AddItem(d.buy_frozen_fee, "buy_frozen_fee");
  AddItem(d.buy_balance_today, "buy_balance_today");
  AddItem(d.buy_fee_today, "buy_fee_today");
  AddItem(d.sell_balance_today, "sell_balance_today");
  AddItem(d.sell_fee_today, "sell_fee_today");
  AddItem(d.deposit, "deposit");
  AddItem(d.withdraw, "withdraw");
  AddItem(d.drawable, "drawable");
  AddItem(d.market_value, "market_value");
  AddItem(d.asset, "asset");
  AddItem(d.asset_his, "asset_his");
  AddItem(d.dividend_balance_today, "dividend_balance_today");
  AddItem(d.cost, "cost");
  AddItem(d.hold_profit, "hold_profit");
  AddItem(d.float_profit_today, "float_profit_today");
  AddItem(d.real_profit_today, "real_profit_today");
  AddItem(d.profit_today, "profit_today");
  AddItem(d.profit_rate_today, "profit_rate_today");
}

void FieldSerializer::DefineStruct(security::Position& d) {
  AddItem(d.user_id, "user_id");
  AddItem(d.exchange_id, "exchange_id");
  AddItem(d.instrument_id, "instrument_id");
  AddItem(d.create_date, "create_date");
  AddItem(d.volume, "volume");
  AddItem(d.last_price, "last_price");
  AddItem(d.buy_volume_today, "buy_volume_today");
  AddItem(d.buy_balance_today, "buy_balance_today");
  AddItem(d.buy_fee_today, "buy_fee_today");
  AddItem(d.sell_volume_today, "sell_volume_today");
  AddItem(d.sell_balance_today, "sell_balance_today");
  AddItem(d.sell_fee_today, "sell_fee_today");
  AddItem(d.shared_volume_today, "shared_volume_today");
  AddItem(d.devidend_balance_today, "devidend_balance_today");
  AddItem(d.cost, "cost");
  AddItem(d.market_value, "market_value");
  AddItem(d.float_profit_today, "float_profit_today");
  AddItem(d.real_profit_today, "real_profit_today");
  AddItem(d.profit_today, "profit_today");
  AddItem(d.profit_rate_today, "profit_rate_today");
  AddItem(d.hold_profit, "hold_profit");
  AddItem(d.real_profit_total, "real_profit_total");
  AddItem(d.profit_total, "profit_total");
  AddItem(d.profit_rate_total, "profit_rate_total");
}

void FieldSerializer::DefineStruct(security::Order& d) {
  AddItem(d.user_id, "user_id");
  AddItem(d.exchange_id, "exchange_id");
  AddItem(d.instrument_id, "instrument_id");
  AddItem(d.order_id, "order_id");
  AddItem(d.volume_orign, "volume_orign");
  AddItem(d.volume_left, "volume_left");
  AddItem(d.limit_price, "limit_price");
  AddItem(d.insert_date_time, "insert_date_time");
  AddItem(d.status_msg, "status_msg");
  AddItemEnum(d.direction, ("direction"),
    {
      {security::Direction::kBuy, ("BUY")},
      {security::Direction::kSell, ("SELL")},
    });
  AddItemEnum(d.price_type, ("price_type"),
    {
      {security::PriceType::kLimit, ("LIMIT")},
      {security::PriceType::kAny, ("ANY")},
    });
  AddItemEnum(d.status, ("status"),
    {
      {security::OrderStatus::kAlive, ("ALIVE")},
      {security::OrderStatus::kDead, ("FINISHED")},
    });
}

void FieldSerializer::DefineStruct(security::Trade& d) {
  AddItem(d.user_id, "user_id");
  AddItem(d.exchange_id, "exchange_id");
  AddItem(d.instrument_id, "instrument_id");
  AddItem(d.trade_id, "trade_id");
  AddItem(d.order_id, "order_id");
  AddItem(d.exchange_trade_id, "exchange_trade_id");
  AddItem(d.price, "price");
  AddItem(d.volume, "volume");
  // AddItem(d.balance(), "balance");
  AddItem(d.fee, "fee");
  AddItemEnum(d.direction, ("direction"),
    {
      {security::Direction::kBuy, ("BUY")},
      {security::Direction::kSell, ("SELL")},
    });
  AddItem(d.trade_date_time, "trade_date_time");
}
}  // namespace TqSdk2
