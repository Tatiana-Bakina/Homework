import os

import pandas as pd


def read_transactions_from_csv(filepath: str) -> list[dict]:
    """
    Считывает финансовые операции из CSV-файла.
    Аргументы:
        filepath (str): путь к CSV-файлу
    Возвращает:
        list[dict]: список словарей с транзакциями
    """
    if not os.path.exists(filepath):
        print(f"Ошибка: Файл {filepath} не найден.")
        return []
    if not filepath.lower().endswith(".csv"):
        print(f"Ошибка: Файл {filepath} не является CSV-файлом")
        return []
    try:
        df = pd.read_csv(filepath, delimiter=';')
        if df.empty:
            print(f"Ошибка: Файл {filepath} пустой.")
            return []

        transactions_list = df.to_dict("records")
        return transactions_list

    except Exception as e:
        print(f"Ошибка при чтении файла '{filepath}': {e}")
        return []


def read_transactions_from_excel(filepath: str) -> list[dict]:
    """
    Считывает финансовые операции из Excel-файла.
    Аргументы:
        filepath (str): путь к Excel-файлу
    Возвращает:
        list[dict]: список словарей с транзакциями
    """
    if not os.path.exists(filepath):
        print(f"Ошибка: Файл {filepath} не найден.")
        return []
    if not (filepath.lower().endswith(".xls") or filepath.lower().endswith(".xlsx")):
        print(f"Ошибка: Файл {filepath} не является Excel-файлом. " f"Поддерживаются расширения .xls и .xlsx")
        return []
    try:
        df = pd.read_excel(filepath)
        if df.empty:
            print(f"Ошибка: Файл {filepath} пустой.")
            return []

        transactions_list = df.to_dict("records")
        return transactions_list

    except Exception as e:
        print(f"Ошибка при чтении файла '{filepath}': {e}")
        return []
