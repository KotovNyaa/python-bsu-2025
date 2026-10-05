"""Модель данных студента."""

from lab.errors import ValidationError


class Student:
    """Представление студента с его идентификатором, ФИО и оценками."""

    def __init__(
        self,
        student_id: int,
        name: str,
        grades: list[int | None] | None = None,
    ) -> None:
        self.id = self._validate_id(student_id)
        self.name = self._validate_name(name)
        self.grades: list[int | None] = []
        self.set_grades(grades or [])

    @staticmethod
    def _validate_id(student_id: int) -> int:
        """Проверяет корректность идентификатора."""
        if not isinstance(student_id, int) or student_id <= 0:
            raise ValidationError(
                f"ID студента должен быть положительным целым числом, получено: {student_id}"
            )
        return student_id

    @staticmethod
    def _validate_name(name: str) -> str:
        """Проверяет корректность ФИО."""
        if not isinstance(name, str) or not name.strip():
            raise ValidationError("ФИО студента не может быть пустой строкой.")
        return name.strip()

    def set_grades(self, grades: list[int | None]) -> None:
        """Валидирует и устанавливает список оценок."""
        validated: list[int | None] = []
        for g in grades:
            if g is None:
                validated.append(None)
            elif isinstance(g, int) and 0 <= g <= 100:
                validated.append(g)
            else:
                raise ValidationError(
                    f"Оценка должна быть числом от 0 до 100 или None, получено: {g}"
                )
        self.grades = validated

    @property
    def average(self) -> float:
        """Рассчитывает средний балл только по имеющимся отметкам."""
        valid_grades = [g for g in self.grades if g is not None]
        if not valid_grades:
            return 0.0
        return sum(valid_grades) / len(valid_grades)

    def __repr__(self) -> str:
        return f"Student(id={self.id}, name='{self.name}', grades={self.grades}, avg={self.average:.2f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return (
            self.id == other.id
            and self.name == other.name
            and self.grades == other.grades
        )
