from __future__ import (absolute_import, division, print_function, unicode_literals)

class Portfolio:
	def __init__(self):
		self.__cash = 0
		self.__position = 0

	@property
	def cash(self) -> float:
		return self.__cash

	@cash.setter
	def cash(self, amount: float):
		self.__cash = amount

	def add_cash(self, amount: float):
		self.__cash += amount

	def sub_cash(self, amount: float):
		self.__cash -= amount

	@property
	def position(self) -> float:
		return self.__position

	@position.setter
	def position(self, amount: float):
		self.__position = amount

	@property
	def total(self) -> float:
		return self.__cash + self.__position
