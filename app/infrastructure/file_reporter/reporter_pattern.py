from abc import ABC, abstractmethod


class FileReporter(ABC):
    @abstractmethod
    def single_commodity_render(self, data: dict, gold: bool):
        pass

    @abstractmethod
    def multiple_currency_render(self, data: dict):
        pass

    @abstractmethod
    def create_report(self):
        pass
