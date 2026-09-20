"""Консольное приложение «Система управления конференциями»."""

from __future__ import annotations

from models import Conference, Section, Talk
from models.conferences import add_conference, find_conference_by_id, show_conferences
from models.sections import (
    add_section,
    check_section_capacity,
    filter_sections_by_capacity,
    find_section,
    find_section_by_id,
    show_sections,
    sort_sections,
)
from models.talks import (
    cancel_talk_submission,
    create_talk_submission,
    get_submission_status,
    is_slot_available,
    show_talks,
)
from storage import (
    load_conferences,
    load_sections,
    load_talks,
    save_conferences,
    save_sections,
    save_talks,
)
from utils import input_int

CONFERENCES_FILE = "data/conferences.json"
SECTIONS_FILE = "data/sections.json"
TALKS_FILE = "data/talks.json"

MENU = """
Система управления конференциями

1. Показать секции
2. Найти секцию по названию
3. Проверить свободные места в секции
4. Проверить доступность тайм-слота
5. Подать заявку на доклад
6. Отменить заявку
7. Показать доклады
8. Добавить конференцию
9. Добавить секцию
10. Отобрать секции по свободным местам
11. Показать конференции
12. Показать секции по убыванию вместимости
0. Выход
"""


def save_all(
    conferences: list[Conference],
    sections: list[Section],
    talks: list[Talk],
) -> None:
    """Сохранить все коллекции в JSON-файлы."""
    save_conferences(CONFERENCES_FILE, conferences)
    save_sections(SECTIONS_FILE, sections)
    save_talks(TALKS_FILE, talks)


def show_free_slots(sections: list[Section], talks: list[Talk]) -> None:
    """Сценарий: показать свободные места в секции."""
    section_id = input_int("ID секции: ")
    try:
        free = check_section_capacity(sections, talks, section_id)
    except ValueError:
        print("Секция не найдена.")
        return
    print(f"Свободно мест: {free}")


def check_slot(sections: list[Section], talks: list[Talk]) -> None:
    """Сценарий: проверить доступность тайм-слота."""
    section = find_section_by_id(sections, input_int("ID секции: "))
    if section is None:
        print("Секция не найдена.")
        return
    time_slot = input("Тайм-слот (например, 10:00): ")
    print(get_submission_status(is_slot_available(talks, section, time_slot)))


def create_new_talk(talks: list[Talk], sections: list[Section]) -> None:
    """Сценарий: подать заявку на доклад."""
    section = find_section_by_id(sections, input_int("ID секции: "))
    if section is None:
        print("Секция не найдена, заявка не создана.")
        return

    author = input("Автор доклада: ")
    title = input("Название доклада: ")
    time_slot = input("Тайм-слот: ")

    talk = create_talk_submission(talks, section, author, title, time_slot)
    if talk is None:
        print("Заявка не создана: слот занят или в секции нет свободных мест.")
        return
    print(f"Заявка создана, id={talk.id}")
    save_talks(TALKS_FILE, talks)


def cancel_talk(talks: list[Talk]) -> None:
    """Сценарий: отменить заявку."""
    talk_id = input_int("ID заявки для отмены: ")
    if cancel_talk_submission(talks, talk_id):
        print("Заявка отменена.")
        save_talks(TALKS_FILE, talks)
    else:
        print("Заявка не найдена или уже отменена.")


def create_new_conference(conferences: list[Conference]) -> None:
    """Сценарий: добавить конференцию."""
    name = input("Название конференции: ")
    conference = add_conference(conferences, name)
    print(f"Конференция добавлена, id={conference.id}")
    save_conferences(CONFERENCES_FILE, conferences)


def create_new_section(
    conferences: list[Conference],
    sections: list[Section],
) -> None:
    """Сценарий: добавить секцию в существующую конференцию."""
    name = input("Название секции: ")
    conference = find_conference_by_id(conferences, input_int("ID конференции: "))
    if conference is None:
        print("Конференция не найдена, секция не добавлена.")
        return

    capacity = input_int("Вместимость (макс. докладов): ")
    try:
        section = add_section(sections, name, conference, capacity)
    except ValueError as error:
        print(f"Ошибка: {error}.")
        return
    print(f"Секция добавлена, id={section.id}")
    save_sections(SECTIONS_FILE, sections)


def show_filtered_sections(sections: list[Section], talks: list[Talk]) -> None:
    """Сценарий: отобрать секции по числу свободных мест."""
    min_free = input_int("Минимум свободных мест: ")
    found = False
    for section in filter_sections_by_capacity(sections, talks, min_free):
        print(section)
        found = True
    if not found:
        print("Подходящих секций не найдено.")


def main() -> None:
    """Точка запуска приложения: меню и вызов функций проекта."""
    conferences = load_conferences(CONFERENCES_FILE)
    sections = load_sections(SECTIONS_FILE, conferences)
    talks = load_talks(TALKS_FILE, sections)

    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_sections(sections)
        elif choice == "2":
            show_sections(find_section(sections, input("Название секции: ")))
        elif choice == "3":
            show_free_slots(sections, talks)
        elif choice == "4":
            check_slot(sections, talks)
        elif choice == "5":
            create_new_talk(talks, sections)
        elif choice == "6":
            cancel_talk(talks)
        elif choice == "7":
            show_talks(talks)
        elif choice == "8":
            create_new_conference(conferences)
        elif choice == "9":
            create_new_section(conferences, sections)
        elif choice == "10":
            show_filtered_sections(sections, talks)
        elif choice == "11":
            show_conferences(conferences)
        elif choice == "12":
            show_sections(sort_sections(sections))
        elif choice == "0":
            save_all(conferences, sections, talks)
            print("Данные сохранены. Выход из программы.")
            break
        else:
            print("Неверный пункт меню, попробуйте снова.")


if __name__ == "__main__":
    main()
