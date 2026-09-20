"""Класс Talk и функции работы с заявками на доклады."""

from __future__ import annotations

from .sections import Section


class Talk:
    """Заявка на доклад в секции конференции."""

    def __init__(
        self,
        talk_id: int,
        section: Section,
        author: str,
        title: str,
        time_slot: str,
    ) -> None:
        """Создать заявку. section — объект Section, а не его id."""
        self.id = talk_id
        self.section = section
        self.author = author
        self.title = title
        self.time_slot = time_slot
        self.is_cancelled = False

    def cancel(self) -> None:
        """Отменить заявку (объект остаётся в коллекции)."""
        self.is_cancelled = True

    def blocks_slot(self, section: Section, time_slot: str) -> bool:
        """Блокирует ли эта заявка тайм-слот: активна, та же секция и время."""
        return (
            not self.is_cancelled
            and self.section.id == section.id
            and self.time_slot == time_slot
        )

    def to_dict(self) -> dict:
        """Преобразовать заявку в данные для JSON (связь — по id)."""
        return {
            "id": self.id,
            "section_id": self.section.id,
            "author": self.author,
            "title": self.title,
            "time_slot": self.time_slot,
            "is_cancelled": self.is_cancelled,
        }

    @classmethod
    def from_data(cls, data: dict, section: Section) -> Talk:
        """Создать заявку из словаря и найденного объекта секции."""
        talk = cls(
            talk_id=data["id"],
            section=section,
            author=data["author"],
            title=data["title"],
            time_slot=data["time_slot"],
        )
        talk.is_cancelled = data.get("is_cancelled", False)
        return talk

    def __str__(self) -> str:
        """Вернуть строковое представление заявки с учётом состояния."""
        status = " [отменена]" if self.is_cancelled else ""
        return (
            f"{self.id}. {self.title} — {self.author} "
            f"(секция «{self.section.name}», слот {self.time_slot}){status}"
        )


def is_slot_available(talks: list[Talk], section: Section, time_slot: str) -> bool:
    """Свободен ли тайм-слот: отменённые заявки слот не блокируют."""
    return not any(talk.blocks_slot(section, time_slot) for talk in talks)


def create_talk_submission(
    talks: list[Talk],
    section: Section,
    author: str,
    title: str,
    time_slot: str,
) -> Talk | None:
    """Создать заявку и добавить её в коллекцию.

    Возвращает None, если слот занят или в секции нет свободных мест.
    """
    if not is_slot_available(talks, section, time_slot):
        return None
    if not section.has_free_slots(talks):
        return None

    new_id = max((talk.id for talk in talks), default=0) + 1
    talk = Talk(new_id, section, author, title, time_slot)
    talks.append(talk)
    return talk


def find_talk_by_id(talks: list[Talk], talk_id: int) -> Talk | None:
    """Найти заявку по идентификатору."""
    for talk in talks:
        if talk.id == talk_id:
            return talk
    return None


def cancel_talk_submission(talks: list[Talk], talk_id: int) -> bool:
    """Отменить заявку по id, не удаляя её из коллекции.

    Возвращает False, если заявка не найдена или уже отменена.
    """
    talk = find_talk_by_id(talks, talk_id)
    if talk is None or talk.is_cancelled:
        return False
    talk.cancel()
    return True


def get_submission_status(is_available: bool) -> str:
    """Вернуть текстовый статус тайм-слота."""
    if is_available:
        return "Слот доступен для доклада"
    return "Слот уже занят"


def show_talks(talks: list[Talk]) -> None:
    """Вывести список заявок на доклады."""
    if not talks:
        print("Доклады пока не добавлены.")
        return
    for talk in talks:
        print(talk)
