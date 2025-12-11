import pytest
from main import (
    read_json, get_from_and_to_number, format_date,
    amount_info
)

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
