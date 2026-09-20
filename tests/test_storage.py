"""Тесты загрузки и сохранения объектов в JSON."""

import json

from models import Conference, Section, Talk
from storage import (
    load_conferences,
    load_sections,
    load_talks,
    save_conferences,
    save_sections,
    save_talks,
)


def test_roundtrip_restores_links(tmp_path):
    conference = Conference(1, "PyCon 2026")
    section = Section(1, "Backend", conference, 5)
    talk = Talk(1, section, "Иванов", "Async", "10:00")
    talk.cancel()

    conf_file = str(tmp_path / "conferences.json")
    sec_file = str(tmp_path / "sections.json")
    talk_file = str(tmp_path / "talks.json")
    save_conferences(conf_file, [conference])
    save_sections(sec_file, [section])
    save_talks(talk_file, [talk])

    conferences = load_conferences(conf_file)
    sections = load_sections(sec_file, conferences)
    talks = load_talks(talk_file, sections)

    assert sections[0].conference is conferences[0]
    assert talks[0].section is sections[0]
    assert talks[0].is_cancelled


def test_saved_json_contains_ids_not_objects(tmp_path):
    section = Section(1, "Backend", Conference(1, "PyCon"), 5)
    talk = Talk(1, section, "Иванов", "Async", "10:00")
    talk_file = tmp_path / "talks.json"
    save_talks(str(talk_file), [talk])

    data = json.loads(talk_file.read_text(encoding="utf-8"))
    assert data[0]["section_id"] == 1
    assert "section" not in data[0]


def test_missing_file_gives_empty_list(tmp_path):
    assert load_conferences(str(tmp_path / "missing.json")) == []


def test_corrupted_file_gives_empty_list(tmp_path):
    broken = tmp_path / "broken.json"
    broken.write_text("{broken", encoding="utf-8")
    assert load_conferences(str(broken)) == []


def test_talk_with_unknown_section_is_skipped(tmp_path):
    talk_file = tmp_path / "talks.json"
    talk_file.write_text(
        json.dumps(
            [{"id": 1, "section_id": 99, "author": "A", "title": "T", "time_slot": "10:00"}]
        ),
        encoding="utf-8",
    )
    assert load_talks(str(talk_file), []) == []
