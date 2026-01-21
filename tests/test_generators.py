import pytest
from typing import Generator
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

TRANSACTIONS = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]


@pytest.mark.parametrize(
    "currency_code,expected_ids",
    [
        # Фильтрация по USD - должно найти 3 транзакции
        ("USD", [939719570, 142264268, 895315941]),
        # Фильтрация по RUB - должно найти 2 транзакции
        ("RUB", [873106923, 594226727]),
        # Несуществующая валюта - пустой результат
        ("EUR", []),
        # Другая несуществующая валюта
        ("GBP", []),
        # Проверка регистра (чувствительность к регистру)
        ("usd", []),  # ожидаем пустой результат, так как в данных "USD"
        ("rub", []),  # ожидаем пустой результат, так как в данных "RUB"
    ],
)
def test_filter_by_currency_basic(currency_code, expected_ids):
    """Тест базовой фильтрации транзакций по валюте"""
    generator = filter_by_currency(TRANSACTIONS, currency_code)

    # Проверяем, что функция возвращает генератор
    assert isinstance(generator, Generator)

    # Получаем отфильтрованные транзакции
    filtered_transactions = list(generator)

    # Проверяем количество найденных транзакций
    assert len(filtered_transactions) == len(expected_ids)

    # Проверяем ID транзакций
    actual_ids = [tx["id"] for tx in filtered_transactions]
    assert actual_ids == expected_ids


def test_transaction_descriptions():
    generator = transaction_descriptions(TRANSACTIONS)

    # Проверяем, что это генератор
    assert isinstance(generator, Generator)

    # Получаем все описания
    descriptions = list(generator)

    # Проверяем количество описаний
    assert len(descriptions) == 5

    # Проверяем конкретные описания
    expected_descriptions = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]

    assert descriptions == expected_descriptions


def test_transaction_descriptions_order():
    """Тест порядка возвращаемых описаний"""
    generator = transaction_descriptions(TRANSACTIONS)

    # Проверяем порядок по одному элементу
    assert next(generator) == "Перевод организации"
    assert next(generator) == "Перевод со счета на счет"
    assert next(generator) == "Перевод со счета на счет"
    assert next(generator) == "Перевод с карты на карту"
    assert next(generator) == "Перевод организации"

    # Проверяем, что генератор исчерпан
    with pytest.raises(StopIteration):
        next(generator)


def test_transaction_descriptions_empty_list():
    """Тест с пустым списком транзакций"""
    generator = transaction_descriptions([])
    descriptions = list(generator)
    assert descriptions == []


def test_transaction_descriptions_single_transaction():
    """Тест с одной транзакцией"""
    single_transaction = [TRANSACTIONS[0]]
    generator = transaction_descriptions(single_transaction)
    descriptions = list(generator)
    assert descriptions == ["Перевод организации"]


@pytest.mark.parametrize(
    "start,stop,expected",
    [
        (2, 4, ["0000 0000 0000 0002", "0000 0000 0000 0003", "0000 0000 0000 0004"]),
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (
            9995,
            10000,
            [
                "0000 0000 0000 9995",
                "0000 0000 0000 9996",
                "0000 0000 0000 9997",
                "0000 0000 0000 9998",
                "0000 0000 0000 9999",
                "0000 0000 0001 0000",
            ],
        ),
    ],
)
def test_card_number_generator_with_stop(start, stop, expected):
    """Тест генератора с указанием stop"""
    generator = card_number_generator(start=start, stop=stop)
    result = list(generator)
    assert result == expected
    # Проверяем, что генератор исчерпан
    with pytest.raises(StopIteration):
        next(generator)


def test_card_number_generator_ifinite():
    """Тест бесконечного генератора (без stop)"""
    generator = card_number_generator(start=10)

    # Берем только первые 5 элементов
    result = []
    for i, card in enumerate(generator):
        if i >= 5:
            break
        result.append(card)

    assert result == [
        "0000 0000 0000 0010",
        "0000 0000 0000 0011",
        "0000 0000 0000 0012",
        "0000 0000 0000 0013",
        "0000 0000 0000 0014",
    ]


def test_card_number_generator_large_numbers():
    """Тест с большими числами"""
    generator = card_number_generator(start=9999999999999990, stop=9999999999999999)
    result = list(generator)
    assert len(result) == 10
    assert result[0] == "9999 9999 9999 9990"
    assert result[-1] == "9999 9999 9999 9999"
