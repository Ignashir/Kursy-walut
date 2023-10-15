import pytest
import httpx
from datetime import date

from app.infrastructure.api_puller.commodity_puller import CommodityPuller
from app.infrastructure.api_puller.repository import CurrencyOperator
from app.infrastructure.api_puller.currency_enum import Currency


@pytest.fixture
def expected_all_table_pull() -> str:
    return "http://api.nbp.pl/api/exchangerates/tables/a/"


@pytest.fixture
def expected_all_table_pull_with_limit() -> str:
    return "http://api.nbp.pl/api/exchangerates/tables/a/last/5/"


@pytest.fixture
def expected_all_table_pull_with_date() -> str:
    return "http://api.nbp.pl/api/exchangerates/tables/a/2023-10-10/"


@pytest.fixture
def expected_all_table_pull_with_begin_end_date() -> str:
    return "http://api.nbp.pl/api/exchangerates/tables/a/2023-10-10/2023-10-13/"


@pytest.fixture
def expected_single_currency_pull() -> str:
    return "http://api.nbp.pl/api/exchangerates/rates/a/usd/"


@pytest.fixture
def expected_single_currency_pull_with_limit() -> str:
    return "http://api.nbp.pl/api/exchangerates/rates/a/usd/last/5/"


@pytest.fixture
def expected_single_currency_pull_with_date() -> str:
    return "http://api.nbp.pl/api/exchangerates/rates/a/usd/2023-10-10/"


@pytest.fixture
def expected_single_currency_pull_with_begin_end_date() -> str:
    return "http://api.nbp.pl/api/exchangerates/rates/a/usd/2023-10-10/2023-10-13/"


@pytest.fixture
def currency_puller():
    return CommodityPuller()


@pytest.fixture
def currency_operator():
    return CurrencyOperator()


def test_multiple_request_types(expected_all_table_pull, expected_all_table_pull_with_limit,
                                expected_all_table_pull_with_date, expected_all_table_pull_with_begin_end_date,
                                currency_puller):
    assert expected_all_table_pull == currency_puller.create_request().request
    assert expected_all_table_pull_with_limit == currency_puller.create_request(limit=5).request
    assert expected_all_table_pull_with_date == currency_puller.create_request(
        req_date=date(2023, 10, 10)).request
    assert expected_all_table_pull_with_begin_end_date == currency_puller.create_request(
        date_begin=date(2023, 10, 10), date_end=date(2023, 10, 13)).request


def test_single_request_types(expected_single_currency_pull, expected_single_currency_pull_with_limit,
                              expected_single_currency_pull_with_date, expected_single_currency_pull_with_begin_end_date,
                              currency_puller):
    assert expected_single_currency_pull == currency_puller.create_request(code=Currency.USD).request
    assert expected_single_currency_pull_with_limit == currency_puller.create_request(
        code=Currency.USD, limit=5).request
    assert expected_single_currency_pull_with_date == currency_puller.create_request(
        code=Currency.USD, req_date=date(2023, 10, 10)).request
    assert expected_single_currency_pull_with_begin_end_date == currency_puller.create_request(
        code=Currency.USD, date_begin=date(2023, 10, 10), date_end=date(2023, 10, 13)
    ).request


def test_multiple_request_results(expected_all_table_pull, expected_all_table_pull_with_limit,
                                  expected_all_table_pull_with_date, expected_all_table_pull_with_begin_end_date,
                                  currency_operator):
    assert httpx.get(expected_all_table_pull).json()[0] == currency_operator.pull_all_commodities().pulled_value
    assert httpx.get(expected_all_table_pull_with_limit).json()[0] == currency_operator.pull_all_commodities(
        limit=5).pulled_value
    assert httpx.get(expected_all_table_pull_with_date).json()[0] == currency_operator.pull_all_commodities(
        req_date=date(2023, 10, 10)).pulled_value
    assert (httpx.get(expected_all_table_pull_with_begin_end_date).json()[0] == currency_operator.pull_all_commodities(
        date_begin=date(2023, 10, 10), date_end=date(2023, 10, 13)).pulled_value)


def test_single_request_results(expected_single_currency_pull, expected_single_currency_pull_with_limit,
                                expected_single_currency_pull_with_date, expected_single_currency_pull_with_begin_end_date,
                                currency_operator):
    assert httpx.get(expected_single_currency_pull).json() == currency_operator.pull_commodity(
        code=Currency.USD).pulled_value
    assert httpx.get(expected_single_currency_pull_with_limit).json() == currency_operator.pull_commodity(
        code=Currency.USD, limit=5).pulled_value
    assert httpx.get(expected_single_currency_pull_with_date).json() == currency_operator.pull_commodity(
        code=Currency.USD, req_date=date(2023, 10, 10)).pulled_value
    assert (httpx.get(expected_single_currency_pull_with_begin_end_date).json() == currency_operator.
            pull_commodity(code=Currency.USD, date_begin=date(2023, 10, 10),
                           date_end=date(2023, 10, 13)).pulled_value)
