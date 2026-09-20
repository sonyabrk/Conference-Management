"""Класс Conference и функции работы с конференциями."""

from __future__ import annotations


class Conference:
    """Конференция, в рамках которой работают секции."""

    def __init__(self, conference_id: int, name: str) -> None:
        """Создать объект конференции."""
        self.id = conference_id
        self.name = name

    def matches(self, query: str) -> bool:
        """Проверить, содержит ли название подстроку (без учёта регистра)."""
        return query.lower() in self.name.lower()

    def to_dict(self) -> dict:
        """Преобразовать конференцию в данные для JSON."""
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_data(cls, data: dict) -> Conference:
        """Создать конференцию из словаря (например, из JSON)."""
        return cls(conference_id=data["id"], name=data["name"])

    def __str__(self) -> str:
        """Вернуть строковое представление конференции."""
        return f"{self.id}. {self.name}"


def add_conference(conferences: list[Conference], name: str) -> Conference:
    """Создать конференцию, добавить в коллекцию и вернуть её."""
    new_id = max((conf.id for conf in conferences), default=0) + 1
    conference = Conference(new_id, name)
    conferences.append(conference)
    return conference


def find_conference(conferences: list[Conference], query: str) -> list[Conference]:
    """Найти конференции по подстроке названия."""
    return [conf for conf in conferences if conf.matches(query)]


def find_conference_by_id(
    conferences: list[Conference],
    conference_id: int,
) -> Conference | None:
    """Найти конференцию по идентификатору."""
    for conference in conferences:
        if conference.id == conference_id:
            return conference
    return None


def show_conferences(conferences: list[Conference]) -> None:
    """Вывести список конференций."""
    if not conferences:
        print("Конференции пока не добавлены.")
        return
    for conference in conferences:
        print(conference)
