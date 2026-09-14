"""Функции сохранения и загрузки данных проекта в JSON-файлах."""

import json


def load_conferences(filename: str) -> dict[int, dict]:
    """Загрузить конференции из JSON-файла.

    При отсутствии файла или повреждённом JSON
    возвращает пустой словарь.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, начинаем с пустого списка конференций.")
        return {}
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, начинаем с пустого списка конференций.")
        return {}

    return {int(key): value for key, value in data.items()}


def save_conferences(filename: str, conferences: dict[int, dict]) -> None:
    """Сохранить конференции в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(conferences, file, ensure_ascii=False, indent=2)


def load_sections(filename: str) -> dict[int, dict]:
    """Загрузить секции из JSON-файла.

    При отсутствии файла или повреждённом JSON
    возвращает пустой словарь.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, начинаем с пустого списка секций.")
        return {}
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, начинаем с пустого списка секций.")
        return {}

    return {int(key): value for key, value in data.items()}


def save_sections(filename: str, sections: dict[int, dict]) -> None:
    """Сохранить секции в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(sections, file, ensure_ascii=False, indent=2)


def load_talks(filename: str) -> list[dict]:
    """Загрузить заявки на доклады из JSON-файла.

    При отсутствии файла или повреждённом JSON
    возвращает пустой список.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, начинаем с пустого списка докладов.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, начинаем с пустого списка докладов.")
        return []


def save_talks(filename: str, talks: list[dict]) -> None:
    """Сохранить заявки на доклады в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(talks, file, ensure_ascii=False, indent=2)
