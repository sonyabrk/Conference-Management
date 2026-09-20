"""Класс Section и функции работы с секциями."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

from .conferences import Conference

if TYPE_CHECKING:
    from .talks import Talk


class Section:
    """Секция конференции с ограниченной вместимостью."""

    def __init__(
        self,
        section_id: int,
        name: str,
        conference: Conference,
        capacity: int,
    ) -> None:
        """Создать секцию. capacity — максимум докладов."""
        self.id = section_id
        self.name = name
        self.conference = conference
        self.capacity = capacity

    @staticmethod
    def validate_capacity(capacity: int) -> bool:
        """Проверить корректность вместимости (должна быть > 0)."""
        return capacity > 0

    def free_slots(self, talks: list[Talk]) -> int:
        """Сколько докладов ещё помещается (отменённые не считаются)."""
        used = sum(
            1
            for talk in talks
            if talk.section.id == self.id and not talk.is_cancelled
        )
        return self.capacity - used

    def has_free_slots(self, talks: list[Talk], min_free: int = 1) -> bool:
        """Проверить, что свободно не меньше min_free мест."""
        return self.free_slots(talks) >= min_free

    def matches(self, query: str) -> bool:
        """Проверить, содержит ли название подстроку (без учёта регистра)."""
        return query.lower() in self.name.lower()

    def to_dict(self) -> dict:
        """Преобразовать секцию в данные для JSON (связь — по id)."""
        return {
            "id": self.id,
            "name": self.name,
            "conference_id": self.conference.id,
            "capacity": self.capacity,
        }

    @classmethod
    def from_data(cls, data: dict, conference: Conference) -> Section:
        """Создать секцию из словаря и уже найденного объекта конференции."""
        return cls(
            section_id=data["id"],
            name=data["name"],
            conference=conference,
            capacity=data["capacity"],
        )

    def __str__(self) -> str:
        """Вернуть строковое представление секции."""
        return (
            f"{self.id}. {self.name} "
            f"(конференция «{self.conference.name}», вместимость {self.capacity})"
        )


def add_section(
    sections: list[Section],
    name: str,
    conference: Conference,
    capacity: int,
) -> Section:
    """Создать секцию, добавить в коллекцию и вернуть её.

    Если вместимость некорректна, выбрасывает ValueError.
    """
    if not Section.validate_capacity(capacity):
        raise ValueError("вместимость секции должна быть больше нуля")
    new_id = max((section.id for section in sections), default=0) + 1
    section = Section(new_id, name, conference, capacity)
    sections.append(section)
    return section


def find_section(sections: list[Section], query: str) -> list[Section]:
    """Найти секции по подстроке названия."""
    return [section for section in sections if section.matches(query)]


def find_section_by_id(sections: list[Section], section_id: int) -> Section | None:
    """Найти секцию по идентификатору."""
    for section in sections:
        if section.id == section_id:
            return section
    return None


def check_section_capacity(
    sections: list[Section],
    talks: list[Talk],
    section_id: int,
) -> int:
    """Вернуть число свободных мест в секции.

    Если секция не найдена, выбрасывает ValueError.
    """
    section = find_section_by_id(sections, section_id)
    if section is None:
        raise ValueError(f"секция с id={section_id} не найдена")
    return section.free_slots(talks)


def filter_sections_by_capacity(
    sections: list[Section],
    talks: list[Talk],
    min_free_slots: int,
) -> Iterator[Section]:
    """Генератор секций, где свободно не меньше min_free_slots мест."""
    for section in sections:
        if section.has_free_slots(talks, min_free_slots):
            yield section


def sort_sections(sections: list[Section]) -> list[Section]:
    """Отсортировать секции по вместимости (по убыванию)."""
    return sorted(sections, key=lambda section: section.capacity, reverse=True)


def show_sections(sections: list[Section]) -> None:
    """Вывести список секций."""
    if not sections:
        print("Секции пока не добавлены.")
        return
    for section in sections:
        print(section)
