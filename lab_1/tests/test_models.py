"""Тесты для модели данных Student."""

import pytest

from lab.errors import ValidationError
from lab.models import Student


def test_student_creation_valid() -> None:
    """Проверяет создание студента с валидными данными."""
    student = Student(student_id=1, name="Иван Иванов", grades=[80, None, 95])
    assert student.id == 1
    assert student.name == "Иван Иванов"
    assert student.grades == [80, None, 95]


@pytest.mark.parametrize("invalid_id", [0, -5, "1", 2.5, None])
def test_student_invalid_id_raises(invalid_id: object) -> None:
    """Проверяет ошибку при некорректном идентификаторе."""
    with pytest.raises(ValidationError):
        Student(student_id=invalid_id, name="Тест")  # type: ignore[arg-type]


@pytest.mark.parametrize("invalid_name", ["", "   ", None, 123])
def test_student_invalid_name_raises(invalid_name: object) -> None:
    """Проверяет ошибку при некорректном имени студента."""
    with pytest.raises(ValidationError):
        Student(student_id=1, name=invalid_name)  # type: ignore[arg-type]


@pytest.mark.parametrize("invalid_grades", [[-1], [101], ["отлично"], [50, 200]])
def test_student_invalid_grades_raises(invalid_grades: list[object]) -> None:
    """Проверяет ошибку при некорректных оценках."""
    with pytest.raises(ValidationError):
        Student(student_id=1, name="Тест", grades=invalid_grades)  # type: ignore[arg-type]


def test_student_average_calculation() -> None:
    """Проверяет расчет среднего балла только по имеющимся отметкам."""
    s1 = Student(1, "Студент 1", [80, 90])
    assert s1.average == 85.0

    s2 = Student(2, "Студент 2", [80, None, 100])
    assert s2.average == 90.0

    s3 = Student(3, "Студент 3", [0, 100])
    assert s3.average == 50.0

    s4 = Student(4, "Студент 4", [])
    assert s4.average == 0.0

    s5 = Student(5, "Студент 5", [None, None])
    assert s5.average == 0.0


def test_student_set_grades_and_equality() -> None:
    """Проверяет обновление оценок и равенство студентов."""
    s1 = Student(1, "Иван", [50])
    s2 = Student(1, "Иван", [50])
    assert s1 == s2

    s1.set_grades([100, 90])
    assert s1.average == 95.0
    assert s1 != s2
