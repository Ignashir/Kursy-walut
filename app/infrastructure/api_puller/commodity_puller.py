import httpx
from dataclasses import dataclass
from datetime import date
from typing import Self
# import json
# import functools

from app.infrastructure.api_puller.currency_enum import Currency

# http://api.nbp.pl/api/exchangerates/tables/a/
# http://api.nbp.pl/api/exchangerates/tables/a/last/{topCount}/
# http://api.nbp.pl/api/exchangerates/tables/a/{date}/
# http://api.nbp.pl/api/exchangerates/tables/a/{startDate}/{endDate}/

# http://api.nbp.pl/api/exchangerates/rates/a/{code}/
# http://api.nbp.pl/api/exchangerates/rates/a/{code}/last/{topCount}/
# http://api.nbp.pl/api/exchangerates/rates/a/{code}/{date}/
# http://api.nbp.pl/api/exchangerates/rates/a/{code}/{startDate}/{endDate}/

# ----------------------------------------------------------------
# Gdybym chcial jednak zmienic wszystko na asynchroniczne
# ----------------------------------------------------------------
# def async_client(func):
#     @functools.wraps(func)
#     async def wrapped(*args, **kwargs):
#         client = httpx.AsyncClient()
#         await func(*args, **kwargs, client=client)
#         await client.aclose()
#     return wrapped



@dataclass
class CommodityPuller:
    request: str = ""

    def create_request(self,
                       code: Currency = None,
                       gold: bool = False,
                       req_date: date = None,
                       date_begin: date = None,
                       date_end: date = None,
                       limit: int = None
                       ) -> Self:
        '''
                Method allowing to pull currency data from NBP.PL API.
                USE limit / date_begin / req_date SEPARATELY.
                THE HIERARCHY IS req_date -> date_begin -> limit
                SAME APPLIES TO GOLD AND CURRENCY.
                :param code:        Currency code
                :param gold:        Pull gold or not
                :param req_date:    Date to pull data from
                :param date_begin:  Starting date to pull data from
                :param date_end:    Ending date to pull data from (optional)
                :param limit:       Number of data to pull (optional)
                :return: json object with data
                '''
        ending = lambda x: "" if x else "/"
        self.request = "http://api.nbp.pl/api/"
        if gold:
            self.request += "cenyzlota"
            if any([req_date, date_begin, limit]):
                self.request += "/"
        else:
            self.request += "exchangerates/"
            self.request += f"rates/a/{code.name.lower()}/" if code else "tables/a/"
        if req_date:
            self.request += req_date.strftime("%Y-%m-%d") + ending(gold)
        elif date_begin:
            self.request += date_begin.strftime('%Y-%m-%d') + "/"
            self.request += date_end.strftime('%Y-%m-%d') + ending(gold) if date_end else ""
        elif limit:
            self.request += f"last/{limit}" + ending(gold)
        return self

    # @async_client
    def pull_currency(self,
                            code: Currency = None,
                            gold: bool = False,
                            req_date: date = None,
                            date_begin: date = None,
                            date_end: date = None,
                            limit: int = None
    ) -> {}:
        try:
            if req_date.weekday() >= 5:
                raise ValueError("DATE MUST BE A WORKING DAY")
        except AttributeError:
            pass
        self.create_request(code, gold, req_date, date_begin, date_end, limit)
        return httpx.get(self.request).json()
