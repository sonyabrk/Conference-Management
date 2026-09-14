"""Функции для работы с конференциями и секциями."""


def add_conference(conferences: dict[int, dict], name: str) -> int:
    """Добавить конференцию в словарь conferences.

    Возвращает идентификатор созданной конференции.
    """
    new_id = max(conferences.keys(), default=0) + 1
    conferences[new_id] = {"name": name}
    return new_id


def find_conference(conferences: dict[int, dict], query: str) -> dict[int, dict]:
    """Найти конференции по подстроке названия (без учёта регистра)."""
    query_lower = query.lower()
    return {
        conf_id: data
        for conf_id, data in conferences.items()
        if query_lower in data["name"].lower()
    }


def add_section(
    sections: dict[int, dict],
    name: str,
    conference_id: int,
    capacity: int,
) -> int:
    """Добавить секцию в словарь sections.

    capacity — максимальное число докладов, которые вмещает секция.
    Возвращает идентификатор созданной секции.
    """
    new_id = max(sections.keys(), default=0) + 1
    sections[new_id] = {
        "name": name,
        "conference_id": conference_id,
        "capacity": capacity,
    }
    return new_id


def find_section(sections: dict[int, dict], query: str) -> dict[int, dict]:
    """Найти секции по подстроке названия (без учёта регистра)."""
    query_lower = query.lower()
    return {
        section_id: data
        for section_id, data in sections.items()
        if query_lower in data["name"].lower()
    }


def check_section_capacity(
    sections: dict[int, dict],
    talks: list[dict],
    section_id: int,
) -> int:
    """Вернуть, сколько ещё докладов помещается в секцию.

    Считает уже поданные (не отменённые) доклады в секции
    и вычитает их из вместимости.
    """
    section = sections[section_id]
    used = sum(1 for talk in talks if talk["section_id"] == section_id)
    return section["capacity"] - used


def filter_sections_by_capacity(
    sections: dict[int, dict],
    talks: list[dict],
    min_free_slots: int,
):
    """Отобрать секции, в которых свободно не меньше min_free_slots мест.

    Реализовано как генератор: значения формируются по мере
    перебора секций, а не собираются сразу в список/словарь.
    """
    for section_id, data in sections.items():
        free = check_section_capacity(sections, talks, section_id)
        if free >= min_free_slots:
            yield section_id, data


def sort_sections(sections: dict[int, dict]) -> list[tuple[int, dict]]:
    """Отсортировать секции по вместимости (по убыванию).

    Возвращает список пар (id, данные_секции).
    """
    return sorted(
        sections.items(),
        key=lambda item: item[1]["capacity"],
        reverse=True,
    )
