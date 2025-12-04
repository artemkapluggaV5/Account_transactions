import json
from datetime import datetime

executed_operations = []


def read_json():
    with open("operations.json", "r", encoding='utf-8') as file:
        operations = json.load(file)
        executed = [op for op in operations if op["state"] == "EXECUTED"]
        sort_operations = sorted(executed, key=lambda x: x["date"], reverse=True)[:5]
        for operation in sort_operations:
            executed_operations.append(operation)

    return executed_operations

def get_from_and_to_number(operation):
    def mask_number(data):
        if not data:
            return "Нет данных"

        name, number = data.rsplit(" ", 1)

        if name == "Счет":
            return f"{name} **{number[-4:]}"
        else:
            masked = number[:4] + " " + number[4:6] + "** **** " + number[-4:]
            return f"{name} {masked}"

    from_data = operation.get("from")
    to_data = operation.get("to")

    return mask_number(from_data), mask_number(to_data)

def format_date(operation):
    date_str = operation["date"]
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    return date_obj.strftime("%d.%m.%Y")


def amount_info(operation):
    amount = operation["operationAmount"]["amount"]
    currency = operation["operationAmount"]["currency"]["name"]
    return f"{amount} {currency}"

def display_info(operation):
    date = format_date(operation)
    description = operation.get("description")

    from_user, to_user = get_from_and_to_number(operation)

    amount = amount_info(operation)

    print(f"""
{date} {description}
{from_user} -> {to_user}
{amount}
""")

def main():
    operations = read_json()
    for operation in operations:
        display_info(operation)


main()