from __future__ import (absolute_import, division, print_function, unicode_literals)

import time
import datetime as dt
import pandas as pd
from . import store
from . import portfolio as pt
from bokeh.plotting import figure, show, ColumnDataSource, output_file
from bokeh.io import output_notebook
from bokeh.models import NumeralTickFormatter, DatetimeTickFormatter, HoverTool, CrosshairTool
from tabulate import tabulate
from . import strategy

class Report(object):
	def __init__(self, symbol: str, strategy: str, start_cash: float, duration: dt.timedelta, store: store.Store, portfolio: pt.Portfolio):
		self.__symbol = symbol
		self.__strategy = strategy
		self.__start_cash = start_cash
		self.__duration = duration
		self.__store = store
		self.__portfolio = portfolio

		ph = pd.DataFrame(
			store.portfolio_history,
			columns=["datetime", "cash", "position", "total"]
		).set_index("datetime").fillna(method="ffill").round({"cash": 2, "position": 2, "total": 2})

		ph["total_diff"] = ph.total.diff()
		p_change = ph.total.pct_change()
		wealth_index = len(ph.total.index) * (1 + p_change).cumprod()

		dr = pd.DataFrame()
		dr["prev_peaks"] = wealth_index.cummax()
		dr["values"] = (wealth_index - dr["prev_peaks"]) / dr["prev_peaks"]
		ph["drawdown"] = dr["values"]
		dr = dr.reset_index().groupby("prev_peaks")["datetime"].agg(["min", "max"])
		dr["duration"] = dr['max'].sub(dr['min'])

		self.__drawdowns = dr[dr["duration"] > pd.Timedelta(days=0)]
		self.__portfolio_history = self.PortfolioHistory(is_notebook=self.__is_notebook, data=ph)

		self.__ledger_records = pd.DataFrame(
			self.__store.ledger_records,
			columns=["datetime", "type", "amount", "asset"]
		).round({"amount": 2})

		self.__trades = pd.DataFrame(
			self.__store.trades,
			columns=["datetime", "side", "amount", "price", "notional", "fee"]
		).round({"amount": 2, "price": 2, "notional": 2, "fee": 2})

	def __is_notebook(self) -> bool:
		try:
			from IPython import get_ipython

			if "IPKernelApp" not in get_ipython().config:
				return False
		except ImportError:
			return False
		except AttributeError:
			return False

		return True

	def __get_win_loss_ratio(self) -> tuple[float, float]:
		pnls = self.__ledger_records.loc[self.__ledger_records["type"] == strategy.TRANSACTION_TYPE_REALIZED_PNL]

		win_qty = len(pnls.loc[pnls["amount"] > 0].index)
		loss_qty = len(pnls.loc[pnls["amount"] < 0].index)
		win_ratio = 0
		loss_ratio = 0

		if len(pnls.index) > 0:
			win_ratio = round(win_qty / len(pnls.index) * 100, 1)
			loss_ratio = round(loss_qty / len(pnls.index) * 100, 1)

		return win_ratio, loss_ratio

	@property
	def portfolio_history(self):
		return self.__portfolio_history

	def info(self):
		first = self.__store.ohlc_data.iloc[0]
		last = self.__store.ohlc_data.iloc[-1]
		profit_amount = self.__portfolio.total - self.__start_cash
		win_ratio, loss_ratio = self.__get_win_loss_ratio()
		max_drawdown = abs(self.portfolio_history.data.drawdown.min() * 100)
		max_drawdown_idx = self.__drawdowns.set_index("max").duration.idxmax()

		table = [
			["Symbol", self.__symbol],
			["Start Date", f"{first.name.strftime('%d-%m-%Y')} ({int(time.mktime(first.name.timetuple()))})"],
			["End Date", f"{last.name.strftime('%d-%m-%Y')} ({int(time.mktime(last.name.timetuple()))})"],
			["Strategy", self.__strategy],
			["Cash (start / end)", f"{self.__start_cash:.2f} / {self.__portfolio.cash:.2f}"],
			["Position (start / end)", f"{0:.2f} / {self.__portfolio.position:.2f}"],
			["Total Portfolio (start / end)", f"{self.__start_cash:.2f} / {self.__portfolio.total:.2f}"],
			["Total Portfolio (min / max)", f"{self.portfolio_history.data.total.min():.2f} / {self.portfolio_history.data.total.max():.2f}"],
			["Profit", f"{profit_amount:.2f} ({(profit_amount / self.__start_cash) * 100:.2f}%)"],
			["Avg. Daily Profit [%]", f"{self.portfolio_history.data.pct_change(periods=1).total.mean() * 100:.2f}%"],
			["Avg. Monthly Profit [%]", f"{self.portfolio_history.data.pct_change(periods=30).total.mean() * 100:.2f}%"],
			["Avg. Annual Profit [%]", f"{self.portfolio_history.data.pct_change(periods=365).total.mean() * 100:.2f}%"],
			["Total Trades Qty", len(self.__trades.index)],
			["Win / Loss Ratio", f"{win_ratio:.1f}% / {loss_ratio:.1f}%"],
			["Max. Drawdown", f"{self.portfolio_history.data.loc[max_drawdown_idx].total:.2f} ({max_drawdown:.2f}%)"],
			["Drawdown Duration (avg / max)", f"{self.__drawdowns.duration.mean().days} days / {self.__drawdowns.duration.max().days} days"],
			["Duration", self.__duration]
		]

		print(tabulate(table, colalign=("left", "right"), tablefmt="psql"))

	@property
	def ledger_records(self):
		return self.__ledger_records

	@property
	def trades(self):
		return self.__trades

	class PortfolioHistory(object):
		def __init__(self, is_notebook: bool, data: pd.DataFrame):
			self.__is_notebook = is_notebook
			self.__data = data

		@property
		def data(self):
			return self.__data

		def plot(self):
			if self.__is_notebook:
				output_notebook()
			else:
				output_file("portfolio-history.html")

			source = ColumnDataSource(data=self.__data.reset_index())
			tools = "pan, wheel_zoom, reset, save"

			p = figure(
				width=1000,
				height=500,
				tools=tools,
				title="Portfolio History",
				x_axis_label="Date",
				y_axis_label="Amount",
				x_axis_type="datetime",
				active_scroll="wheel_zoom",
				toolbar_location="above"
			)

			p.sizing_mode = "scale_both"

			hover = HoverTool(
				tooltips=[
					("Date", "@datetime{%Y-%m-%d}"),
					("Total", "@total{%0.2f}"),
					("Cash", "@cash{%0.2f}"),
					("Position", "@position{%0.2f}")
				],
				formatters={
					"@datetime": "datetime",
					"@total": "printf",
					"@cash": "printf",
					"@position": "printf"
				},
				mode="vline",
				show_arrow=False,
				line_policy="none"
			)

			p.add_tools(hover)

			cross = CrosshairTool()
			cross.line_color = "grey"
			cross.line_alpha = 0.5
			p.add_tools(cross)

			p.line("datetime", "position", source=source, legend_label="Position", line_width=1, line_color="orange")
			p.line("datetime", "cash", source=source, legend_label="Cash", line_width=1, line_color="red")
			p.line("datetime", "total", source=source, legend_label="Total", line_width=1, line_color="green")

			p.legend.location = "top_left"
			p.xaxis[0].formatter = DatetimeTickFormatter(years="%Y", months="%Y-%m", days="%Y-%m-%d", hours="%Y-%m-%d %H:%M", minutes="%Y-%m-%d %H:%M")
			p.yaxis[0].formatter = NumeralTickFormatter(format="0.00")
			show(p)
