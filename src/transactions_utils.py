import re
from collections import Counter
from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Фильтрация транзакций по наличию заданной строки в описании с использованием библиотеки re.
    Поиск регистронезависимый.
    Args:
        data: Список словарей с данными о транзакциях.
        search: Строка для поиска в описании.
    Returns:
        Список транзакций, у которых в поле 'description' найдена строка search."""

    if not search:
        return data

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result = [transaction for transaction in data if pattern.search(transaction.get("description", ""))]
    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, Any]:
    """ "Подсчитывает количество транзакций в каждой из заданных категорий.
    Категория определяется по полю 'description'. Если описание транзакции совпадает
    с одной из категорий, счётчик для этой категории увеличивается.

    Args:
        data: Список словарей с данными о транзакциях.
        categories: Список категорий (строк), которые нужно подсчитать.

    Returns:
        Словарь {категория: количество транзакций}.
    """
    counter = Counter()
    for transaction in data:
        desc = transaction.get("description", "")
        if desc in categories:
            counter[desc] += 1
    return dict(counter)
