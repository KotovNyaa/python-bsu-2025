"""Общие фикстуры для тестирования лабораторной работы."""

from pathlib import Path
import pytest

from lab.models import Student


@pytest.fixture
def sample_students() -> list[Student]:
    """Возвращает тестовый набор студентов с различными сценариями оценок."""
    return [
        Student(student_id=1, name="Иванов Иван", grades=[80, 90, 100]),
        Student(student_id=2, name="Петров Петр", grades=[60, None, 70]),
        Student(student_id=3, name="Сидоров Сидор", grades=[0, 40]),
        Student(student_id=4, name="Алексеев Алексей", grades=[]),
    ]


@pytest.fixture
def sample_csv_with_header(tmp_path: Path) -> Path:
    """Создает временный CSV-файл с заголовком."""
    content = (
        "id,name,grade1,grade2,grade3\n"
        "1,Иванов Иван,80,90,100\n"
        "2,Петров Петр,60,,70\n"
        "3,Сидоров Сидор,0,40,\n"
    )
    file_path = tmp_path / "with_header.csv"
    file_path.write_text(content, encoding="utf-8")
    return file_path


@pytest.fixture
def sample_csv_without_header(tmp_path: Path) -> Path:
    """Создает временный CSV-файл без заголовка."""
    content = "1,Иванов Иван,80,90,100\n2,Петров Петр,60,,70\n3,Сидоров Сидор,0,40,\n"
    file_path = tmp_path / "without_header.csv"
    file_path.write_text(content, encoding="utf-8")
    return file_path
