from dataclasses import dataclass
from datetime import date

from app.infrastructure.api_puller.currency_enum import Currency
from app.application.port.output import CurrencyOutputPort, GoldOutputPort, PlotterOutputPort
from app.infrastructure.api_puller.repository import CurrencyOperator, GoldOperator
from app.infrastructure.plotter.plotter import Plotter


@dataclass
class CurrencyOutputPortPullerAdapter(CurrencyOutputPort):
    puller_repository: CurrencyOperator

    def pull_single_currency(self,
                             code: Currency = None,
                             req_date: date = None,
                             date_begin: date = None,
                             date_end: date = None,
                             limit: int = None):
        self.puller_repository.pull_commodity(code=code, req_date=req_date, date_begin=date_begin, date_end=date_end,
                                              limit=limit)

    def pull_multiple_currencies(self,
                                 req_date: date = None,
                                 date_begin: date = None,
                                 date_end: date = None,
                                 limit: int = None):
        self.puller_repository.pull_all_commodities(req_date=req_date, date_begin=date_begin, date_end=date_end,
                                                    limit=limit)

    def get_pulled_currency(self):
        return self.puller_repository.return_commodity()


@dataclass
class GoldOutputPortPullerAdapter(GoldOutputPort):
    puller_repository: GoldOperator

    def pull_gold(self,
                  req_date: date = None,
                  date_begin: date = None,
                  date_end: date = None,
                  limit: int = None):
        self.puller_repository.pull_commodity(req_date=req_date, date_begin=date_begin, date_end=date_end, limit=limit)

    def get_pulled_gold(self):
        return self.puller_repository.return_commodity()


@dataclass
class PlotterOutputPortPullerAdapter(PlotterOutputPort):
    plotter: Plotter

    def make_plot_for_single_commodity(self, values: list | dict, plot_name: str = ""):
        self.plotter.make_plot_for_single_commodity(values, plot_name)

    def make_plot_for_multiple_currencies(self, values: dict, plot_name: str = ""):
        self.plotter.make_plot_for_multiple_currencies(values, plot_name)
