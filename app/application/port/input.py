from abc import ABC, abstractmethod
from datetime import date

from app.infrastructure.api_puller.currency_enum import Currency


class SingleCurrencyPullUseCase(ABC):
    @abstractmethod
    def pull_currency_from_api(self,
                               code: Currency = None,
                               req_date: date = None,
                               date_begin: date = None,
                               date_end: date = None,
                               limit: int = None):
        pass


class MultipleCurrencyPullUseCase(ABC):
    @abstractmethod
    def pull_many_currencies_from_api(self,
                               req_date: date = None,
                               date_begin: date = None,
                               date_end: date = None,
                               limit: int = None):
        pass


class GetCurrencyUseCase(ABC):
    @abstractmethod
    def get_currency(self):
        pass


class GoldPullUseCase(ABC):
    @abstractmethod
    def pull_gold_from_api(self,
                           req_date: date = None,
                           date_begin: date = None,
                           date_end: date = None,
                           limit: int = None):
        pass


class GetGoldUseCase(ABC):
    @abstractmethod
    def get_gold(self):
        pass
