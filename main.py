from __future__ import annotations

from conferences import (
    add_conference,
    add_section,
    filter_sections_by_capacity,
    find_section,
)
from storage import (
    load_conferences,
    load_sections,
    load_talks,
    save_conferences,
    save_sections,
    save_talks,
)
from talks import (
    cancel_talk_submission,
    create_talk_submission,
    get_submission_status,
    is_slot_available,
)
from utils import input_int
from conferences import check_section_capacity

CONFERENCES_FILE = "data/conferences.json"
SECTIONS_FILE = "data/sections.json"
TALKS_FILE = "data/talks.json"


def show_sections(sections: dict[int, dict]) -> None:
    """Вывести список секций."""
    if not sections:
        print("Секции пока не добавлены.")
        return
    for section_id, data in sections.items():
        print(
            f"{section_id}. {data['name']} "
            f"(конференция {data['conference_id']}, "
            f"вместимость {data['capacity']})"
        )


def show_talks(talks: list[dict]) -> None:
    """Вывести список заявок на доклады."""
    if not talks:
        print("Доклады пока не добавлены.")
        return
    for talk in talks:
        print(
            f"{talk['id']}. {talk['title']} — {talk['author']} "
            f"(секция {talk['section_id']}, слот {talk['time_slot']})"
        )


def main() -> None:
    """Точка запуска приложения: меню и вызов функций проекта."""
    conferences = load_conferences(CONFERENCES_FILE)
    sections = load_sections(SECTIONS_FILE)
    talks = load_talks(TALKS_FILE)

    menu = """
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
0. Выход
"""

    while True:
        print(menu)
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_sections(sections)

        elif choice == "2":
            query = input("Название секции: ")
            found = find_section(sections, query)
            show_sections(found)

        elif choice == "3":
            section_id = input_int("ID секции: ")
            if section_id in sections:
                free = check_section_capacity(sections, talks, section_id)
                print(f"Свободно мест: {free}")
            else:
                print("Секция не найдена.")

        elif choice == "4":
            section_id = input_int("ID секции: ")
            time_slot = input("Тайм-слот (например, 10:00): ")
            available = is_slot_available(talks, section_id, time_slot)
            print(get_submission_status(available))

        elif choice == "5":
            section_id = input_int("ID секции: ")
            author = input("Автор доклада: ")
            title = input("Название доклада: ")
            time_slot = input("Тайм-слот: ")
            submission = create_talk_submission(
                talks, section_id, author, title, time_slot
            )
            if submission:
                print("Заявка создана.")
                save_talks(TALKS_FILE, talks)
            else:
                print("Слот занят, заявка не создана.")

        elif choice == "6":
            talk_id = input_int("ID заявки для отмены: ")
            if cancel_talk_submission(talks, talk_id):
                print("Заявка отменена.")
                save_talks(TALKS_FILE, talks)
            else:
                print("Заявка не найдена.")

        elif choice == "7":
            show_talks(talks)

        elif choice == "8":
            name = input("Название конференции: ")
            new_id = add_conference(conferences, name)
            print(f"Конференция добавлена, id={new_id}")
            save_conferences(CONFERENCES_FILE, conferences)

        elif choice == "9":
            name = input("Название секции: ")
            conference_id = input_int("ID конференции: ")
            capacity = input_int("Вместимость (макс. докладов): ")
            new_id = add_section(sections, name, conference_id, capacity)
            print(f"Секция добавлена, id={new_id}")
            save_sections(SECTIONS_FILE, sections)

        elif choice == "10":
            min_free = input_int("Минимум свободных мест: ")
            found = False
            for section_id, data in filter_sections_by_capacity(
                sections, talks, min_free
            ):
                print(
                    f"{section_id}. {data['name']} "
                    f"(вместимость {data['capacity']})"
                )
                found = True
            if not found:
                print("Подходящих секций не найдено.")

        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Неверный пункт меню, попробуйте снова.")


if __name__ == "__main__":
    main()
