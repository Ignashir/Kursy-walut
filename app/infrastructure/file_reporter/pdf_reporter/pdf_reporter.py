from fpdf import FPDF
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import logging

from app.infrastructure.file_reporter.reporter_builder import FileReporter


logging.basicConfig(level=logging.INFO)


class PDF(FPDF):
    # Header of every PDF page
    def header(self):
        self.set_font('helvetica', 'B', 20)
        self.cell(0, 20, 'REPORT', align='C')
        self.ln(20)

    # Footer of every PDF page
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', '', 10)
        self.cell(0, 7, 'TO SEE MORE ABOUT API VISIT', align='C')
        self.ln(5)
        self.cell(0, 7, 'NBP.API', align='C', link="https://nbp.pl/statystyka-i-sprawozdawczosc/kursy/")
        self.ln(2)
        self.cell(0, 7, f'PAGE {self.page_no()}/{{nb}}', align='L')
        self.cell(0, 7, f'DATE OF RENDER {date.today()}', align='R')


@dataclass
class PDFReporter(FileReporter):
    pdf_object: PDF = PDF(orientation='P', unit='mm', format='A4')

    # Create PDF object for single commodities (currency/gold)
    def single_commodity_render(self, data: dict, gold: bool = False):
        values = data if gold else data["rates"]
        self.pdf_object.add_page()
        self.pdf_object.set_font("Times", size=20)
        self.pdf_object.cell(0, 20, f"VALUES OF {'GOLD' if gold else data['code']}", align='C')
        self.pdf_object.ln(20)
        self.pdf_object.set_font("Times", size=10)
        with self.pdf_object.table(borders_layout="INTERNAL", line_height=2.5 * self.pdf_object.font_size) as table:
            header = table.row()
            header.cell("PRICE IN PLN")
            header.cell("DATE")
            for pull in values:
                row = table.row()
                if gold:
                    row.cell(f"{pull['cena']}")
                    row.cell(pull['data'])
                else:
                    row.cell(f"{pull['mid']}")
                    row.cell(pull['effectiveDate'])
        self.pdf_object.ln(20)
        self.pdf_object.image(Path().joinpath(f'app/infrastructure/web/static_resources/'
                                              f'{"gold-plot" if gold else "one-currency"}.png'), x=-6)

    # Create PDF object for multiple currencies
    def multiple_currency_render(self, data: dict):
        values = data["rates"]
        self.pdf_object.add_page()
        self.pdf_object.set_font("Times", size=20)
        self.pdf_object.cell(0, 20, "VALUES OF MAIN CURRENCIES", align='C')
        self.pdf_object.ln(10)
        self.pdf_object.cell(0, 20, f"AS OF {data['effectiveDate']}", align='C')
        self.pdf_object.ln(20)
        self.pdf_object.set_font("Times", size=10)
        with self.pdf_object.table(borders_layout="INTERNAL", line_height=2.5 * self.pdf_object.font_size) as table:
            header = table.row()
            header.cell("CURRENCY")
            header.cell("AVG PRICE IN PLN")
            for pull in values:
                row = table.row()
                row.cell(pull['code'])
                row.cell(f"{pull['mid']}")
        self.pdf_object.ln(20)
        self.pdf_object.image(Path().joinpath('app/infrastructure/web/static_resources/many-currency.png'), x=-6)

    # Render PDF object and place it in static_resources in web folder under 'report.pdf' name
    def create_report(self):
        self.pdf_object.output(Path().joinpath('app/infrastructure/web/static_resources/report.pdf').as_posix())
        # This has to stay like that because, as docs state:
        #   Note that FPDF instance objects are not designed to be reusable:
        #   content cannot be added once output() has been called.
        self.pdf_object = PDF(orientation='P', unit='mm', format='A4')
