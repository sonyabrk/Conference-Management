"""Тесты класса Section и функций работы с секциями."""

import inspect

import pytest

from models import Section, Talk
from models.sections import (
    add_section,
    check_section_capacity,
    filter_sections_by_capacity,
    find_section,
    sort_sections,
)


def test_section_creation(conference, section):
    assert section.id == 1
    assert section.name == "Backend-разработка"
    assert section.capacity == 5
    assert section.conference is conference


def test_section_str(section):
    text = str(section)
    assert "Backend-разработка" in text
    assert "PyCon 2026" in text


def test_validate_capacity():
    assert Section.validate_capacity(5)
    assert not Section.validate_capacity(0)
    assert not Section.validate_capacity(-1)


def test_free_slots_without_talks(section):
    assert section.free_slots([]) == 5


def test_free_slots_ignores_cancelled_talks(section):
    active = Talk(1, section, "Иванов", "A", "10:00")
    cancelled = Talk(2, section, "Петров", "B", "11:00")
    cancelled.cancel()
    assert section.free_slots([active, cancelled]) == 4


def test_has_free_slots(section):
    assert section.has_free_slots([], 5)
    assert not section.has_free_slots([], 6)


def test_section_from_data_and_to_dict(conference):
    data = {"id": 3, "name": "Data", "conference_id": 1, "capacity": 4}
    section = Section.from_data(data, conference)
    assert section.conference is conference
    assert section.to_dict() == data


def test_add_section(conference):
    sections = []
    section = add_section(sections, "Backend", conference, 5)
    assert sections == [section]
    assert section.conference is conference


def test_add_section_invalid_capacity(conference):
    with pytest.raises(ValueError):
        add_section([], "Backend", conference, 0)


def test_find_section(conference):
    sections = []
    add_section(sections, "Backend-разработка", conference, 5)
    add_section(sections, "Frontend", conference, 3)
    found = find_section(sections, "backend")
    assert len(found) == 1


def test_check_section_capacity(conference):
    sections = []
    section = add_section(sections, "Frontend", conference, 3)
    assert check_section_capacity(sections, [], section.id) == 3


def test_check_section_capacity_unknown_section():
    with pytest.raises(ValueError):
        check_section_capacity([], [], 1)


def test_sort_sections(conference):
    sections = []
    add_section(sections, "Small Room", conference, 3)
    add_section(sections, "Big Hall", conference, 10)
    result = sort_sections(sections)
    assert [s.capacity for s in result] == [10, 3]


def test_filter_sections_by_capacity_is_generator(conference):
    sections = []
    add_section(sections, "Small Room", conference, 2)
    add_section(sections, "Big Hall", conference, 10)
    result = filter_sections_by_capacity(sections, [], 5)
    assert inspect.isgenerator(result)
    assert [s.name for s in result] == ["Big Hall"]
