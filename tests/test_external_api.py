import pytest
from unittest.mock import patch, Mock
import os
from src.external_api import convert_amount_to_rub, _convert_currency


def test_convert_amount_to_rub_rub():
    """Тест конвертации рублевой транзакции."""
    transaction = {"amount": "100.50", "currency": "RUB"}

    result = convert_amount_to_rub(transaction)
    assert result == 100.50
    assert isinstance(result, float)


def test_convert_amount_to_rub_usd():
    """Тест конвертации USD транзакции."""
    transaction = {"amount": "100.0", "currency": "USD"}

    with patch("src.external_api._convert_currency") as mock_convert:
        mock_convert.return_value = 9000.0
        result = convert_amount_to_rub(transaction)

        assert result == 9000.0
        mock_convert.assert_called_once_with(100.0, "USD")


def test_convert_amount_to_rub_eur():
    """Тест конвертации EUR транзакции."""
    transaction = {"amount": "50.0", "currency": "EUR"}

    with patch("src.external_api._convert_currency") as mock_convert:
        mock_convert.return_value = 5000.0
        result = convert_amount_to_rub(transaction)

        assert result == 5000.0
        mock_convert.assert_called_once_with(50.0, "EUR")


def test_convert_amount_to_rub_invalid_amount():
    """Тест конвертации с некорректной суммой."""
    transaction = {"amount": "not_a_number", "currency": "RUB"}

    result = convert_amount_to_rub(transaction)
    assert result == 0.0


@patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_api_key"})
@patch("src.external_api.requests.get")
def test_convert_currency_success(mock_get):
    """Тест успешной конвертации через API."""
    # Настраиваем mock ответ
    mock_response = Mock()
    mock_response.json.return_value = {"success": True, "result": 9000.0}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = _convert_currency(100.0, "USD")

    assert result == 9000.0
    mock_get.assert_called_once()


@patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_api_key"})
@patch("src.external_api.requests.get")
def test_convert_currency_api_failure(mock_get):
    """Тест конвертации при ошибке API."""
    mock_get.side_effect = Exception("API error")

    result = _convert_currency(100.0, "USD")

    # Должен использоваться фиксированный курс
    assert result == 100.0 * 90.0  # USD фиксированный курс
