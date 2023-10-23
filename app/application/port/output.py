from abc import ABC, abstractmethod
from datetime import date

from app.domain.event import CurrencyPulledEvent, GoldPulledEvent
from app.infrastructure.api_puller.currency_enum import Currency


class CommodityPullerEventPublisher(ABC):
    @abstractmethod
    def publish(self, commodity_pull_event: CurrencyPulledEvent | GoldPulledEvent):
        pass


class CurrencyOutputPort(ABC):
    @abstractmethod
    def pull_single_currency(self,
                             code: Currency = None,
                             req_date: date = None,
                             date_begin: date = None,
                             date_end: date = None,
                             limit: int = None):
        pass

    @abstractmethod
    def pull_multiple_currencies(self,
                                 req_date: date = None,
                                 date_begin: date = None,
                                 date_end: date = None,
                                 limit: int = None):
        pass

    @abstractmethod
    def get_pulled_currency(self):
        pass

    @abstractmethod
    def make_plot(self, code):
        pass


class GoldOutputPort(ABC):
    @abstractmethod
    def pull_gold(self,
                  req_date: date = None,
                  date_begin: date = None,
                  date_end: date = None,
                  limit: int = None):
        pass

    @abstractmethod
    def get_pulled_gold(self):
        pass


class PlotterOutputPort(ABC):
    @abstractmethod
    def make_plot_for_single_commodity(self, values: list | dict, plot_name: str):
        pass

    @abstractmethod
    def make_plot_for_multiple_currencies(self, values: dict, plot_name: str):
        pass
