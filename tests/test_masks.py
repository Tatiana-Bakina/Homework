import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, masked_card_number",
    [
        (2202202506920674, "2202 20** **** 0674"),
        (1234567887654321, "1234 56** **** 4321"),
        (1111111111111111, "1111 11** **** 1111"),
    ],
)
def test_get_mask_card_number(card_number, masked_card_number):
    """Тестирует маскировку номера карты (параметризованный)."""
    assert get_mask_card_number(card_number) == masked_card_number


@pytest.mark.parametrize(
    "account_number, masked_account_number",
    [(40817810769001554309, "**4309"), (11111111111111111111, "**1111"), (123456789, "**6789")],
)
def test_get_mask_account(account_number, masked_account_number):
    """Тестирует маскировку номера счёта"""
    assert get_mask_account(account_number) == masked_account_number
