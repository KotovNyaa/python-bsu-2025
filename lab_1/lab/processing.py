"""Бизнес-логика обработки списка студентов, фильтрации и статистики."""

from typing import Any

from lab.errors import (
    DuplicateStudentError,
    EmptyGroupError,
    StudentNotFoundError,
    ValidationError,
)
from lab.models import Student


def calculate_group_stats(students: list[Student]) -> dict[str, Any]:
    """Вычисляет общую статистику по коллекции студентов."""
    if not students:
        return {"count": 0, "overall_avg": 0.0, "best": None, "worst": None}

    all_grades = [g for s in students for g in s.grades if g is not None]
    overall_avg = sum(all_grades) / len(all_grades) if all_grades else 0.0

    best_student = max(students, key=lambda s: (s.average, s.name))
    worst_student = min(students, key=lambda s: (s.average, s.name))

    return {
        "count": len(students),
        "overall_avg": overall_avg,
        "best": best_student,
        "worst": worst_student,
    }


def sort_students(students: list[Student], by: str = "avg") -> list[Student]:
    """Сортирует список студентов по заданному критерию."""
    if by == "avg":
        return sorted(students, key=lambda s: (-s.average, s.name.lower()))
    if by == "name":
        return sorted(students, key=lambda s: s.name.lower())
    if by == "id":
        return sorted(students, key=lambda s: s.id)
    raise ValidationError(
        f"Неизвестный критерий сортировки: '{by}'. Допустимы: avg, name, id."
    )


def filter_by_min_average(students: list[Student], min_avg: float) -> list[Student]:
    """Фильтрует студентов со средним баллом не ниже заданного порога."""
    return [s for s in students if s.average >= min_avg]


def filter_with_debts(
    students: list[Student], passing_score: int = 40
) -> list[Student]:
    """Фильтрует студентов с пропусками или оценками ниже проходного балла."""
    return [
        s
        for s in students
        if not s.grades or any(g is None or g < passing_score for g in s.grades)
    ]


def filter_by_name(students: list[Student], query: str) -> list[Student]:
    """Фильтрует студентов по подстроке в ФИО без учета регистра."""
    clean_query = query.strip().lower()
    return [s for s in students if clean_query in s.name.lower()]


class StudentGroup:
    """Управление коллекцией студентов в оперативной памяти."""

    def __init__(self, initial_students: list[Student] | None = None) -> None:
        self._students: dict[int, Student] = {}
        if initial_students:
            for s in initial_students:
                self.add(s)

    def add(self, student: Student) -> None:
        """Добавляет студента в группу с проверкой уникальности ID."""
        if student.id in self._students:
            raise DuplicateStudentError(
                f"Студент с ID {student.id} уже существует в группе."
            )
        self._students[student.id] = student

    def remove(self, student_id: int) -> Student:
        """Удаляет студента по ID."""
        if student_id not in self._students:
            raise StudentNotFoundError(f"Студент с ID {student_id} не найден.")
        return self._students.pop(student_id)

    def get(self, student_id: int) -> Student:
        """Возвращает студента по ID."""
        if student_id not in self._students:
            raise StudentNotFoundError(f"Студент с ID {student_id} не найден.")
        return self._students[student_id]

    def update_grades(self, student_id: int, new_grades: list[int | None]) -> None:
        """Обновляет оценки студента по ID."""
        student = self.get(student_id)
        student.set_grades(new_grades)

    def get_all(self) -> list[Student]:
        """Возвращает текущий список всех студентов."""
        return list(self._students.values())

    def sort(self, by: str = "avg") -> list[Student]:
        """Сортирует текущих студентов и возвращает новый список."""
        return sort_students(self.get_all(), by=by)

    def filter_by_min_avg(self, min_avg: float) -> list[Student]:
        """Возвращает студентов со средним баллом не ниже min_avg."""
        return filter_by_min_average(self.get_all(), min_avg=min_avg)

    def filter_debts(self, passing_score: int = 40) -> list[Student]:
        """Возвращает студентов с задолженностями."""
        return filter_with_debts(self.get_all(), passing_score=passing_score)

    def filter_by_name(self, query: str) -> list[Student]:
        """Ищет студентов по подстроке в ФИО."""
        return filter_by_name(self.get_all(), query=query)

    def get_stats(self) -> dict[str, Any]:
        """Возвращает статистику по группе."""
        return calculate_group_stats(self.get_all())

    def get_top(self, n: int) -> list[Student]:
        """Возвращает ТОП-N студентов по среднему баллу."""
        if n <= 0:
            raise ValidationError("Число N должно быть больше 0.")
        if not self._students:
            raise EmptyGroupError("Группа пуста, невозможно сформировать ТОП.")
        sorted_list = self.sort(by="avg")
        return sorted_list[:n]

    def clear(self) -> None:
        """Очищает коллекцию студентов."""
        self._students.clear()

    def __len__(self) -> int:
        return len(self._students)
