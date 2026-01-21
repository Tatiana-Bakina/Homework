from itertools import count
from typing import Generator, Optional


def filter_by_currency(transactions: list, currency_code: str) -> Generator:
    """
    Генерирует транзакции заданной валюты.
    Parameters:
        transactions (list): Список транзакций, каждая из которых представлена словарем.
                            Каждая транзакция включает вложенное поле operationAmount.currency.code,
                            которое хранит валюту операции.
        currency_code (str): Код валюты, по которой фильтруются транзакции.
    Yields:
        dict: Транзакции, соответствующие указанной валюте.
    """
    yield from (ts for ts in transactions if ts["operationAmount"]["currency"]["code"] == currency_code)


def transaction_descriptions(transactions: list) -> Generator[str, None, None]:
    """
    Генерирует описания транзакций.
    Parameters:
        transactions (list): Список транзакций, каждая из которых представлена словарем.
                            Поле description содержит описание операции.
    Yields:
        str: Описание очередной транзакции.
    """
    yield from (ts["description"] for ts in transactions)


def card_number_generator(start: int = 1, stop: Optional[int] = None) -> Generator[str, None, None]:
    """
    Генерирует номера банковских карт в указанном диапазоне.
    Parameters:
        start (int): Начальное значение генерации номеров (по умолчанию 1).
        stop (Optional[int]): Конечное значение генерации номеров (если None, генерация продолжается бесконечно).
    Yields:
        str: Форматированный номер кредитной карты вида 'XXXX XXXX XXXX XXXX'.
    """
    for i in count(start=start):
        if stop is not None and i > stop:
            break
        formatted_number = f"{i:016}"
        yield f"{formatted_number[:4]} {formatted_number[4:8]} {formatted_number[8:12]} {formatted_number[12:]}"

