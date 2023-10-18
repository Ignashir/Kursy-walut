from app.infrastructure.api_puller.configuration import currency_operator, gold_operator
from app.infrastructure.plotter.configuration import plotter
from app.infrastructure.adapter.adapter import (CurrencyOutputPortPullerAdapter, GoldOutputPortPullerAdapter,
                                                PlotterOutputPortPullerAdapter)


currency_output_port_puller_adapter = CurrencyOutputPortPullerAdapter(currency_operator)
gold_output_port_puller_adapter = GoldOutputPortPullerAdapter(gold_operator)
plotter_output_port_puller_adapter = PlotterOutputPortPullerAdapter(plotter)
