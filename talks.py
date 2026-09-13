"""Функции для работы с заявками на доклады (talks)."""


def is_slot_available(
    talks: list[dict],
    section_id: int,
    time_slot: str,
) -> bool:
    """Проверить, свободен ли тайм-слот в секции.

    Возвращает False, если в этой секции на это время
    уже есть доклад.
    """
    for talk in talks:
        if talk["section_id"] == section_id and talk["time_slot"] == time_slot:
            return False
    return True


def create_talk_submission(
    talks: list[dict],
    section_id: int,
    author: str,
    title: str,
    time_slot: str,
) -> dict | None:
    """Создать заявку на доклад.

    Проверяет доступность слота и добавляет запись в talks.
    Если слот занят, возвращает None и заявка не создаётся.
    """
    if not is_slot_available(talks, section_id, time_slot):
        return None

    new_id = max((talk["id"] for talk in talks), default=0) + 1
    submission = {
        "id": new_id,
        "section_id": section_id,
        "author": author,
        "title": title,
        "time_slot": time_slot,
    }
    talks.append(submission)
    return submission


def cancel_talk_submission(talks: list[dict], talk_id: int) -> bool:
    """Отменить заявку на доклад по идентификатору.

    Возвращает True, если заявка найдена и удалена,
    иначе False.
    """
    for talk in talks:
        if talk["id"] == talk_id:
            talks.remove(talk)
            return True
    return False


def get_submission_status(is_available: bool) -> str:
    """Вернуть текстовый статус тайм-слота (функция из ПР1)."""
    if is_available:
        return "Слот доступен для доклада"
    return "Слот уже занят"