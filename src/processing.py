from typing import Dict, List


def filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Фильтрует список транзакций по указанному статусу состояния ('state').

    Параметры:
      transactions (List[Dict]): Список словарей, каждый из которых представляет одну банковскую операцию.
                               Каждый словарь содержит поля: id, date, amount и state.
      state (str): Значение статуса, по которому производится фильтрация (например, EXECUTED или CANCELED).
                   По умолчанию установлено значение 'EXECUTED'.

    Возвращает:
      List[Dict]: Новый список транзакций, содержащий только те записи, чей статус совпадает с указанным значением.
    """
    filtered_transactions = [transaction for transaction in transactions if transaction.get("state") == state]
    return filtered_transactions


def sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Сортирует список транзакций по дате.

    Параметры:
      transactions (List[Dict]): Список словарей, представляющих банковские операции.
                                Каждое поле словаря должно содержать ключ 'date',
                                содержащий строку даты-времени в ISO формате.
      reverse (bool): Логический флаг, определяющий направление сортировки.
                     True означает сортировку по убыванию (самые свежие операции первыми),
                     False — по возрастанию (старые операции первыми).
                     По умолчанию установлен True.

    Возвращает:
      List[Dict]: Новую копию отсортированного списка транзакций.
    """
    sorted_transactions = sorted(
        transactions,
        key=lambda x: x["date"],  # Использует поле 'date' для сравнения элементов
        reverse=reverse,  # Направление сортировки
    )
    return sorted_transactions
