import matplotlib.pyplot as plt
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Final
import logging

logging.basicConfig(level=logging.INFO)
WIDTH_PIXELS: Final[float] = 6.5
HEIGHT_PIXELS: Final[float] = 4


@dataclass
class Plotter:
    @staticmethod
    def make_plot_for_single_commodity(values: list | dict, plot_name: str = "commodity-plot"):
        fig, pl = plt.subplots(figsize=(WIDTH_PIXELS, HEIGHT_PIXELS))
        pl.set_xlabel("Date")
        pl.set_ylabel("PLN")
        pl.xaxis.set_major_locator(plt.MaxNLocator(3))
        if isinstance(values, dict):
            pl.plot([data["effectiveDate"] for data in values["rates"]], [data["mid"] for data in values["rates"]])
            pl.set_title(f"Value of {values['code']}")
        elif isinstance(values, list):
            pl.plot([data["data"] for data in values], [data["cena"] for data in values])
            pl.set_title("Value of Gold")
        plt.savefig(Path().joinpath(f'app/infrastructure/web/static_resources/{plot_name}.png'), format="png")
        plt.show()

    @staticmethod
    def make_plot_for_multiple_currencies(values: dict, plot_name: str = "commodity-plot"):
        fig, ax = plt.subplots(figsize=(WIDTH_PIXELS, HEIGHT_PIXELS))
        ax.set_xlabel("CURRENCIES")
        ax.set_ylabel("PLN")
        ax.set_title(f"Average value of main currencies from {values['effectiveDate']} to {date.today()}")
        filtered_data = [data for data in values["rates"] if data["code"] in
                         ['USD', 'AUD', 'CAD', 'EUR', 'CHF', 'GBP']]
        currency_values = [data["mid"] for data in filtered_data]
        currency_names = [data["code"] for data in filtered_data]
        ax.bar(x=currency_names, width=1, height=currency_values, edgecolor="white", linewidth=1)
        plt.savefig(Path().joinpath(f'app/infrastructure/web/static_resources/{plot_name}.png'), format="png")
        plt.show()
