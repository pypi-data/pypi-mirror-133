from __future__ import (absolute_import, division, print_function, unicode_literals)

from dataclasses import dataclass
import pandas as pd
import numpy
import talib
import math
import datetime as dt
from datetime import timezone
from . import config as cfg
from . import store
from . import portfolio as pt
from . import report as rp
from . import strategy
from . import utils

@dataclass(frozen=True)
class OHLCData:
	symbol: str
	files: list
	timestamp: int
	datetime: str
	open: float
	high: float
	low: float
	close: float
	volume: float
	timeframe: str
	compression: str = ""
	dtformat: str = "%Y-%m-%d %H:%M:%S"
	tsformat: str = "s"  # D,s,ms,us,ns
	separator: str = ","
	header: int = 0
	ascending: bool = True
	start_date: pd.Timestamp = None
	end_date: pd.Timestamp = None

@dataclass(frozen=True)
class Indicator:
	name: str
	tag: str
	timeframe: str
	period: int

class Backtrader:
	def __init__(self):
		self.__symbol = None
		self.__ohlc_timeframes = ["1m", "5m", "15m", "30m", "1h", "2h", "3h", "4h", "6h", "12h", "1D", "1W"]
		self.__ohlc_timeframe = None
		self.__start_cash = 0
		self.cfg = cfg.Config()
		self.store = store.Store()
		self.portfolio = pt.Portfolio()
		self.strategy = strategy.Strategy(self)

	def __get_indicator_values_fill_limit(self, timeframe: str, mins: int) -> int:
		if timeframe == "1m":
			return int(mins - 1)
		elif timeframe == "5m":
			return int((mins / 5) - 1)
		elif timeframe == "15m":
			return int((mins / 15) - 1)
		elif timeframe == "30m":
			return int((mins / 30) - 1)
		elif timeframe == "1h":
			return int((mins / 60) - 1)
		elif timeframe == "2h":
			return int((mins / 120) - 1)
		elif timeframe == "3h":
			return int((mins / 180) - 1)
		elif timeframe == "4h":
			return int((mins / 240) - 1)
		elif timeframe == "6h":
			return int((mins / 360) - 1)
		elif timeframe == "12h":
			return int((mins / 720) - 1)
		elif timeframe == "1D":
			return int((mins / 1440) - 1)
		elif timeframe == "1W":
			return int((mins / 10080) - 1)

	def __is_ohlc_nan(self, ohlc: tuple):
		if math.isnan(ohlc.open) or math.isnan(ohlc.high) or math.isnan(ohlc.low) or math.isnan(ohlc.close):
			return True

		return False

	def debug_mode(self, enabled: bool):
		self.cfg.debug = enabled

	def set_taker_fee_rate(self, percent: float):
		self.cfg.taker_fee_rate = percent / 100

	def set_cash(self, amount: float):
		self.__start_cash = amount
		self.portfolio.cash = amount

	def set_funding_rate(self, percent: float):
		self.cfg.funding_rate = percent / 100

	def set_funding_rate_interval(self, seconds: int):
		self.cfg.funding_rate_interval = seconds

	def add_ohlc_data(self, data: OHLCData):
		if data.timestamp == -1 and data.datetime == -1:
			raise Exception("Timestamp or datetime column is required.")

		self.__symbol = data.symbol
		usecols = []

		if data.datetime >= 0:
			usecols.append(data.datetime)
		else:
			usecols.append(data.timestamp)

		usecols = usecols + [data.open, data.high, data.low, data.close, data.volume]
		dfs = (pd.read_csv(f, sep=data.separator, header=data.header, usecols=usecols) for f in data.files)
		df = pd.concat(dfs, ignore_index=False)

		cols = {
			"open": data.open,
			"high": data.high,
			"low": data.low,
			"close": data.close,
			"volume": data.volume
		}

		if data.datetime >= 0:
			cols["datetime"] = data.datetime
		else:
			cols["timestamp"] = data.timestamp

		sorted_cols = sorted(cols.items(), key=lambda x: x[1], reverse=False)
		columns = {}

		for i, col in enumerate(sorted_cols):
			columns[df.columns[i]] = col[0]

		df = df.rename(columns=columns)

		if data.datetime >= 0:
			df["datetime"] = pd.to_datetime(df["datetime"], format=data.dtformat, utc=True)
		else:
			df["datetime"] = pd.to_datetime(df["timestamp"], unit=data.tsformat, utc=True)

		df = df.sort_values("datetime", ascending=data.ascending).set_index("datetime")

		if data.compression != "" and data.timeframe != data.compression:
			from_idx = self.__ohlc_timeframes.index(data.timeframe)
			to_idx = self.__ohlc_timeframes.index(data.compression)

			if to_idx > from_idx:
				df = utils.resample_ohlc_data(df, data.compression)
				self.__ohlc_timeframe = data.compression
			else:
				raise Exception(f"Timeframe compression from {data.timeframe} to {data.compression} is not possible.")
		else:
			self.__ohlc_timeframe = data.timeframe

		if data.start_date is not None:
			df = df[df.index >= pd.to_datetime(data.start_date, utc=True)]

		if data.end_date is not None:
			df = df[df.index <= pd.to_datetime(data.end_date, utc=True)]

		self.store.ohlc_data = df

	def set_strategy(self, strategy):
		self.store.clear_series_data()

		if self.store.ohlc_data is None or self.store.ohlc_data.empty:
			raise Exception("OHLC data is empty.")

		self.__strategy = strategy(self)
		series_data = self.store.ohlc_data

		if self.__strategy.indicators is not None and len(self.__strategy.indicators) > 0:
			for ind in self.__strategy.indicators:
				ind_tf_idx = self.__ohlc_timeframes.index(ind.timeframe)
				ohlc_tf_idx = self.__ohlc_timeframes.index(self.__ohlc_timeframe)

				if ohlc_tf_idx > ind_tf_idx:
					raise Exception(f"Indicator timeframe must be less than or equal OHLC data timeframe.")

				resampled = utils.resample_ohlc_data(self.store.ohlc_data, ind.timeframe)
				indexes = numpy.array(resampled.index.values)
				df = pd.DataFrame(index=indexes)

				if ind.name == "EMA":
					if len(resampled.close) < ind.period:
						raise Exception(f"OHLC data is not enough for period {ind.period}.")

					close = numpy.array(resampled.close, dtype=float)
					nans = numpy.isnan(close)
					df[ind.tag] = pd.Series(talib.EMA(close[~nans], timeperiod=ind.period), index=indexes[~nans])
				elif ind.name == "CCI":
					if len(resampled.close) < ind.period:
						raise Exception(f"OHLC data is not enough for period {ind.period}.")

					high = numpy.array(resampled.high, dtype=float)
					low = numpy.array(resampled.low, dtype=float)
					close = numpy.array(resampled.close, dtype=float)
					nans = numpy.isnan(close)

					df[ind.tag] = pd.Series(
						talib.CCI(
							high[~nans],
							low[~nans],
							close[~nans],
							timeperiod=ind.period
						),
						index=indexes[~nans]
					)
				elif ind.name == "ATR":
					if len(resampled.close) < ind.period + 1:
						raise Exception(f"OHLC data is not enough for period {ind.period}.")

					high = numpy.array(resampled.high, dtype=float)
					low = numpy.array(resampled.low, dtype=float)
					close = numpy.array(resampled.close, dtype=float)
					nans = numpy.isnan(close)

					df[ind.tag] = pd.Series(
						talib.ATR(
							high[~nans],
							low[~nans],
							close[~nans],
							timeperiod=ind.period
						),
						index=indexes[~nans]
					)

				delta = utils.get_timeframe_timedelta(ind.timeframe)
				df.index += delta
				df.index = df.index.tz_localize("UTC")
				series_data = pd.concat([series_data, df], ignore_index=False, axis=1)
				mins = int(delta.total_seconds() / 60)
				limit = self.__get_indicator_values_fill_limit(self.__ohlc_timeframe, mins)
				series_data[ind.tag] = series_data[ind.tag].fillna(method="ffill", limit=limit)

		self.store.series_data = series_data

	def run(self) -> rp.Report:
		self.store.clear_history()
		self.portfolio.cash = self.__start_cash
		self.portfolio.position = 0
		self.__strategy.position = None

		if self.portfolio.cash == 0:
			raise Exception("Insufficient funds.")

		if self.__strategy is None:
			raise Exception("Strategy is not set.")

		start = dt.datetime.now(timezone.utc)

		for row in self.store.series_data.itertuples():
			if self.__is_ohlc_nan(row):
				continue

			self.__strategy.last_series = row
			self.__strategy.handle_stop_loss()
			self.__strategy.handle_take_profit()
			self.__strategy.next()

			pos_size = 0

			if self.__strategy.position is not None:
				pos_size = self.__strategy.position.size

			self.portfolio.position = row.close * pos_size
			self.store.add_portfolio_history([row.Index, self.portfolio.cash, self.portfolio.position, self.portfolio.total])

		end = dt.datetime.now(timezone.utc)
		duration = end - start

		return rp.Report(
			symbol=self.__symbol,
			strategy=self.__strategy.name,
			start_cash=self.__start_cash,
			duration=duration,
			store=self.store,
			portfolio=self.portfolio
		)
