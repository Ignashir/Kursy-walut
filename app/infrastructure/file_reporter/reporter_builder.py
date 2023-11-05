# Tutaj znajdowac bedzie sie cala klasa umozliwiajaca zapisanie danych do pliku (txt, pdf, json)
from abc import ABC, abstractmethod

# TODO nie wiem czy to nie powinno znajdowac sie w application/port/output
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


class TXTReporter(FileReporter):
    def single_commodity_render(self, data: dict, gold: bool):
        pass

    def multiple_currency_render(self, data: dict):
        pass

    def create_report(self):
        pass
