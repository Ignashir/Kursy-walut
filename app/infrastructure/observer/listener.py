from app.domain.event import CurrencyPulledEvent, GoldPulledEvent, WebRequestEvent


class Listener:
    def __call__(self, commodity_event: CurrencyPulledEvent | GoldPulledEvent | WebRequestEvent):
        if isinstance(commodity_event, CurrencyPulledEvent):
            print(f'CURRENCY PULLED {", ".join([currency for currency in commodity_event.code])} '
                  f'AT {commodity_event.date.strftime("%Y-%m-%d %H:%M")}')
        elif isinstance(commodity_event, GoldPulledEvent):
            print(f'GOLD PULLED FROM {commodity_event.date_to_pull.strftime("%Y-%m-%d")} '
                  f'AT {commodity_event.date.strftime("%Y-%m-%d %H:%M")}')
        elif isinstance(commodity_event, WebRequestEvent):
            print(f'METHOD {WebRequestEvent.request} : {WebRequestEvent.response_code}'
                  f'EXECUTED AT {WebRequestEvent.date}')
