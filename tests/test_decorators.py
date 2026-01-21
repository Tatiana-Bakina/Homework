import pytest
from decorators import log


# Тестируем успешное выполнение функции
def test_log_success(capsys):
    """
    Проверяет, что декоратор log корректно регистрирует успешное завершение функции.
    """

    @log()  # Применяем декоратор log к нашей тестовой функции
    def successful_function():
        pass  # Простая пустая функция, которая ничего не делает

    successful_function()  # Вызываем нашу функцию, обернутую декоратором

    # Читаем вывод, сделанный функцией в ходе своего выполнения
    captured = capsys.readouterr()  # Получаем вывод из stdout и stderr

    # Проверяем, что в выводе присутствует фраза "completed successfully.", означающая успешное выполнение
    assert "completed successfully." in captured.out


# Тестируем обработку ошибок в функции
def test_log_failure():
    """
    Проверяет, что декоратор log корректно регистрирует возникновение ошибки.
    """

    @log()  # Применяем декоратор log к нашей тестовой функции
    def failing_function():
        raise ValueError("Something went wrong!")  # Искусственно генерируем ошибку

    # Проверяем, что ожидаемая ошибка действительно возникла
    with pytest.raises(ValueError):
        failing_function()  # Вызываем функцию, ожидая появления ошибки
