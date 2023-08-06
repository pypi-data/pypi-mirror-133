from __future__ import (absolute_import, division, print_function, unicode_literals)

import pandas as pd
from . import strategy

def resample_ohlc_data(data: pd.DataFrame, timeframe: str):
	if data.empty:
		raise Exception("OHLC data is empty.")

	item = {
		"open": "first",
		"high": "max",
		"low": "min",
		"close": "last",
		"volume": "sum"
	}

	if timeframe == "1m":
		return data
	elif timeframe == "5m":
		return data.resample("5Min").agg(item)
	elif timeframe == "15m":
		return data.resample("15Min").agg(item)
	elif timeframe == "30m":
		return data.resample("30Min").agg(item)
	elif timeframe == "1h":
		return data.resample("60Min").agg(item)
	elif timeframe == "2h":
		return data.resample("120Min").agg(item)
	elif timeframe == "3h":
		return data.resample("180Min").agg(item)
	elif timeframe == "4h":
		return data.resample("240Min").agg(item)
	elif timeframe == "6h":
		return data.resample("360Min").agg(item)
	elif timeframe == "12h":
		return data.resample("720Min").agg(item)
	elif timeframe == "1D":
		return data.resample("D").agg(item)
	elif timeframe == "1W":
		return data.resample("W-MON").agg(item)

	return data

def is_first_min_of_timeframe(ts: pd.Timestamp, timeframe: str):
	if timeframe == "1m":
		return True
	elif timeframe == "5m":
		if ts.minute in [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]:
			return True
	elif timeframe == "15m":
		if ts.minute in [0, 15, 30, 45]:
			return True
	elif timeframe == "30m":
		if ts.minute in [0, 30]:
			return True
	elif timeframe == "1h":
		if ts.minute == 0:
			return True
	elif timeframe == "2h":
		if ts.hour in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22] and ts.minute == 0:
			return True
	elif timeframe == "3h":
		if ts.hour in [0, 3, 6, 9, 12, 15, 18, 21] and ts.minute == 0:
			return True
	elif timeframe == "4h":
		if ts.hour in [0, 4, 8, 12, 16, 20] and ts.minute == 0:
			return True
	elif timeframe == "6h":
		if ts.hour in [0, 6, 12, 18] and ts.minute == 0:
			return True
	elif timeframe == "12h":
		if ts.hour in [0, 12] and ts.minute == 0:
			return True
	elif timeframe == "1D":
		if ts.hour == 0 and ts.minute == 0:
			return True
	elif timeframe == "1W":
		if ts.weekday() == 0 and ts.hour == 0 and ts.minute == 0:
			return True

	return False

def is_last_min_of_timeframe(ts: pd.Timestamp, timeframe: str):
	if timeframe == "1m":
		return True
	elif timeframe == "5m":
		if ts.minute in [4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59]:
			return True
	elif timeframe == "15m":
		if ts.minute in [14, 29, 44, 59]:
			return True
	elif timeframe == "30m":
		if ts.minute in [29, 59]:
			return True
	elif timeframe == "1h":
		if ts.minute == 59:
			return True
	elif timeframe == "2h":
		if ts.hour in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23] and ts.minute == 59:
			return True
	elif timeframe == "3h":
		if ts.hour in [2, 5, 8, 11, 14, 17, 20, 23] and ts.minute == 59:
			return True
	elif timeframe == "4h":
		if ts.hour in [3, 7, 11, 15, 19, 23] and ts.minute == 59:
			return True
	elif timeframe == "6h":
		if ts.hour in [5, 11, 17, 23] and ts.minute == 59:
			return True
	elif timeframe == "12h":
		if ts.hour in [11, 23] and ts.minute == 59:
			return True
	elif timeframe == "1D":
		if ts.hour == 23 and ts.minute == 59:
			return True
	elif timeframe == "1W":
		if ts.weekday() == 6 and ts.hour == 23 and ts.minute == 59:
			return True

	return False

