from app.infrastructure.api_puller.currency_enum import Currency

from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class CurrencyPulledEvent:
    code: [Currency]
    date: datetime


@dataclass
class GoldPulledEvent:
    '''
    date:          Date of pulling gold value from api
    date_to_pull:  Date requested to pull gold value from
    '''
    date: datetime
    date_to_pull: date


@dataclass
class WebRequestEvent:
    request: str
    response_code: int
    date: datetime