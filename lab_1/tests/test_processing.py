"""Тесты для бизнес-логики обработки и группы студентов."""

import pytest

from lab.errors import (
    DuplicateStudentError,
    EmptyGroupError,
    StudentNotFoundError,
    ValidationError,
)
from lab.models import Student
from lab.processing import (
    StudentGroup,
    calculate_group_stats,
    filter_by_min_average,
    filter_by_name,
    filter_with_debts,
    sort_students,
)


def test_group_crud_operations() -> None:
    """Проверяет базовые CRUD-операции над группой."""
    group = StudentGroup()
    student = Student(1, "Анна", [90, 95])

    group.add(student)
    assert len(group) == 1
    assert group.get(1) == student

    with pytest.raises(DuplicateStudentError):
        group.add(Student(1, "Другая Анна", [50]))

    group.update_grades(1, [100, 100])
    assert group.get(1).average == 100.0

    removed = group.remove(1)
    assert removed == student
    assert len(group) == 0

    with pytest.raises(StudentNotFoundError):
        group.remove(1)


def test_sort_students() -> None:
    """Проверяет сортировку по разным критериям со стабильностью."""
    s1 = Student(1, "Борис", [80])
    s2 = Student(2, "Анна", [80])
    s3 = Student(3, "Владимир", [95])
    students = [s1, s2, s3]

    sorted_avg = sort_students(students, by="avg")
    assert [s.id for s in sorted_avg] == [3, 2, 1]

    sorted_name = sort_students(students, by="name")
    assert [s.id for s in sorted_name] == [2, 1, 3]

    sorted_id = sort_students(students, by="id")
    assert [s.id for s in sorted_id] == [1, 2, 3]

    with pytest.raises(ValidationError):
        sort_students(students, by="invalid")


def test_filter_operations(sample_students: list[Student]) -> None:
    """Проверяет фильтрацию студентов по оценкам, долгам и имени."""
    filtered_avg = filter_by_min_average(sample_students, min_avg=65.0)
    assert len(filtered_avg) == 2
    assert {s.id for s in filtered_avg} == {1, 2}

    filtered_debts = filter_with_debts(sample_students, passing_score=40)
    assert {s.id for s in filtered_debts} == {2, 3, 4}

    filtered_name = filter_by_name(sample_students, query="сидор")
    assert len(filtered_name) == 1
    assert filtered_name[0].id == 3


def test_group_statistics(sample_students: list[Student]) -> None:
    """Проверяет расчет общей групповой статистики."""
    stats_empty = calculate_group_stats([])
    assert stats_empty["count"] == 0
    assert stats_empty["overall_avg"] == 0.0
    assert stats_empty["best"] is None

    stats = calculate_group_stats(sample_students)
    assert stats["count"] == 4
    assert stats["overall_avg"] == (80 + 90 + 100 + 60 + 70 + 0 + 40) / 7
    assert stats["best"].id == 1
    assert stats["worst"].id == 4


def test_group_top_students(sample_students: list[Student]) -> None:
    """Проверяет получение ТОП-N студентов."""
    group = StudentGroup(sample_students)

    top2 = group.get_top(2)
    assert len(top2) == 2
    assert [s.id for s in top2] == [1, 2]

    with pytest.raises(ValidationError):
        group.get_top(0)

    empty_group = StudentGroup()
    with pytest.raises(EmptyGroupError):
        empty_group.get_top(1)
