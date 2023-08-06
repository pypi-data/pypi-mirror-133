from __future__ import (absolute_import, division, print_function, unicode_literals)

class Config:
	def __init__(self):
		self.__debug = False
		self.__taker_fee_rate = 0.0005
		self.__funding_rate = 0.0001
		self.__funding_rate_interval = 28800

	@property
	def debug(self) -> bool:
		return self.__debug

	@debug.setter
	def debug(self, value: bool):
		self.__debug = value

	@property
	def taker_fee_rate(self) -> float:
		return self.__taker_fee_rate

	@taker_fee_rate.setter
	def taker_fee_rate(self, value: float):
		self.__taker_fee_rate = value

	@property
	def funding_rate(self) -> float:
		return self.__funding_rate

	@funding_rate.setter
	def funding_rate(self, value: float):
		self.__funding_rate = value

	@property
	def funding_rate_interval(self) -> int:
		return self.__funding_rate_interval

	@funding_rate_interval.setter
	def funding_rate_interval(self, value: int):
		self.__funding_rate_interval = value
