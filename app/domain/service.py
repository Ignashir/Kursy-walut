from datetime import date, datetime
from typing import Self

from app.infrastructure.api_puller.currency_enum import Currency
from app.application.port.input import (SingleCurrencyPullUseCase,
                                        MultipleCurrencyPullUseCase,
                                        GetCurrencyUseCase,
                                        GoldPullUseCase,
                                        GetGoldUseCase,
                                        DrawAGraphUseCase)
from app.domain.event import GoldPulledEvent, CurrencyPulledEvent
from app.infrastructure.adapter.configuration import (currency_output_port_puller_adapter,
                                                      gold_output_port_puller_adapter,
                                                      plotter_output_port_puller_adapter)
from app.infrastructure.observer.configuration import event


class CurrencyService(SingleCurrencyPullUseCase, MultipleCurrencyPullUseCase, GetCurrencyUseCase, DrawAGraphUseCase):
    def pull_currency_from_api(self,
                               code: Currency = None,
                               req_date: date = None,
                               date_begin: date = None,
                               date_end: date = None,
                               limit: int = None) -> Self:
        currency_output_port_puller_adapter.pull_single_currency(code, req_date, date_begin, date_end, limit)
        event.publish(CurrencyPulledEvent([code.name], datetime.today()))
        return self

    def pull_many_currencies_from_api(self,
                                      req_date: date = None,
                                      date_begin: date = None,
                                      date_end: date = None,
                                      limit: int = None) -> Self:
        currency_output_port_puller_adapter.pull_multiple_currencies(req_date, date_begin, date_end, limit)
        event.publish(CurrencyPulledEvent([code for code in Currency.__dict__["_member_names_"]], datetime.today()))
        return self

    def get_currency(self):
        currency_output_port_puller_adapter.get_pulled_currency()

    def draw_graph(self, many: bool = False):
        if not many:
            plotter_output_port_puller_adapter.make_plot_for_single_commodity(
                currency_output_port_puller_adapter.puller_repository.pulled_value, plot_name="one-currency")
        else:
            plotter_output_port_puller_adapter.make_plot_for_multiple_currencies(
                currency_output_port_puller_adapter.puller_repository.pulled_value, plot_name="many-currency")


class GoldService(GoldPullUseCase, GetGoldUseCase, DrawAGraphUseCase):
    def pull_gold_from_api(self,
                           req_date: date = None,
                           date_begin: date = None,
                           date_end: date = None,
                           limit: int = None) -> Self:
        event.publish(GoldPulledEvent(date=datetime.today(), date_to_pull=(req_date if req_date else datetime.today())))
        gold_output_port_puller_adapter.pull_gold(req_date=req_date, date_begin=date_begin, date_end=date_end, limit=limit)
        return self

    def get_gold(self):
        gold_output_port_puller_adapter.get_pulled_gold()

    def draw_graph(self):
        plotter_output_port_puller_adapter.make_plot_for_single_commodity(
            gold_output_port_puller_adapter.puller_repository.pulled_value, plot_name="gold-plot")
