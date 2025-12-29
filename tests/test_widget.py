import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "account_card, masked_account_card",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(account_card, masked_account_card):
    """Тестирует работу функции mask_account_card"""
    assert mask_account_card(account_card) == masked_account_card


def test_mask_account_card_errors():
    """Тестирует вывод ошибок при некорректных вводных данных."""
    # Проверка на отсутствие номера карты/счета
    with pytest.raises(ValueError, match="Некорректный ввод"):
        mask_account_card("Счет")

    # Проверка на нецифровой номер
    with pytest.raises(ValueError, match="Некорректный номер карты/счета"):
        mask_account_card("Visa 1234qwerty")


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2022-05-12T08:45:18.154532", "12.05.2022"),
    ],
)
def test_get_date(date_str, expected):
    """Тестирует преобразование даты."""
    assert get_date(date_str) == expected
