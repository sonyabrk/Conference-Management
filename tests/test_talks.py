"""Тесты функций работы с заявками на доклады."""

from talks import (
    cancel_talk_submission,
    create_talk_submission,
    is_slot_available,
)


def test_is_slot_available():
    talks = []
    assert is_slot_available(talks, 1, "10:00")


def test_duplicate_slot_forbidden():
    talks = []
    create_talk_submission(talks, 1, "Иванов И.И.", "Доклад про Python", "10:00")
    assert not is_slot_available(talks, 1, "10:00")


def test_create_talk_submission():
    talks = []
    submission = create_talk_submission(
        talks, 1, "Иванов И.И.", "Доклад про Python", "10:00"
    )
    assert submission is not None
    assert len(talks) == 1


def test_cancel_talk_submission():
    talks = []
    submission = create_talk_submission(
        talks, 1, "Иванов И.И.", "Доклад про Python", "10:00"
    )
    assert cancel_talk_submission(talks, submission["id"])
    assert len(talks) == 0
