from datetime import date


from app.domain.service import CurrencyService, GoldService
from app.infrastructure.api_puller.currency_enum import Currency


# CurrencyService().pull_many_currencies_from_api(limit=5).draw_graph(many=True)
# CurrencyService().pull_currency_from_api(code=Currency.GBP, limit=90).draw_graph(many=False)
# print(CurrencyService().pull_currency_from_api(code='GBP', limit=90).get_currency())
# GoldService().pull_gold_from_api(limit=40).draw_graph()


# ML MODEL && WEB
