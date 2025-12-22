from typing import Union


def get_mask_card_number(card_number: str) -> str:
    """Получает число с номером кредитной карты и формирует её маску вида
    XXXX XX** **** XXXX. Первая шестерка символов видима,
    последние четыре также остаются открытыми, остальное скрыто символом '*'.
    Блокировка идет каждые четыре символа. Args: card_number (str):
    Номер кредитной карты длиной ровно 16 цифр. Raises: ValueError:
    Если длина не равна 16 или карта содержит недопустимые символы.
    Returns: str: Маскированная строка номера карты.
    """
    card_str = str(card_number)
    if len(card_str) != 16 or not card_str.isdigit():
        raise ValueError("Неверный формат номера карты")

    masked_part = "**"
    return f"{card_str[:4]} {card_str[4:6]} ** {masked_part} {card_str[-4:]}"


print(get_mask_card_number(1234_5678_90))


def get_mask_account(account_number: str) -> str:
    """Формирует маску банковского счёта вида **XXXX,
    показывая только последнюю четверку символов. Args: account_number (str):
    Номер банковского счёта длиной больше или равной 4 цифрам. Raises: ValueError:
    Если счёт короче четырёх символов или содержит нецифровые символы. Returns: str:
    Маскированная строка номера счёта."""
    acc_str = str(account_number)
    if len(acc_str) < 4 or not acc_str.isdigit():
        raise ValueError("Неверный формат номера счёта")

    return f"**{acc_str[-4:]}"
