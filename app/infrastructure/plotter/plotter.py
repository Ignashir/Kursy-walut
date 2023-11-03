import matplotlib.pyplot as plt
import matplotlib.lines as lines
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)


@dataclass
class Plotter:
    @staticmethod
    def make_plot_for_single_commodity(values: list | dict, plot_name: str = "commodity-plot"):
        fig, pl = plt.subplots(figsize=(8, 4))
        pl.set_xlabel("Date")
        pl.set_ylabel("PLN")
        pl.xaxis.set_major_locator(plt.MaxNLocator(3))
        if isinstance(values, dict):
            pl.plot([data["effectiveDate"] for data in values["rates"]], [data["mid"] for data in values["rates"]])
            pl.set_title(f"Value of {values['code']}")
        elif isinstance(values, list):
            pl.plot([data["data"] for data in values], [data["cena"] for data in values])
            pl.set_title("Value of Gold")
                # logging.info("================================================================================================")
        # [logging.info(f) for f in Path().iterdir()]
        # logging.info("================================================================================================")
        # [logging.info(f) for f in Path().joinpath('app/infrastructure/web/static_resources').iterdir()]
        # logging.info("================================================================================================")
        # plt.savefig(f"./webapp/app/infrastructure/web/static_resources/{plot_name}-{date.today()}.png", format="png")
        plt.savefig(Path().joinpath(f'app/infrastructure/web/static_resources/{plot_name}.png'), format="png")
        plt.show()

    @staticmethod
    def make_plot_for_multiple_currencies(values: dict, plot_name: str = "commodity-plot"):
        fig, ax = plt.subplots()
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
