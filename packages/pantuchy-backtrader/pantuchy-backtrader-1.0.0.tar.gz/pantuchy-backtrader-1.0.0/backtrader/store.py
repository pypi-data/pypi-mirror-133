from __future__ import (absolute_import, division, print_function, unicode_literals)
import pandas as pd

class Store:
	def __init__(self):
		self.__ohlc_data = None
		self.__series_data = None
		self.__portfolio_history = []
		self.__ledger_records = []
		self.__trades = []
		self.__indicators_history = []

	@property
	def ohlc_data(self) -> pd.DataFrame:
		return self.__ohlc_data

	@ohlc_data.setter
	def ohlc_data(self, data: pd.DataFrame):
		self.__ohlc_data = data

	@property
	def series_data(self) -> pd.DataFrame:
		return self.__series_data

	@series_data.setter
	def series_data(self, data: pd.DataFrame):
		self.__series_data = data

	def clear_series_data(self):
		self.__series_data = None

	@property
	def ledger_records(self) -> list:
		return self.__ledger_records

	def add_ledger_record(self, row: list):
		self.__ledger_records.append(row)

	@property
	def trades(self) -> list:
		return self.__trades

	def add_trade(self, row: list):
		self.__trades.append(row)

	@property
	def portfolio_history(self) -> list:
		return self.__portfolio_history

	def add_portfolio_history(self, row: list):
		if row[0].hour == 0 and row[0].minute == 0:
			self.__portfolio_history.append(row)

	@property
	def indicators_history(self) -> list:
		return self.__indicators_history

	def add_indicators_history(self, values: dict):
		self.__indicators_history.append(values)

	def clear_history(self):
		self.__portfolio_history = []
		self.__ledger_records = []
		self.__trades = []
		self.__indicators_history = []
