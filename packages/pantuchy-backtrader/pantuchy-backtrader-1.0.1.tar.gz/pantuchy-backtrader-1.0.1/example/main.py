from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
sys.dont_write_bytecode = True

import backtrader as bt
import pandas as pd
import math

class BuyAndHold(bt.Strategy):
   def __init__(self, ctx):
      super().__init__(ctx)
      self.min_trade_notional = 100

   def next(self):
      if self.last_series.Index.weekday() == 0 and self.last_series.Index.hour == 0 and self.last_series.Index.minute == 0:
         if self.ctx.portfolio.cash < self.min_trade_notional:
            self.min_trade_notional = self.ctx.portfolio.cash

         fee = self.min_trade_notional * self.ctx.cfg.taker_fee_rate

         if self.ctx.portfolio.cash >= self.min_trade_notional + fee:
            size = self.min_trade_notional / self.last_series.close
            self.buy(size=size)

class MarginTrading(bt.Strategy):
	def __init__(self, ctx):
		super().__init__(ctx)

		self.indicators = [
			bt.Indicator(name="EMA", tag="ema_fast", timeframe="1D", period=8),
			bt.Indicator(name="EMA", tag="ema_slow", timeframe="1D", period=21)
		]

		self.min_trade_notional = 10
		self.max_balance_risk = 0.1
		self.max_leverage = 10

	def next(self):
		if math.isnan(self.last_series.ema_fast) or math.isnan(self.last_series.ema_slow):
			return

		if self.position is not None:
			if self.position.side == bt.POSITION_SIDE_LONG:
				if self.last_series.ema_fast < self.last_series.ema_slow:
					self.close()
			elif self.position.side == bt.POSITION_SIDE_SHORT:
				if self.last_series.ema_fast > self.last_series.ema_slow:
					self.close()
		else:
			notional = self.ctx.portfolio.cash * self.max_balance_risk

			if notional >= self.min_trade_notional:
				size = notional / self.last_series.close

				if self.last_series.ema_fast > self.last_series.ema_slow:
					self.buy(size=size)
				elif self.last_series.ema_fast < self.last_series.ema_slow:
					self.sell(size=size)

ohlc_data = bt.OHLCData(
	symbol="BTC/USD",
	files=[
		"/Users/pol.maksim/Google Drive/Мой диск/OHLC Data/bitfinex-BTC-USD-1m.csv"
	],
	timestamp=0,
	datetime=-1,
	open=1,
	high=3,
	low=4,
	close=2,
	volume=5,
	timeframe="1m",
	compression="5m",
	dtformat="%Y-%m-%d %H:%M:%S",
	tsformat="ms",
	separator=",",
	header=0,
	ascending=True,
	# start_date=pd.Timestamp(year=2017, month=1, day=1),
	# end_date=pd.Timestamp(year=2017, month=12, day=31)
)

b = bt.Backtrader()
b.set_taker_fee_rate(0.04)
b.set_funding_rate(0.01)
b.set_funding_rate_interval(28800)
b.add_ohlc_data(ohlc_data)
b.debug_mode(False)
b.set_cash(10000)
b.set_strategy(MarginTrading)

report = b.run()
report.info()
# report.portfolio_history.plot()
