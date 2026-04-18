from unittest.mock import patch

import pandas as pd

from src.data_readers import read_transactions_from_csv, read_transactions_from_excel


@patch("src.data_readers.pd.read_csv")
@patch("src.data_readers.os.path.exists")
def test_csv_successful_reading(mock_exists, mock_read_csv):
    """Тест на успешное чтение CSV файла"""
    mock_exists.return_value = True
    # Создание тестового датафрейма
    test_df = pd.DataFrame(
        {
            "id": [650703, 3598919],
            "state": ["EXECUTED", "EXECUTED"],
            "date": ["2023-09-05T11:30:32Z", "2020-12-06T23:00:58Z"],
            "amount": [16210, 29740],
            "currency_name": ["Sol", "Peso"],
            "currency_code": ["PEN", "COP"],
            "from": ["Счет 58803664561298323391", "Discover 3172601889670065"],
            "to": ["Счет 39745660563456619397", "Discover 0720428384694643"],
            "description": ["Перевод организации", "Перевод с карты на карту"],
        }
    )
    mock_read_csv.return_value = test_df
    result = read_transactions_from_csv("data/transactions.csv")
    # Проверка, что read_csv вызван с правильным разделителем
    mock_read_csv.assert_called_once_with("data/transactions.csv", delimiter=";")
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], dict)
    assert result[0]["id"] == 650703
    assert result[0]["state"] == "EXECUTED"
    assert result[0]["currency_code"] == "PEN"


@patch("src.data_readers.os.path.exists")
def test_csv_file_not_found(mock_exists):
    """Тест при отсутствии файла"""
    mock_exists.return_value = False
    result = read_transactions_from_csv("somefile.csv")
    assert result == []


@patch("src.data_readers.pd.read_csv")
@patch("src.data_readers.os.path.exists")
def test_csv_wrong_extension(mock_exists, mock_read_csv):
    """Тест с неправильным расширением файла"""
    mock_exists.return_value = True
    result = read_transactions_from_csv("data/file.txt")
    mock_read_csv.assert_not_called()
    assert result == []


@patch("src.data_readers.pd.read_csv")
@patch("src.data_readers.os.path.exists")
def test_csv_empty_dataframe(mock_exists, mock_read_csv):
    """Тест на пустой CSV-файл"""
    mock_exists.return_value = True
    empty_df = pd.DataFrame()
    mock_read_csv.return_value = empty_df
    result = read_transactions_from_csv("data/empty.csv")
    mock_read_csv.assert_called_once_with("data/empty.csv", delimiter=";")
    assert result == []


@patch("src.data_readers.pd.read_excel")
@patch("src.data_readers.os.path.exists")
def test_excel_successful_reading(mock_exists, mock_read_excel):
    """Тест на успешное чтение Excel файла"""
    mock_exists.return_value = True
    # Создание тестового датафрейма
    test_df = pd.DataFrame(
        {
            "id": [650703, 3598919],
            "state": ["EXECUTED", "EXECUTED"],
            "date": ["2023-09-05T11:30:32Z", "2020-12-06T23:00:58Z"],
            "amount": [16210, 29740],
            "currency_name": ["Sol", "Peso"],
            "currency_code": ["PEN", "COP"],
            "from": ["Счет 58803664561298323391", "Discover 3172601889670065"],
            "to": ["Счет 39745660563456619397", "Discover 0720428384694643"],
            "description": ["Перевод организации", "Перевод с карты на карту"],
        }
    )
    mock_read_excel.return_value = test_df
    result = read_transactions_from_excel("data/transactions.xlsx")
    mock_read_excel.assert_called_once_with("data/transactions.xlsx")
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["id"] == 650703
    assert result[0]["currency_name"] == "Sol"


@patch("src.data_readers.os.path.exists")
def test_excel_file_not_found(mock_exists):
    """Тест при отсутствии файла"""
    mock_exists.return_value = False
    result = read_transactions_from_excel("nonexistent.xlsx")
    assert result == []


@patch("src.data_readers.pd.read_excel")
@patch("src.data_readers.os.path.exists")
def test_excel_wrong_extension(mock_exists, mock_read_excel):
    """Тест с неправильным расширением файла"""
    mock_exists.return_value = True
    result = read_transactions_from_excel("data/file.csv")
    mock_read_excel.assert_not_called()
    assert result == []


@patch("src.data_readers.pd.read_excel")
@patch("src.data_readers.os.path.exists")
def test_excel_empty_dataframe(mock_exists, mock_read_excel):
    """Тест: на пустой Excel файл"""
    mock_exists.return_value = True
    empty_df = pd.DataFrame()
    mock_read_excel.return_value = empty_df
    result = read_transactions_from_excel("data/empty.xlsx")
    mock_read_excel.assert_called_once_with("data/empty.xlsx")
    assert result == []