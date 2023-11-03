from app.application.port.output import CommodityPullerEventPublisher
from app.domain.event import CurrencyPulledEvent, GoldPulledEvent, WebRequestEvent
from app.infrastructure.observer.listener import Listener


class Event(CommodityPullerEventPublisher):
    def __init__(self):
        self.observers = []

    def subscribe(self, observer: Listener) -> None:
        if observer not in self.observers:
            self.observers.append(observer)

    def unsubscribe(self, observer: Listener) -> None:
        self.observers.remove(observer)

    def publish(self, commodity_pull_event: CurrencyPulledEvent | GoldPulledEvent | WebRequestEvent):
        [observer(commodity_pull_event) for observer in self.observers]