"""Тесты для файлового ввода-вывода CSV."""

from pathlib import Path
import pytest

from lab.errors import CSVFormatError, FileNotFoundAppError
from lab.io_utils import (
    export_top_students_csv,
    read_students_from_csv,
    write_students_to_csv,
)
from lab.models import Student


def test_read_csv_with_header(sample_csv_with_header: Path) -> None:
    """Проверяет чтение CSV-файла с заголовком."""
    students = read_students_from_csv(sample_csv_with_header)
    assert len(students) == 3
    assert students[0].name == "Иванов Иван"
    assert students[0].grades == [80, 90, 100]
    assert students[1].grades == [60, None, 70]
    assert students[2].grades == [0, 40, None]


def test_read_csv_without_header(sample_csv_without_header: Path) -> None:
    """Проверяет чтение CSV-файла без заголовка."""
    students = read_students_from_csv(sample_csv_without_header)
    assert len(students) == 3
    assert students[0].id == 1
    assert students[0].grades == [80, 90, 100]


def test_read_csv_nonexistent_file(tmp_path: Path) -> None:
    """Проверяет ошибку при чтении несуществующего файла."""
    with pytest.raises(FileNotFoundAppError):
        read_students_from_csv(tmp_path / "missing.csv")


@pytest.mark.parametrize(
    "corrupted_content",
    [
        "1\n",
        "abc,Иван,90\n",
        "1,Иван,not_a_grade\n",
        "1,Иван,150\n",
        "1,Иван,90\n1,Петр,80\n",
    ],
)
def test_read_csv_corrupted_formats_raise(
    tmp_path: Path, corrupted_content: str
) -> None:
    """Проверяет реакцию парсера на битые файлы CSV."""
    bad_file = tmp_path / "bad.csv"
    bad_file.write_text(corrupted_content, encoding="utf-8")
    with pytest.raises(CSVFormatError):
        read_students_from_csv(bad_file)


def test_csv_roundtrip_and_alignment(tmp_path: Path) -> None:
    """Проверяет сохранение, выравнивание колонок и обратное чтение."""
    s1 = Student(1, "Студент 1", [90, 95, 100])
    s2 = Student(2, "Студент 2", [80])
    original_students = [s1, s2]

    out_file = tmp_path / "output.csv"
    write_students_to_csv(out_file, original_students)

    raw_lines = out_file.read_text(encoding="utf-8").splitlines()
    assert raw_lines[0] == "id,name,grade1,grade2,grade3"
    assert raw_lines[2] == "2,Студент 2,80,,"

    loaded = read_students_from_csv(out_file)
    assert len(loaded) == 2
    assert loaded[0] == s1
    assert loaded[1].grades == [80, None, None]


def test_export_top_students_csv(
    tmp_path: Path, sample_students: list[Student]
) -> None:
    """Проверяет формат экспорта ТОП-N студентов."""
    top_file = tmp_path / "top.csv"
    export_top_students_csv(top_file, sample_students[:2])

    lines = top_file.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "id,name,average,grades"
    assert lines[1] == "1,Иванов Иван,90.00,80 90 100"
    assert lines[2] == "2,Петров Петр,65.00,60 - 70"
