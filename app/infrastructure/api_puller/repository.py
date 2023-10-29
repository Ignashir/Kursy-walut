from typing import Self
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import date

from app.infrastructure.api_puller.commodity_puller import CommodityPuller
from app.infrastructure.api_puller.currency_enum import Currency


import logging
logging.basicConfig(level=logging.INFO)

@dataclass
class PullerOperator(ABC):
    puller = CommodityPuller()
    pulled_value: dict | None = None

    @abstractmethod
    def pull_commodity(self,
                       code: Currency = None,
                       gold: bool = False,
                       req_date: date = None,
                       date_begin: date = None,
                       date_end: date = None,
                       limit: int = None) -> Self:
        pass

    @abstractmethod
    def return_commodity(self) -> None:
        pass


class CurrencyOperator(PullerOperator):
    def pull_all_commodities(self,
                             req_date: date = None,
                             date_begin: date = None,
                             date_end: date = None,
                             limit: int = None) -> Self:
        self.pulled_value = self.puller.pull_currency(req_date=req_date, date_begin=date_begin, date_end=date_end,
                                                      limit=limit)[0]
        return self

    def pull_commodity(self,
                       code: Currency = None,
                       gold: bool = False,
                       req_date: date = None,
                       date_begin: date = None,
                       date_end: date = None,
                       limit: int = None) -> Self:
        self.pulled_value = self.puller.pull_currency(code=code, req_date=req_date, date_begin=date_begin,
                                                      date_end=date_end, limit=limit)
        return self

    def return_commodity(self) -> None:
        return self.pulled_value


class GoldOperator(PullerOperator):
    def pull_commodity(self,
                       code: Currency = None,
                       gold: bool = True,
                       req_date: date = None,
                       date_begin: date = None,
                       date_end: date = None,
                       limit: int = None) -> Self:
        self.pulled_value = self.puller.pull_currency(gold=True, req_date=req_date, date_begin=date_begin,
                                                      date_end=date_end, limit=limit)
        return self

    def return_commodity(self) -> None:
        return self.pulled_value

