import pytest
import json
import os
import tempfile
from unittest.mock import mock_open, patch
from src.utils import load_transactions_from_json


def test_load_transactions_valid_file():
    """Тест загрузки корректного JSON файла."""
    test_data = [{"id": 1, "amount": 100.0, "currency": "RUB", "description": "Test transaction"}]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name

    try:
        result = load_transactions_from_json(temp_path)
        assert result == test_data
    finally:
        os.unlink(temp_path)


def test_load_transactions_file_not_found():
    """Тест загрузки несуществующего файла."""
    result = load_transactions_from_json("non_existent_file.json")
    assert result == []


def test_load_transactions_empty_file():
    """Тест загрузки пустого файла."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        temp_path = f.name

    try:
        result = load_transactions_from_json(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


def test_load_transactions_not_json():
    """Тест загрузки некорректного JSON."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("not a json content")
        temp_path = f.name

    try:
        result = load_transactions_from_json(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


def test_load_transactions_not_list():
    """Тест загрузки JSON, который не является списком."""
    test_data = {"id": 1, "amount": 100.0}

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name

    try:
        result = load_transactions_from_json(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)
