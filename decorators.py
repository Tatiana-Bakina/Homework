import time
from functools import wraps
from typing import Optional, Callable, Any


def log(filename: Optional[str] = None):
    """
    Декорирует функцию, логируя время начала и конца выполнения,
    а также обрабатывая ошибки.

    Параметры:
    - filename (Optional[str], default=None): Имя файла для записи логов.
      Если не задана, выводит логи в консоль.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"
                output_message(message, filename)
                return result
            except Exception as e:
                error_message = f"{func.__name__} error: {type(e).__name__}. " f"Inputs: {args}, {kwargs}"
                output_message(error_message, filename)
                raise e
            finally:
                end_time = time.time()
                duration = round(end_time - start_time, 4)
                performance_message = f"{func.__name__} took {duration}s to execute."
                output_message(performance_message, filename)

        return wrapper

    return decorator


def output_message(message: str, filename: Optional[str]) -> None:
    """
    Функция для вывода сообщений либо в файл, либо в консоль.
    """
    if filename is not None:
        with open(filename, "a") as f:
            f.write(message + "\n")
    else:
        print(message)
