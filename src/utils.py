import json
from typing import List, Dict, Any, Optional
import os


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу с транзакциями

    Returns:
        Список словарей с данными о транзакциях
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            return []

        # Проверяем, не пустой ли файл
        if os.path.getsize(file_path) == 0:
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, IOError, OSError):
        return []
