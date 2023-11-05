import logging
from app.domain.event import CurrencyPulledEvent, GoldPulledEvent, WebRequestEvent, PDFCreateEvent


logging.basicConfig(level=logging.INFO)


class Listener:
    def __call__(self, commodity_event: CurrencyPulledEvent | GoldPulledEvent | WebRequestEvent | PDFCreateEvent):
        if isinstance(commodity_event, CurrencyPulledEvent):
            logging.info(f'CURRENCY PULLED {", ".join([currency for currency in commodity_event.code])} '
                         f'AT {commodity_event.date.strftime("%Y-%m-%d %H:%M")}')
        elif isinstance(commodity_event, GoldPulledEvent):
            logging.info(f'GOLD PULLED FROM {commodity_event.date_to_pull.strftime("%Y-%m-%d")} '
                         f'AT {commodity_event.date.strftime("%Y-%m-%d %H:%M")}')
        elif isinstance(commodity_event, WebRequestEvent):
            logging.info(f'METHOD {commodity_event.request} : {commodity_event.response_code} '
                         f'EXECUTED AT {commodity_event.date.strftime("%Y-%m-%d %H:%M")}')
        elif isinstance(commodity_event, PDFCreateEvent):
            logging.info(f'REPORT RENDERED AT {commodity_event.date}')
