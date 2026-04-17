import logging
import os

# Создаём логер
logger = logging.getLogger("masks")

# Создаем папку logs, если она отсутствует
if not os.path.exists("logs"):
    os.makedirs("logs")

# Создаем обработчик
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")

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


def get_mask_account(account_number: int) -> str:
    """
    Функция получает номер банковского счёта и возвращает его маской формата '**XXXX'.

    :param account_number: Целое число — номер счёта
    :return: Строка с маской номера счёта
    """
    logger.debug(f"Вызов get_mask_account с аргументом: {account_number}")

    try:
        number_str = f"{account_number:d}"
        result = f"**{number_str[-4:]}"

        logger.info(f"Успешно замаскирован номер счёта: {account_number} -> {result}")
        return result
    except Exception as e:
        logger.error(f"Ошибка в get_mask_account: {type(e).__name__}: {e}", exc_info=True)
        raise


def get_mask_card_number(card_number: int) -> str:
    """
    Функция получает номер банковской карты и возвращает её маской формата 'XXXX XX** **** XXXX'.

    :param card_number: Целое число — номер карты
    :return: Строка с маской номера карты
    """
    logger.debug(f"Вызов get_mask_card_number с аргументом: {card_number}")

    try:
        number_str = f"{card_number:016d}"
        result = f"{number_str[:4]} {number_str[4:6]}** **** {number_str[-4:]}"

        logger.info(f"Успешно замаскирован номер карты: {card_number} -> {result}")
        return result
    except Exception as e:
        logger.error(f"Ошибка в get_mask_card_number: {type(e).__name__}: {e}", exc_info=True)
        raise
