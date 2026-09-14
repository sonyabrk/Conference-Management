"""Тесты функций работы с конференциями и секциями."""

from conferences import (
    add_conference,
    add_section,
    check_section_capacity,
    filter_sections_by_capacity,
    find_section,
    sort_sections,
)


def test_add_conference():
    conferences = {}
    conf_id = add_conference(conferences, "PyCon 2026")
    assert len(conferences) == 1
    assert conferences[conf_id]["name"] == "PyCon 2026"


def test_add_section():
    sections = {}
    section_id = add_section(sections, "Backend-разработка", 1, 5)
    assert len(sections) == 1
    assert sections[section_id]["capacity"] == 5


def test_find_section():
    sections = {}
    add_section(sections, "Backend-разработка", 1, 5)
    found = find_section(sections, "backend")
    assert len(found) == 1


def test_check_section_capacity():
    sections = {}
    talks = []
    section_id = add_section(sections, "Frontend", 1, 3)
    free = check_section_capacity(sections, talks, section_id)
    assert free == 3


def test_sort_sections():
    sections = {}
    add_section(sections, "Small Room", 1, 3)
    add_section(sections, "Big Hall", 1, 10)
    sorted_list = sort_sections(sections)
    assert sorted_list[0][1]["capacity"] == 10
    assert sorted_list[1][1]["capacity"] == 3


def test_filter_sections_by_capacity():
    sections = {}
    talks = []
    add_section(sections, "Small Room", 1, 2)
    add_section(sections, "Big Hall", 1, 10)
    result = dict(filter_sections_by_capacity(sections, talks, 5))
    assert len(result) == 1
    assert "Big Hall" in [data["name"] for data in result.values()]