def get_candle_open_timestamp(ts: pd.Timestamp, timeframe: str):
	n = 0

	if timeframe == "1m":
		n = ts.minute % 1
	elif timeframe == "5m":
		n = ts.minute % 5
	elif timeframe == "15m":
		n = ts.minute % 15
	elif timeframe == "30m":
		n = ts.minute % 30
	elif timeframe == "1h":
		n = ts.minute % 60
	elif timeframe == "2h":
		n = ((ts.hour % 2) * 60) + (ts.minute % 60)
	elif timeframe == "3h":
		n = ((ts.hour % 3) * 60) + (ts.minute % 60)
	elif timeframe == "4h":
		n = ((ts.hour % 4) * 60) + (ts.minute % 60)
	elif timeframe == "6h":
		n = ((ts.hour % 6) * 60) + (ts.minute % 60)
	elif timeframe == "12h":
		n = ((ts.hour % 12) * 60) + (ts.minute % 60)
	elif timeframe == "1D":
		n = ((ts.hour % 24) * 60) + (ts.minute % 60)
	elif timeframe == "1W":
		n = ((ts.weekday() % 7) * 1440) + ((ts.hour % 24) * 60) + (ts.minute % 60)

	return ts - pd.Timedelta(n, unit="m")

def get_prev_candle_open_timestamp(ts: pd.Timestamp, timeframe: str):
	n = get_candle_open_timestamp(ts, timeframe)

	if timeframe == "1m":
		return n - pd.Timedelta(60, unit="sec")
	elif timeframe == "5m":
		return n - pd.Timedelta(300, unit="sec")
	elif timeframe == "15m":
		return n - pd.Timedelta(900, unit="sec")
	elif timeframe == "30m":
		return n - pd.Timedelta(1800, unit="sec")
	elif timeframe == "1h":
		return n - pd.Timedelta(3600, unit="sec")
	elif timeframe == "2h":
		return n - pd.Timedelta(7200, unit="sec")
	elif timeframe == "3h":
		return n - pd.Timedelta(10800, unit="sec")
	elif timeframe == "4h":
		return n - pd.Timedelta(14400, unit="sec")
	elif timeframe == "6h":
		return n - pd.Timedelta(21600, unit="sec")
	elif timeframe == "12h":
		return n - pd.Timedelta(43200, unit="sec")
	elif timeframe == "1D":
		return n - pd.Timedelta(86400, unit="sec")
	elif timeframe == "1W":
		return n - pd.Timedelta(604800, unit="sec")

	return n

def get_timeframe_timedelta(timeframe: str):
	if timeframe == "1m":
		return pd.Timedelta(60, unit="sec")
	elif timeframe == "5m":
		return pd.Timedelta(300, unit="sec")
	elif timeframe == "15m":
		return pd.Timedelta(900, unit="sec")
	elif timeframe == "30m":
		return pd.Timedelta(1800, unit="sec")
	elif timeframe == "1h":
		return pd.Timedelta(3600, unit="sec")
	elif timeframe == "2h":
		return pd.Timedelta(7200, unit="sec")
	elif timeframe == "3h":
		return pd.Timedelta(10800, unit="sec")
	elif timeframe == "4h":
		return pd.Timedelta(14400, unit="sec")
	elif timeframe == "6h":
		return pd.Timedelta(21600, unit="sec")
	elif timeframe == "12h":
		return pd.Timedelta(43200, unit="sec")
	elif timeframe == "1D":
		return pd.Timedelta(86400, unit="sec")
	elif timeframe == "1W":
		return pd.Timedelta(604800, unit="sec")

def get_liquidation_price(side: str, leverage: int, open_price: float):
	if side == strategy.POSITION_SIDE_LONG:
		return (open_price * leverage) / (leverage + 1 - (0.01 * leverage))
	elif side == strategy.POSITION_SIDE_SHORT:
		return (open_price * leverage) / (leverage - 1 + (0.01 * leverage))

	return None

def get_optimal_leverage(side: str, open_price: float, stop_price: float, max_leverage: int = 1):
	max_liq_price = 0

	if side == strategy.POSITION_SIDE_LONG:
		max_liq_price = stop_price - (stop_price * 0.1)
	elif side == strategy.POSITION_SIDE_SHORT:
		max_liq_price = stop_price + (stop_price * 0.1)

	leverage = 1

	for i in range(max_leverage):
		liq_price = get_liquidation_price(side, i+1, open_price)

		if side == strategy.POSITION_SIDE_LONG:
			if liq_price < max_liq_price:
				leverage = i + 1
		elif side == strategy.POSITION_SIDE_SHORT:
			if liq_price > max_liq_price:
				leverage = i + 1

	return leverage
