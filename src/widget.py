from datetime import datetime
from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(data: str) -> str:
    """
    Маскирует номер карты или счёта в строке.
    Принимает строку с типом и номером карты/счёта,
    возвращает строку с замаскированным номером.
    Args:
        data: Строка вида 'Visa Platinum 7000792289606361' или 'Счет 73654108430135874305'.
    Returns:
        Строка с замаскированным номером.
        Для карт: 'Visa Platinum 7000 79** **** 6361'.
        Для счетов: 'Счет **4305'.
    Raises:
        ValueError: Если формат строки некорректен или номер содержит нецифровые символы.
    """
    # Делим строку по последнему пробелу
    parts = data.rsplit(maxsplit=1)

    # Проверяем, чтобы в результате получилось ровно два элемента
    if len(parts) != 2:
        raise ValueError("Некорректный ввод")

    name_part, number_part = parts

    # Проверяем корректность номера
    if not number_part.isdigit():
        raise ValueError("Некорректный номер карты/счета")

    # Определяем, какой тип операции выполняем (маскировка карты или счета)
    if name_part.lower().startswith("счет"):
        masked_value = get_mask_account(int(number_part))
    else:
        masked_value = get_mask_card_number(int(number_part))

    return f"{name_part} {masked_value}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из ISO-формата в формат 'ДД.ММ.ГГГГ'.
    Args:
        date_string: Строка с датой в ISO-формате, например '2024-03-11T02:26:18.671407'.
    Returns:
        Строка с датой в формате 'ДД.ММ.ГГГГ', например '11.03.2024'.
    """
    dt = datetime.fromisoformat(date_string)
    return dt.strftime("%d.%m.%Y")