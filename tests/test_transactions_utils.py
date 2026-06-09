import pytest
from src.transactions_utils import process_bank_search, process_bank_operations
@pytest.fixture
def sample_transactions():
    return [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
        {"description": "Оплата услуг"},
    ]


def test_process_bank_search_found(sample_transactions):
    result = process_bank_search(sample_transactions, "перевод")
    assert len(result) == 3
    assert all("перевод" in t["description"].lower() for t in result)


def test_process_bank_search_not_found(sample_transactions):
    result = process_bank_search(sample_transactions, "покупка")
    assert result == []


def test_process_bank_search_case_insensitive(sample_transactions):
    result = process_bank_search(sample_transactions, "ОТКРЫТИЕ")
    assert len(result) == 1
    assert result[0]["description"] == "Открытие вклада"


def test_process_bank_search_empty_string(sample_transactions):
    result = process_bank_search(sample_transactions, "")
    assert result == sample_transactions


def test_process_bank_operations(sample_transactions):
    categories = ["Перевод организации", "Открытие вклада", "Оплата услуг"]
    result = process_bank_operations(sample_transactions, categories)
    expected = {"Перевод организации": 2, "Открытие вклада": 1, "Оплата услуг": 1}
    assert result == expected


def test_process_bank_operations_no_match(sample_transactions):
    categories = ["Покупки", "Снятие наличных"]
    result = process_bank_operations(sample_transactions, categories)
    assert result == {}


def test_process_bank_operations_empty_categories(sample_transactions):
    result = process_bank_operations(sample_transactions, [])
    assert result == {}