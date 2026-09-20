"""Тесты класса Conference и функций работы с конференциями."""

from models import Conference
from models.conferences import add_conference, find_conference, find_conference_by_id


def test_conference_creation():
    conference = Conference(1, "PyCon 2026")
    assert conference.id == 1
    assert conference.name == "PyCon 2026"


def test_conference_str():
    assert "PyCon 2026" in str(Conference(1, "PyCon 2026"))


def test_conference_from_data():
    conference = Conference.from_data({"id": 2, "name": "DevConf"})
    assert conference.id == 2
    assert conference.name == "DevConf"


def test_conference_to_dict():
    assert Conference(1, "PyCon").to_dict() == {"id": 1, "name": "PyCon"}


def test_add_conference():
    conferences = []
    first = add_conference(conferences, "PyCon 2026")
    second = add_conference(conferences, "DevConf")
    assert conferences == [first, second]
    assert (first.id, second.id) == (1, 2)


def test_find_conference_ignores_case():
    conferences = []
    add_conference(conferences, "PyCon 2026")
    add_conference(conferences, "DevConf")
    found = find_conference(conferences, "pycon")
    assert len(found) == 1
    assert found[0].name == "PyCon 2026"


def test_find_conference_by_id():
    conferences = []
    conference = add_conference(conferences, "PyCon 2026")
    assert find_conference_by_id(conferences, conference.id) is conference
    assert find_conference_by_id(conferences, 99) is None
