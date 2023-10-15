import pytest
import httpx
from datetime import date

from app.infrastructure.api_puller.commodity_puller import CommodityPuller
from app.infrastructure.api_puller.repository import GoldOperator

# http://api.nbp.pl/api/cenyzlota
# http://api.nbp.pl/api/cenyzlota/last/{topCount}/
# http://api.nbp.pl/api/cenyzlota/{date}/
# http://api.nbp.pl/api/cenyzlota/{startDate}/{endDate}/


@pytest.fixture
def expected_gold_today_pull() -> str:
    return "http://api.nbp.pl/api/cenyzlota"


@pytest.fixture
def expected_gold_today_pull_with_limit() -> str:
    return "http://api.nbp.pl/api/cenyzlota/last/5"


@pytest.fixture
def expected_gold_today_pull_with_date() -> str:
    return "http://api.nbp.pl/api/cenyzlota/2023-10-10"


@pytest.fixture
def expected_gold_today_pull_with_begin_end_date() -> str:
    return "http://api.nbp.pl/api/cenyzlota/2023-10-10/2023-10-13"


@pytest.fixture
def gold_puller():
    return CommodityPuller()


@pytest.fixture
def gold_operator():
    return GoldOperator()


def test_gold_pull_operations(expected_gold_today_pull, expected_gold_today_pull_with_limit,
                              expected_gold_today_pull_with_date, expected_gold_today_pull_with_begin_end_date,
                              gold_puller):
    assert expected_gold_today_pull == gold_puller.create_request(gold=True).request
    assert expected_gold_today_pull_with_limit == gold_puller.create_request(gold=True, limit=5).request
    assert expected_gold_today_pull_with_date == gold_puller.create_request(
        gold=True, req_date=date(2023, 10, 10)).request
    assert expected_gold_today_pull_with_begin_end_date == gold_puller.create_request(
        gold=True, date_begin=date(2023, 10, 10), date_end=date(2023, 10, 13)).request


def test_gold_pull_results(expected_gold_today_pull, expected_gold_today_pull_with_limit,
                           expected_gold_today_pull_with_date, expected_gold_today_pull_with_begin_end_date,
                           gold_operator):
    assert httpx.get(expected_gold_today_pull).json() == gold_operator.pull_commodity().pulled_value
    assert httpx.get(expected_gold_today_pull_with_limit).json() == gold_operator.pull_commodity(limit=5).pulled_value
    assert httpx.get(expected_gold_today_pull_with_date).json() == gold_operator.pull_commodity(
        req_date=date(2023, 10, 10)).pulled_value
    assert httpx.get(expected_gold_today_pull_with_begin_end_date).json() == gold_operator.pull_commodity(
        date_begin=date(2023, 10, 10), date_end=date(2023, 10, 13)).pulled_value

