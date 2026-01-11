import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_executed(transactions):
    """Проверяет фильтрацию транзакций по статусу 'EXECUTED'."""
    result = filter_by_state(transactions)
    expected_result = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
    assert result == expected_result


def test_sort_by_date_descending(transactions):
    """Проверяет сортировку транзакций по дате в порядке убывания."""
    result = sort_by_date(transactions)
    expected_result = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
    assert result == expected_result


def test_sort_by_date_ascending(transactions):
    """Проверяет сортировку транзакций по дате в порядке возрастания."""
    result = sort_by_date(transactions, reverse=False)
    expected_result = [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]
    assert result == expected_result
