import json
import logging
import os
from typing import Any, Dict, List, Optional

# Создаём логер
logger = logging.getLogger("utils")

# Создаем папку logs, если она отсутствует
if not os.path.exists("logs"):
    os.makedirs("logs")

# Создаем обработчик
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")

# Создаем форматер для логов
file_formatter = logging.Formatter(
    fmt="%(asctime)s | %(name)s | %(levelname)-8s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Устанавливаем форматер для обработчика
file_handler.setFormatter(file_formatter)

# Добавляем обработчик к логеру
logger.addHandler(file_handler)

# Устанавливаем минимальный уровень логирования
logger.setLevel(logging.DEBUG)


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу с транзакциями

    Returns:
        Список словарей с данными о транзакциях
    """
    logger.debug(f"Начинаем загрузку файла: {file_path}")

    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            logger.warning(f"Файл не существует: {file_path}")
            return []

        # Проверяем, не пустой ли файл
        if os.path.getsize(file_path) == 0:
            logger.warning(f"Файл пуст: {file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if not isinstance(data, list):
            logger.error(f"Неверный формат: ожидается список, получен {type(data).__name__}")
            return []

        logger.info(f"Успешно загружено {len(data)} транзакций из файла {file_path}")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка JSON в файле {file_path}: {e}")  # ← ДОБАВИТЬ
        return []
    except IOError as e:
        logger.error(f"Ошибка ввода-вывода при чтении файла {file_path}: {e}")
        return []
    except OSError as e:
        logger.error(f"Системная ошибка при доступе к файлу {file_path}: {e}")
        return []
    except Exception as e:
        logger.critical(f"Неожиданная ошибка: {type(e).__name__}: {e}")
        return []
