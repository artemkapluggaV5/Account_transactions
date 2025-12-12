import pytest
from unittest.mock import patch, mock_open
import json

from main import (
    read_json, get_from_and_to_number, format_date,
    amount_info, display_info
)

mock_json_data = json.dumps([
    {"state": "EXECUTED", "date": "2023-01-01T12:00:00.000000", "id": 1},
    {"state": "CANCELED", "date": "2023-01-02T12:00:00.000000", "id": 2},
    {"state": "EXECUTED", "date": "2023-01-05T12:00:00.000000", "id": 3}
])

def test_read_json():
    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        result = read_json()
        assert len(result) == 2
        assert result[0]['id'] == 3

def test_mask_account():
    operation = {"from": "Счет 12345678901234567890"}
    result, _ = get_from_and_to_number(operation)
    assert result == "Счет **7890"

def test_mask_card():
    operation = {"from": "Visa Gold 1234567890123456"}
    result, _ = get_from_and_to_number(operation)
    assert result == "Visa Gold 1234 56** **** 3456"

def test_no_data():
    operation = {"from": None}
    result, _ = get_from_and_to_number(operation)
    assert result == "Нет данных"

def test_format_date():
    operation = {"date": "2019-08-26T10:50:07.241075"}
    result = format_date(operation)
    assert result == "26.08.2019"

def test_amount_info():
    operation = {
        "operationAmount": {"amount": "12345.67", "currency": {"name": "руб."}}
    }
    result = amount_info(operation)
    assert result == "12345.67 руб."

def test_display_info(capsys):
    operation = {
        "date": "2019-08-26T10:50:07.241075",
        "description": "Тест",
        "from": "Счет 1234",
        "to": "Счет 5678",
        "operationAmount": {"amount": "100", "currency": {"name": "руб."}}
    }
    display_info(operation)
    captured = capsys.readouterr()

    assert "26.08.2019 Тест" in captured.out
    assert "Счет **1234 -> Счет **5678" in captured.out