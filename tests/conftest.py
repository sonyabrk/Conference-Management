"""Общие фикстуры для тестов."""

import pytest

from models import Conference, Section


@pytest.fixture
def conference() -> Conference:
    return Conference(1, "PyCon 2026")


@pytest.fixture
def section(conference: Conference) -> Section:
    return Section(1, "Backend-разработка", conference, 5)
