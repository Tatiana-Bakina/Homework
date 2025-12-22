def get_mask_card_number(card_number: int) -> str:
    """
    Функция получает номер банковской карты и возвращает её маской формата 'XXXX XX** **** XXXX'.

    :param card_number: Целое число — номер карты
    :return: Строка с маской номера карты
    """
    number_str = (
        f"{card_number:016d}"  # Приводим к строке фиксированной длины 16 символов
    )
    return f"{number_str[:4]} {number_str[4:6]}** **** {number_str[-4:]}"


def get_mask_account(account_number: int) -> str:
    """
    Функция получает номер банковского счёта и возвращает его маской формата '**XXXX'.

    :param account_number: Целое число — номер счёта
    :return: Строка с маской номера счёта
    """
    number_str = f"{account_number:d}"  # Преобразуем целое число в строку
    return f"**{number_str[-4:]}"