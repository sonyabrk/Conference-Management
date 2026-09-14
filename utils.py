"""Вспомогательные функции для безопасного ввода данных."""

from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число.

    При некорректном вводе (не число) запрос повторяется.
    """
    while True:
        raw_value = input(prompt)
        try:
            return int(raw_value)
        except ValueError:
            print("Ошибка: введите целое число.")


def input_date(prompt: str, date_format: str = "%d.%m.%Y") -> date:
    """Запросить у пользователя дату.

    Формат по умолчанию — ДД.ММ.ГГГГ (например, 15.09.2026).
    При некорректном формате запрос повторяется.
    """
    while True:
        raw_value = input(prompt)
        try:
            return datetime.strptime(raw_value, date_format).date()
        except ValueError:
            print(f"Ошибка: введите дату в формате {date_format}.")
