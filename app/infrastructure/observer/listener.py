from app.domain.event import CurrencyPulledEvent, GoldPulledEvent


class Listener:
    def __call__(self, commodity_event: CurrencyPulledEvent | GoldPulledEvent):
        if isinstance(commodity_event, CurrencyPulledEvent):
            print(f'CURRENCY PULLED {", ".join([currency for currency in commodity_event.code])} '
                  f'AT {commodity_event.date.strftime("%Y-%m-%d %H:%M")}')
        else:
            print(f'GOLD PULLED FROM {commodity_event.date_to_pull.strftime("%Y-%m-%d %H:%M")} '
                  f'AT {commodity_event.date.strftime("%Y-%m-%d %H:%M")}')
