from __future__ import (absolute_import, division, print_function, unicode_literals)

from typing import Final, final
from dataclasses import dataclass
import pandas as pd
from . import utils

POSITION_SIDE_LONG: Final[str] = "LONG"
POSITION_SIDE_SHORT: Final[str] = "SHORT"
ORDER_SIDE_BUY: Final[str] = "BUY"
ORDER_SIDE_SELL: Final[str] = "SELL"
TRANSACTION_TYPE_REALIZED_PNL: Final[str] = "REALIZED_PNL"
TRANSACTION_TYPE_COMMISSION: Final[str] = "COMMISSION"

class Strategy:
	def __init__(self, ctx):
		self.ctx = ctx
		self.name = self.__class__.__name__
		self.indicators = None
		self.position = None
		self.last_series = None

	def __prepare_log_message(self, logs: list) -> str:
		msg = ""

		for item in logs:
			msg += " - " + item + "\n"

		return f"\n{msg}"

	def log(self, msg: str):
		if self.ctx.cfg.debug:
			ts = self.last_series.Index.strftime("%Y-%m-%d %H:%M:%S")
			print(f"{ts} {msg}")

	@final
	def handle_stop_loss(self):
		if self.position is not None:
			if self.position.stop_price > 0:
				logs = [f"Cash before {self.ctx.portfolio.cash:.2f}"]

				if self.position.side == POSITION_SIDE_LONG:
					if self.last_series.low <= self.position.stop_price:
						pnl = (self.position.stop_price - self.position.open_price) * self.position.size
						notional = self.position.stop_price * self.position.size
						fee = notional * self.ctx.cfg.taker_fee_rate
						margin = (self.position.open_price * self.position.size) * (1 / self.position.leverage)
						self.ctx.portfolio.add_cash(margin + pnl - fee)
						self.ctx.store.add_trade([self.last_series.Index, ORDER_SIDE_BUY, self.position.size, self.position.stop_price, notional, fee])
						self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_REALIZED_PNL, pnl, "USD"])
						self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_COMMISSION, fee * -1, "USD"])

						if self.indicators is not None:
							ind_values = {"datetime": self.last_series.Index}

							for col in self.ctx.store.series_data.columns[-len(self.indicators):]:
								ind_values[col] = getattr(self.last_series, col)

							self.ctx.store.add_indicators_history(ind_values)

						logs.append(f"Sold at {self.position.stop_price:.2f} with size {self.position.size:.8f}, notional {notional:.2f} and fee {fee:.2f} USD")
						logs.append(f"Closing {self.position.side} position by stop loss with size {self.position.size:.8f} and margin {margin:.2f}")
						logs.append(f"Realized PNL {pnl:.2f}")
						logs.append(f"Cash after {self.ctx.portfolio.cash:.2f}")
						self.position = None
						self.log(self.__prepare_log_message(logs))
				elif self.position.side == POSITION_SIDE_SHORT:
					if self.last_series.high >= self.position.stop_price:
						pnl = (self.position.open_price - self.position.stop_price) * self.position.size
						notional = self.position.stop_price * self.position.size
						fee = notional * self.ctx.cfg.taker_fee_rate
						margin = (self.position.open_price * self.position.size) * (1 / self.position.leverage)
						self.ctx.portfolio.add_cash(margin + pnl - fee)
						self.ctx.store.add_trade([self.last_series.Index, ORDER_SIDE_BUY, self.position.size, self.position.stop_price, notional, fee])
						self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_REALIZED_PNL, pnl, "USD"])
						self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_COMMISSION, fee * -1, "USD"])

						if self.indicators is not None:
							ind_values = {"datetime": self.last_series.Index}

							for col in self.ctx.store.series_data.columns[-len(self.indicators):]:
								ind_values[col] = getattr(self.last_series, col)

							self.ctx.store.add_indicators_history(ind_values)

						logs.append(f"Bought at {self.position.stop_price:.2f} with size {self.position.size:.8f}, notional {notional:.2f} and fee {fee:.2f} USD")
						logs.append(f"Closing {self.position.side} position by stop loss with size {self.position.size:.8f} and margin {margin:.2f}")
						logs.append(f"Realized PNL {pnl:.2f}")
						logs.append(f"Cash after {self.ctx.portfolio.cash:.2f}")
						self.position = None
						self.log(self.__prepare_log_message(logs))

	@final
	def handle_take_profit(self):
		if self.position is not None:
			if self.position.take_profit_price > 0:
				logs = [f"Cash before {self.ctx.portfolio.cash:.2f}"]

				if self.position.side == POSITION_SIDE_LONG:
					if self.last_series.high >= self.position.take_profit_price:
						pnl = (self.position.take_profit_price - self.position.open_price) * self.position.size
						notional = self.position.take_profit_price * self.position.size
						fee = notional * self.ctx.cfg.taker_fee_rate
						margin = (self.position.open_price * self.position.size) * (1 / self.position.leverage)
						self.ctx.portfolio.add_cash(margin + pnl - fee)
						self.ctx.store.add_trade([self.last_series.Index, ORDER_SIDE_BUY, self.position.size, self.position.take_profit_price, notional, fee])
						self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_REALIZED_PNL, pnl, "USD"])
						self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_COMMISSION, fee * -1, "USD"])

						if self.indicators is not None:
							ind_values = {"datetime": self.last_series.Index}

							for col in self.ctx.store.series_data.columns[-len(self.indicators):]:
								ind_values[col] = getattr(self.last_series, col)

							self.ctx.store.add_indicators_history(ind_values)

						logs.append(f"Sold at {self.position.take_profit_price:.2f} with size {self.position.size:.8f}, notional {notional:.2f} and fee {fee:.2f} USD")
						logs.append(f"Closing {self.position.side} position by take profit with size {self.position.size:.8f} and margin {margin:.2f}")
						logs.append(f"Realized PNL {pnl:.2f}")
						logs.append(f"Cash after {self.ctx.portfolio.cash:.2f}")
						self.position = None
						self.log(self.__prepare_log_message(logs))
				elif self.position.side == POSITION_SIDE_SHORT:
					if self.last_series.low <= self.position.take_profit_price:
						pnl = (self.position.open_price - self.position.take_profit_price) * self.position.size
						notional = self.position.take_profit_price * self.position.size
						fee = notional * self.ctx.cfg.taker_fee_rate
						margin = (self.position.open_price * self.position.size) * (1 / self.position.leverage)
						self.ctx.portfolio.add_cash(margin + pnl - fee)
						self.ctx.store.add_trade([self.last_series.Index, ORDER_SIDE_BUY, self.position.size, self.position.take_profit_price, notional, fee])
						self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_REALIZED_PNL, pnl, "USD"])
						self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_COMMISSION, fee * -1, "USD"])

						if self.indicators is not None:
							ind_values = {"datetime": self.last_series.Index}

							for col in self.ctx.store.series_data.columns[-len(self.indicators):]:
								ind_values[col] = getattr(self.last_series, col)

							self.ctx.store.add_indicators_history(ind_values)

						logs.append(f"Bought at {self.position.take_profit_price:.2f} with size {self.position.size:.8f}, notional {notional:.2f} and fee {fee:.2f} USD")
						logs.append(f"Closing {self.position.side} position by take profit with size {self.position.size:.8f} and margin {margin:.2f}")
						logs.append(f"Realized PNL {pnl:.2f}")
						logs.append(f"Cash after {self.ctx.portfolio.cash:.2f}")
						self.position = None
						self.log(self.__prepare_log_message(logs))

	@final
	def buy(self, size: float, leverage: int = 1, stop_price: float = 0, take_profit_price: float = 0, reduce_only: bool = False):
		if size == 0:
			raise Exception("Size must be greater zero.")

		logs = [f"Cash before {self.ctx.portfolio.cash:.2f}"]

		if reduce_only:
			if self.position is not None:
				if self.position.side != POSITION_SIDE_SHORT:
					raise Exception("Wrong side to reduce position.")

				pnl = (self.position.open_price - self.last_series.close) * size
				notional = self.last_series.close * size
				fee = notional * self.ctx.cfg.taker_fee_rate
				margin = (self.position.open_price * size) * (1 / self.position.leverage)
				self.ctx.portfolio.add_cash(margin + pnl - fee)
				self.ctx.store.add_trade([self.last_series.Index, ORDER_SIDE_BUY, size, self.last_series.close, notional, fee])
				self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_REALIZED_PNL, pnl, "USD"])
				self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_COMMISSION, fee * -1, "USD"])

				if self.indicators is not None:
					ind_values = {"datetime": self.last_series.Index}

					for col in self.ctx.store.series_data.columns[-len(self.indicators):]:
						ind_values[col] = getattr(self.last_series, col)

					self.ctx.store.add_indicators_history(ind_values)

				logs.append(f"Bought at {self.last_series.close:.2f} with size {size:.8f}, notional {notional:.2f} and fee {fee:.2f} USD")

				if self.position.size > size:
					self.position.size -= size
					self.position.update_at = self.last_series.Index
					new_margin = (self.position.open_price * self.position.size) * (1 / self.position.leverage)
					logs.append(f"Reducing {self.position.side} position by size {size:.8f} and margin {margin:.2f}")
					logs.append(f"Updated {self.position.side} position has size {self.position.size:.8f} and margin {new_margin:.2f}")
				else:
					logs.append(f"Closing {self.position.side} position with size {self.position.size:.8f} and margin {margin:.2f}")
					self.position = None

				logs.append(f"Realized PNL {pnl:.2f}")
				logs.append(f"Cash after {self.ctx.portfolio.cash:.2f}")
				self.log(self.__prepare_log_message(logs))
			else:
				raise Exception("No opened positions to reduce size.")
		else:
			notional = self.last_series.close * size
			fee = notional * self.ctx.cfg.taker_fee_rate

			if self.position is not None:
				if self.position.side != POSITION_SIDE_LONG:
					raise Exception("Wrong side for opened position.")

				if leverage != self.position.leverage:
					raise Exception("Wrong leverage for opened position.")

				req_margin = notional * (1 / self.position.leverage)

				if self.ctx.portfolio.cash < req_margin + fee:
					raise Exception("Insufficient funds.")

				old_notional = self.position.open_price * self.position.size
				new_open_price = (old_notional + notional) / (self.position.size + size)
				new_margin = (old_notional * (1 / self.position.leverage)) + req_margin
				self.position.stop_price = stop_price
				self.position.size += size
				self.position.update_at = self.last_series.Index
				self.position.open_price = new_open_price
				self.position.liquidation_price = utils.get_liquidation_price(POSITION_SIDE_LONG, self.position.leverage, self.position.open_price)
				self.ctx.portfolio.sub_cash(req_margin + fee)
				logs.append(f"Bought at {self.last_series.close:.2f} with size {size:.8f}, notional {notional:.2f} and fee {fee:.2f} USD")
				logs.append(f"Increasing {self.position.side} position by size {size:.8f} and margin {req_margin:.2f}")
				logs.append(f"Updated {self.position.side} position has size {self.position.size:.8f} and margin {new_margin:.2f}")
			else:
				margin = notional * (1 / leverage)

				if self.ctx.portfolio.cash < margin + fee:
					raise Exception("Insufficient funds.")

				self.position = self.Position(
					side=POSITION_SIDE_LONG,
					leverage=leverage,
					open_price=self.last_series.close,
					stop_price=stop_price,
					liquidation_price=utils.get_liquidation_price(POSITION_SIDE_LONG, leverage, self.last_series.close),
					size=size,
					created_at=self.last_series.Index,
					updated_at=self.last_series.Index
				)

				self.ctx.portfolio.sub_cash(margin + fee)
				logs.append(f"Bought at {self.last_series.close:.2f} with size {size:.8f}, notional {notional:.2f} and fee {fee:.2f} USD")
				logs.append(f"Opening {self.position.side} position with size {size:.8f} and margin {margin:.2f}")

			self.ctx.store.add_trade([self.last_series.Index, ORDER_SIDE_BUY, size, self.last_series.close, notional, fee])
			self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_COMMISSION, fee * -1, "USD"])

			if self.indicators is not None:
				ind_values = {"datetime": self.last_series.Index}

				for col in self.ctx.store.series_data.columns[-len(self.indicators):]:
					ind_values[col] = getattr(self.last_series, col)

				self.ctx.store.add_indicators_history(ind_values)

			logs.append(f"Cash after {self.ctx.portfolio.cash:.2f}")
			self.log(self.__prepare_log_message(logs))

	@final
	def sell(self, size: float, leverage: int = 1, stop_price: float = 0, take_profit_price: float = 0, reduce_only: bool = False):
		if size == 0:
			raise Exception("Size must be greater zero.")

		logs = [f"Cash before {self.ctx.portfolio.cash:.2f}"]

		if reduce_only:
			if self.position is not None:
				if self.position.side != POSITION_SIDE_LONG:
					raise Exception("Wrong side to reduce position.")

				pnl = (self.last_series.close - self.position.open_price) * size
				notional = self.last_series.close * size
				fee = notional * self.ctx.cfg.taker_fee_rate
				margin = (self.position.open_price * size) * (1 / self.position.leverage)
				self.ctx.portfolio.add_cash(margin + pnl - fee)
				self.ctx.store.add_trade([self.last_series.Index, ORDER_SIDE_BUY, size, self.last_series.close, notional, fee])
				self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_REALIZED_PNL, pnl, "USD"])
				self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_COMMISSION, fee * -1, "USD"])

				if self.indicators is not None:
					ind_values = {"datetime": self.last_series.Index}

					for col in self.ctx.store.series_data.columns[-len(self.indicators):]:
						ind_values[col] = getattr(self.last_series, col)

					self.ctx.store.add_indicators_history(ind_values)

				logs.append(f"Sold at {self.last_series.close:.2f} with size {size:.8f}, notional {notional:.2f} and fee {fee:.2f} USD")

				if self.position.size > size:
					self.position.size -= size
					self.position.update_at = self.last_series.Index
					new_margin = (self.position.open_price * self.position.size) * (1 / self.position.leverage)
					logs.append(f"Reducing {self.position.side} position by size {size:.8f} and margin {margin:.2f}")
					logs.append(f"Updated {self.position.side} position has size {self.position.size:.8f} and margin {new_margin:.2f}")
				else:
					logs.append(f"Closing {self.position.side} position with size {self.position.size:.8f} and margin {margin:.2f}")
					self.position = None

				logs.append(f"Realized PNL {pnl:.2f}")
				logs.append(f"Cash after {self.ctx.portfolio.cash:.2f}")
				self.log(self.__prepare_log_message(logs))
			else:
				raise Exception("No opened positions to reduce size.")
		else:
			notional = self.last_series.close * size
			fee = notional * self.ctx.cfg.taker_fee_rate

			if self.position is not None:
				if self.position.side != POSITION_SIDE_SHORT:
					raise Exception("Wrong side for opened position.")

				if leverage != self.position.leverage:
					raise Exception("Wrong leverage for opened position.")

				req_margin = notional * (1 / self.position.leverage)

				if self.ctx.portfolio.cash < req_margin + fee:
					raise Exception("Insufficient funds.")

				old_notional = self.position.open_price * self.position.size
				new_open_price = (old_notional + notional) / (self.position.size + size)
				new_margin = (old_notional * (1 / self.position.leverage)) + req_margin

				self.position.stop_price = stop_price
				self.position.size += size
				self.position.update_at = self.last_series.Index
				self.position.open_price = new_open_price
				self.position.liquidation_price = utils.get_liquidation_price(POSITION_SIDE_SHORT, self.position.leverage, self.position.open_price)
				self.ctx.portfolio.sub_cash(req_margin + fee)
				logs.append(f"Sold at {self.last_series.close:.2f} with size {size:.8f}, notional {notional:.2f} and fee {fee:.2f} USD")
				logs.append(f"Increasing {self.position.side} position by size {size:.8f} and margin {req_margin:.2f}")
				logs.append(f"Updated {self.position.side} position has size {self.position.size:.8f} and margin {new_margin:.2f}")
			else:
				margin = notional * (1 / leverage)

				if self.ctx.portfolio.cash < margin + fee:
					raise Exception("Insufficient funds.")

				self.position = self.Position(
					side=POSITION_SIDE_SHORT,
					leverage=leverage,
					open_price=self.last_series.close,
					stop_price=stop_price,
					liquidation_price=utils.get_liquidation_price(POSITION_SIDE_SHORT, leverage, self.last_series.close),
					size=size,
					created_at=self.last_series.Index,
					updated_at=self.last_series.Index
				)

				self.ctx.portfolio.sub_cash(margin + fee)
				logs.append(f"Sold at {self.last_series.close:.2f} with size {size:.8f}, notional {notional:.2f} and fee {fee:.2f} USD")
				logs.append(f"Opening {self.position.side} position with size {size:.8f} and margin {margin:.2f}")

			self.ctx.store.add_trade([self.last_series.Index, ORDER_SIDE_BUY, size, self.last_series.close, notional, fee])
			self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_COMMISSION, fee * -1, "USD"])

			if self.indicators is not None:
				ind_values = {"datetime": self.last_series.Index}

				for col in self.ctx.store.series_data.columns[-len(self.indicators):]:
					ind_values[col] = getattr(self.last_series, col)

				self.ctx.store.add_indicators_history(ind_values)

			logs.append(f"Cash after {self.ctx.portfolio.cash:.2f}")
			self.log(self.__prepare_log_message(logs))

	@final
	def close(self):
		if self.position is None:
			raise Exception("No opened positions to close.")

		logs = [f"Cash before {self.ctx.portfolio.cash:.2f}"]

		if self.position.side == POSITION_SIDE_LONG:
			pnl = (self.last_series.close - self.position.open_price) * self.position.size
			notional = self.last_series.close * self.position.size
			fee = notional * self.ctx.cfg.taker_fee_rate
			margin = (self.position.open_price * self.position.size) * (1 / self.position.leverage)
			self.ctx.portfolio.add_cash(margin + pnl - fee)
			self.ctx.store.add_trade([self.last_series.Index, ORDER_SIDE_BUY, self.position.size, self.last_series.close, notional, fee])
			self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_REALIZED_PNL, pnl, "USD"])
			self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_COMMISSION, fee * -1, "USD"])

			if self.indicators is not None:
				ind_values = {"datetime": self.last_series.Index}

				for col in self.ctx.store.series_data.columns[-len(self.indicators):]:
					ind_values[col] = getattr(self.last_series, col)

				self.ctx.store.add_indicators_history(ind_values)

			logs.append(f"Sold at {self.last_series.close:.2f} with size {self.position.size:.8f}, notional {notional:.2f} and fee {fee:.2f} USD")
			logs.append(f"Closing {self.position.side} position with size {self.position.size:.8f} and margin {margin:.2f}")
			logs.append(f"Realized PNL {pnl:.2f}")
			logs.append(f"Cash after {self.ctx.portfolio.cash:.2f}")
			self.position = None
			self.log(self.__prepare_log_message(logs))
		elif self.position.side == POSITION_SIDE_SHORT:
			pnl = (self.position.open_price - self.last_series.close) * self.position.size
			notional = self.last_series.close * self.position.size
			fee = notional * self.ctx.cfg.taker_fee_rate
			margin = (self.position.open_price * self.position.size) * (1 / self.position.leverage)
			self.ctx.portfolio.add_cash(margin + pnl - fee)
			self.ctx.store.add_trade([self.last_series.Index, ORDER_SIDE_BUY, self.position.size, self.last_series.close, notional, fee])
			self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_REALIZED_PNL, pnl, "USD"])
			self.ctx.store.add_ledger_record([self.last_series.Index, TRANSACTION_TYPE_COMMISSION, fee * -1, "USD"])

			if self.indicators is not None:
				ind_values = {"datetime": self.last_series.Index}

				for col in self.ctx.store.series_data.columns[-len(self.indicators):]:
					ind_values[col] = getattr(self.last_series, col)

				self.ctx.store.add_indicators_history(ind_values)

			logs.append(f"Bought at {self.last_series.close:.2f} with size {self.position.size:.8f}, notional {notional:.2f} and fee {fee:.2f} USD")
			logs.append(f"Closing {self.position.side} position with size {self.position.size:.8f} and margin {margin:.2f}")
			logs.append(f"Realized PNL {pnl:.2f}")
			logs.append(f"Cash after {self.ctx.portfolio.cash:.2f}")
			self.position = None
			self.log(self.__prepare_log_message(logs))

	def next(self):
		pass

	@dataclass
	class Position:
		side: str
		open_price: float
		liquidation_price: float
		size: float
		created_at: pd.Timestamp
		updated_at: pd.Timestamp
		leverage: int = 1
		stop_price: float = 0
		take_profit_price: float = 0
