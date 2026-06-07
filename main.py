"""
Главный модуль программы для работы с банковскими транзакциями.
"""

import os
import sys
from typing import List, Dict, Any

from src.data_readers import read_transactions_from_csv, read_transactions_from_excel
from src.processing import filter_by_state, sort_by_date
from src.transactions_utils import process_bank_search
from src.utils import load_transactions_from_json
from src.widget import get_date, mask_account_card


def load_transactions(source: int) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из выбранного источника.

    Args:
        source: 1 - JSON, 2 - CSV, 3 - XLSX.

    Returns:
        Список транзакций в исходном формате.
    """
    base_dir = os.path.join(os.path.dirname(__file__), "data")
    if source == 1:
        file_path = os.path.join(base_dir, "operations.json")
        print("Для обработки выбран JSON-файл.")
        raw_data = load_transactions_from_json(file_path)
        raw_data = [item for item in raw_data if item]
        return raw_data
    elif source == 2:
        file_path = os.path.join(base_dir, "transactions.csv")
        print("Для обработки выбран CSV-файл.")
        return read_transactions_from_csv(file_path)
    elif source == 3:
        file_path = os.path.join(base_dir, "transactions_excel.xlsx")
        print("Для обработки выбран XLSX-файл.")
        return read_transactions_from_excel(file_path)
    else:
        print("Неверный выбор. Завершение программы.")
        sys.exit(1)


def get_valid_status() -> str:
    """Запрашивает у пользователя статус операции до тех пор, пока не будет введён корректный."""
    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        ).strip().upper()
        if status in valid_statuses:
            print(f"Операции отфильтрованы по статусу \"{status}\"")
            return status
        print(f"Статус операции \"{status}\" недоступен.")


def ask_yes_no(question: str) -> bool:
    """Задаёт вопрос с ответом Да/Нет и возвращает True/False."""
    while True:
        answer = input(f"{question} Да/Нет\n").strip().lower()
        if answer in ("да", "yes", "y", "д"):
            return True
        if answer in ("нет", "no", "n"):
            return False
        print("Пожалуйста, ответьте 'Да' или 'Нет'.")


def sort_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате, если пользователь согласен."""
    if not ask_yes_no("Отсортировать операции по дате?"):
        return transactions

    order = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
    reverse = order != "по возрастанию"
    return sort_by_date(transactions, reverse=reverse)


def filter_ruble_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Оставляет только рублёвые транзакции, если пользователь согласен."""
    if not ask_yes_no("Выводить только рублевые транзакции?"):
        return transactions
    # Для JSON формат: currency -> code
    return [t for t in transactions if
            t.get("currency_code") == "RUB" or
            t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"]


def filter_by_description(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по слову в описании, если пользователь согласен."""
    if not ask_yes_no("Отфильтровать список транзакций по определенному слову в описании?"):
        return transactions
    word = input("Введите слово для поиска: ").strip()
    if not word:
        return transactions
    return process_bank_search(transactions, word)


def format_transaction_for_output(transaction: Dict[str, Any]) -> str:
    """Форматирует одну транзакцию для вывода в консоль."""
    # Получаем дату (разный формат для разных источников)
    date_str = transaction.get("date", "")
    if date_str and "T" in date_str:
        date_str = get_date(date_str)
    elif not date_str:
        date_str = "Дата не указана"

    description = transaction.get("description", "")

    # Получаем сумму и валюту (разный формат для разных источников)
    if "operationAmount" in transaction:  # JSON формат
        amount = float(transaction["operationAmount"].get("amount", 0))
        currency = transaction["operationAmount"].get("currency", {}).get("code", "")
    else:  # CSV/Excel формат
        amount = float(transaction.get("amount", 0))
        currency = transaction.get("currency_code", "")

    currency_display = "руб." if currency == "RUB" else currency

    from_acc = transaction.get("from")
    to_acc = transaction.get("to")

    if from_acc and to_acc:
        transfer_str = f"{mask_account_card(from_acc)} -> {mask_account_card(to_acc)}"
    elif to_acc:
        transfer_str = mask_account_card(to_acc)
    elif from_acc:
        transfer_str = mask_account_card(from_acc)
    else:
        transfer_str = ""

    lines = [f"{date_str} {description}", transfer_str, f"Сумма: {amount} {currency_display}", ""]
    return "\n".join(lines)


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Выводит список транзакций в консоль."""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}")
    for t in transactions:
        print(format_transaction_for_output(t))


def main() -> None:
    """Главная функция программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    try:
        choice = int(input().strip())
    except ValueError:
        print("Некорректный ввод. Завершение программы.")
        return

    transactions = load_transactions(choice)

    if not transactions:
        print("Не удалось загрузить данные. Завершение программы.")
        return

    status = get_valid_status()
    filtered_by_state = filter_by_state(transactions, state=status)

    sorted_transactions = sort_transactions(filtered_by_state)

    ruble_transactions = filter_ruble_transactions(sorted_transactions)

    final_transactions = filter_by_description(ruble_transactions)

    print("Распечатываю итоговый список транзакций...")
    print_transactions(final_transactions)


if __name__ == "__main__":
    main()