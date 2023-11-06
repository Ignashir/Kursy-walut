from datetime import date, datetime
from typing import Self

from app.infrastructure.api_puller.currency_enum import Currency
from app.application.port.input import (SingleCurrencyPullUseCase,
                                        MultipleCurrencyPullUseCase,
                                        GetCurrencyUseCase,
                                        GoldPullUseCase,
                                        GetGoldUseCase,
                                        DrawAGraphUseCase,
                                        GetReport,
                                        PredictValue)
from app.domain.event import GoldPulledEvent, CurrencyPulledEvent
from app.infrastructure.adapter.configuration import (currency_output_port_puller_adapter,
                                                      gold_output_port_puller_adapter,
                                                      plotter_output_port_puller_adapter,
                                                      pdf_file_reporter_port_adapter,
                                                      gold_predictor_port_adapter)
from app.infrastructure.observer.configuration import event


class CurrencyService(SingleCurrencyPullUseCase, MultipleCurrencyPullUseCase, GetCurrencyUseCase, DrawAGraphUseCase, GetReport):
    def pull_currency_from_api(self,
                               code: str = None,
                               req_date: str = None,
                               date_begin: str = None,
                               date_end: str = None,
                               limit: int = None) -> Self:
        code = Currency[code]
        currency_output_port_puller_adapter.pull_single_currency(code, req_date, date_begin, date_end, limit)
        event.publish(CurrencyPulledEvent([code.name], datetime.today()))
        return self

    def pull_many_currencies_from_api(self,
                                      req_date: str = None,
                                      date_begin: str = None,
                                      date_end: str = None,
                                      limit: int = None) -> Self:
        currency_output_port_puller_adapter.pull_multiple_currencies(req_date, date_begin, date_end, limit)
        event.publish(CurrencyPulledEvent([code for code in Currency.__dict__["_member_names_"]], datetime.today()))
        return self

    def get_currency(self):
        return currency_output_port_puller_adapter.get_pulled_currency()

    def draw_graph(self, many: bool = False) -> Self:
        if not many:
            plotter_output_port_puller_adapter.make_plot_for_single_commodity(
                currency_output_port_puller_adapter.puller_repository.pulled_value, plot_name="one-currency")
        else:
            plotter_output_port_puller_adapter.make_plot_for_multiple_currencies(
                currency_output_port_puller_adapter.puller_repository.pulled_value, plot_name="many-currency")
        return self

    def get_report(self, many: bool = False) -> Self:
        pdf_file_reporter_port_adapter.create_report(
            currency_output_port_puller_adapter.puller_repository.pulled_value, many=many).generate_report()
        return self


class GoldService(GoldPullUseCase, GetGoldUseCase, DrawAGraphUseCase, GetReport):
    def pull_gold_from_api(self,
                           req_date: str = None,
                           date_begin: str = None,
                           date_end: str = None,
                           limit: int = None) -> Self:
        date_to_pull = req_date if req_date else date_begin
        event.publish(GoldPulledEvent(
            date=datetime.today(),
            date_to_pull=(datetime.strptime(date_to_pull, "%Y-%m-%d").date()
                          if date_to_pull else datetime.today())))
        gold_output_port_puller_adapter.pull_gold(req_date=req_date, date_begin=date_begin, date_end=date_end, limit=limit)
        return self

    def get_gold(self):
        return gold_output_port_puller_adapter.get_pulled_gold()

    def draw_graph(self) -> Self:
        plotter_output_port_puller_adapter.make_plot_for_single_commodity(
            gold_output_port_puller_adapter.puller_repository.pulled_value, plot_name="gold-plot")
        return self

    def get_report(self) -> Self:
        pdf_file_reporter_port_adapter.create_report(
            gold_output_port_puller_adapter.puller_repository.pulled_value, gold=True).generate_report()
        return self

# TODO[IGNACY] for now it is gold exclusive maybe add usd in future
class PredictorService(PredictValue):
    def predict_value(self, date_to_predict: str):
        if datetime.strptime(date_to_predict, '%Y-%m-%d').date() <= date.today():
            return GoldService().pull_gold_from_api(req_date=date_to_predict).get_gold()
        return gold_predictor_port_adapter.predict_value(date_to_predict)[0]
