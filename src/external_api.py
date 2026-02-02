import requests
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


def convert_amount_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными о транзакции

    Returns:
        Сумма в рублях (float)
    """
    try:
        amount = float(transaction.get("amount", 0))
        currency = transaction.get("currency", "RUB")

        # Если валюта уже в рублях, возвращаем как есть
        if currency == "RUB":
            return amount

        # Если валюта в USD или EUR, конвертируем
        if currency in ["USD", "EUR"]:
            return _convert_currency(amount, currency)

        # Для других валют возвращаем как есть (или можно добавить логику)
        return amount

    except (ValueError, TypeError, KeyError):
        return 0.0


def _convert_currency(amount: float, from_currency: str) -> float:
    """
    Конвертирует сумму из указанной валюты в рубли.

    Args:
        amount: Сумма для конвертации
        from_currency: Исходная валюта (USD или EUR)

    Returns:
        Сумма в рублях
    """
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables")

    url = f"https://api.apilayer.com/exchangerates_data/convert"

    params = {"from": from_currency, "to": "RUB", "amount": amount}

    headers = {"apikey": api_key}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("success"):
            return float(data["result"])
        else:
            # Если API вернуло ошибку, используем фиксированный курс
            return _get_fallback_rate(amount, from_currency)

    except (requests.RequestException, KeyError, ValueError):
        # В случае ошибки используем фиксированный курс
        return _get_fallback_rate(amount, from_currency)


def _get_fallback_rate(amount: float, currency: str) -> float:
    """
    Возвращает сумму по фиксированному курсу (резервный вариант).

    Args:
        amount: Сумма для конвертации
        currency: Исходная валюта

    Returns:
        Сумма в рублях по фиксированному курсу
    """
    # Фиксированные курсы (примерные значения)
    rates = {"USD": 90.0, "EUR": 100.0}  # 1 USD = 90 RUB  # 1 EUR = 100 RUB

    return amount * rates.get(currency, 1.0)
