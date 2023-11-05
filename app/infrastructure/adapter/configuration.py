from app.infrastructure.api_puller.configuration import currency_operator, gold_operator
from app.infrastructure.plotter.configuration import plotter
from app.infrastructure.file_reporter.configuration import pdf_reporter
from app.infrastructure.adapter.adapter import (CurrencyOutputPortPullerAdapter, GoldOutputPortPullerAdapter,
                                                PlotterOutputPortPullerAdapter, FileReporterPortAdapter)


currency_output_port_puller_adapter = CurrencyOutputPortPullerAdapter(currency_operator)
gold_output_port_puller_adapter = GoldOutputPortPullerAdapter(gold_operator)
plotter_output_port_puller_adapter = PlotterOutputPortPullerAdapter(plotter)
pdf_file_reporter_port_adapter = FileReporterPortAdapter(pdf_reporter)
