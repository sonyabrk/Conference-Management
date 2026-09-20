"""Загрузка и сохранение данных проекта в JSON-файлах.

В JSON хранятся только данные и идентификаторы связей
(conference_id, section_id), а не сами объекты.
"""

from __future__ import annotations

import json
import os

from models import Conference, Section, Talk
from models.conferences import find_conference_by_id
from models.sections import find_section_by_id


def _read_json(filename: str, title: str) -> list[dict]:
    """Прочитать JSON-список; при проблемах вернуть пустой список."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, начинаем с пустого списка {title}.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, начинаем с пустого списка {title}.")
        return []

    if not isinstance(data, list):
        print(f"Файл {filename} имеет неверный формат, список {title} пуст.")
        return []
    return data


def _write_json(filename: str, data: list[dict]) -> None:
    """Записать список словарей в JSON-файл."""
    folder = os.path.dirname(filename)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_conferences(filename: str) -> list[Conference]:
    """Загрузить конференции: JSON -> объекты Conference."""
    conferences: list[Conference] = []
    for item in _read_json(filename, "конференций"):
        try:
            conferences.append(Conference.from_data(item))
        except (KeyError, TypeError):
            print(f"Пропущена некорректная запись конференции: {item}")
    return conferences


def save_conferences(filename: str, conferences: list[Conference]) -> None:
    """Сохранить конференции: объекты Conference -> JSON."""
    _write_json(filename, [conference.to_dict() for conference in conferences])


def load_sections(filename: str, conferences: list[Conference]) -> list[Section]:
    """Загрузить секции и восстановить связь с объектами Conference."""
    sections: list[Section] = []
    for item in _read_json(filename, "секций"):
        try:
            conference = find_conference_by_id(conferences, item["conference_id"])
            if conference is None:
                print(f"Пропущена секция {item.get('id')}: конференция не найдена.")
                continue
            sections.append(Section.from_data(item, conference))
        except (KeyError, TypeError):
            print(f"Пропущена некорректная запись секции: {item}")
    return sections


def save_sections(filename: str, sections: list[Section]) -> None:
    """Сохранить секции: объекты Section -> JSON (со ссылкой conference_id)."""
    _write_json(filename, [section.to_dict() for section in sections])


def load_talks(filename: str, sections: list[Section]) -> list[Talk]:
    """Загрузить заявки и восстановить связь с объектами Section."""
    talks: list[Talk] = []
    for item in _read_json(filename, "докладов"):
        try:
            section = find_section_by_id(sections, item["section_id"])
            if section is None:
                print(f"Пропущена заявка {item.get('id')}: секция не найдена.")
                continue
            talks.append(Talk.from_data(item, section))
        except (KeyError, TypeError):
            print(f"Пропущена некорректная запись доклада: {item}")
    return talks


def save_talks(filename: str, talks: list[Talk]) -> None:
    """Сохранить заявки: объекты Talk -> JSON (со ссылкой section_id)."""
    _write_json(filename, [talk.to_dict() for talk in talks])
