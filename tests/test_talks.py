"""Тесты класса Talk и функций работы с заявками."""

from models import Section, Talk
from models.talks import (
    cancel_talk_submission,
    create_talk_submission,
    get_submission_status,
    is_slot_available,
)


def test_talk_creation(section):
    talk = Talk(1, section, "Иванов И.И.", "Доклад", "10:00")
    assert talk.section is section
    assert talk.author == "Иванов И.И."
    assert talk.time_slot == "10:00"
    assert not talk.is_cancelled


def test_talk_cancel_and_str(section):
    talk = Talk(1, section, "Иванов И.И.", "Доклад", "10:00")
    talk.cancel()
    assert talk.is_cancelled
    assert "отменена" in str(talk)


def test_talk_from_data_and_to_dict(section):
    data = {
        "id": 1,
        "section_id": 1,
        "author": "Иванов",
        "title": "Доклад",
        "time_slot": "10:00",
        "is_cancelled": True,
    }
    talk = Talk.from_data(data, section)
    assert talk.section is section
    assert talk.is_cancelled
    assert talk.to_dict() == data


def test_talk_from_data_without_is_cancelled(section):
    data = {"id": 1, "author": "A", "title": "T", "time_slot": "10:00"}
    assert not Talk.from_data(data, section).is_cancelled


def test_is_slot_available_empty(section):
    assert is_slot_available([], section, "10:00")


def test_create_talk_submission(section):
    talks = []
    talk = create_talk_submission(talks, section, "Иванов", "Доклад", "10:00")
    assert talk is not None
    assert talk.section is section
    assert talks == [talk]


def test_duplicate_slot_forbidden(section):
    talks = []
    create_talk_submission(talks, section, "Иванов", "Доклад", "10:00")
    assert not is_slot_available(talks, section, "10:00")
    assert create_talk_submission(talks, section, "Петров", "Другой", "10:00") is None
    assert len(talks) == 1


def test_same_slot_in_other_section_allowed(conference, section):
    other = Section(2, "Frontend", conference, 3)
    talks = []
    create_talk_submission(talks, section, "Иванов", "Доклад", "10:00")
    assert is_slot_available(talks, other, "10:00")


def test_cancel_keeps_talk_in_collection(section):
    talks = []
    talk = create_talk_submission(talks, section, "Иванов", "Доклад", "10:00")
    assert cancel_talk_submission(talks, talk.id)
    assert len(talks) == 1
    assert talk.is_cancelled


def test_cancel_unknown_or_repeated(section):
    talks = []
    talk = create_talk_submission(talks, section, "Иванов", "Доклад", "10:00")
    assert not cancel_talk_submission(talks, 99)
    assert cancel_talk_submission(talks, talk.id)
    assert not cancel_talk_submission(talks, talk.id)


def test_cancelled_talk_does_not_block_slot(section):
    talks = []
    first = create_talk_submission(talks, section, "Иванов", "Доклад", "10:00")
    assert create_talk_submission(talks, section, "Петров", "Другой", "10:00") is None

    first.cancel()
    second = create_talk_submission(talks, section, "Петров", "Другой", "10:00")
    assert second is not None
    assert len(talks) == 2


def test_section_capacity_is_enforced(conference):
    small = Section(1, "Small", conference, 1)
    talks = []
    assert create_talk_submission(talks, small, "A", "T1", "10:00") is not None
    assert create_talk_submission(talks, small, "B", "T2", "11:00") is None


def test_get_submission_status():
    assert get_submission_status(True) == "Слот доступен для доклада"
    assert get_submission_status(False) == "Слот уже занят"
