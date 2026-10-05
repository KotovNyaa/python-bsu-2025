"""Функции для работы с файлами CSV."""

import csv
from pathlib import Path

from lab.errors import (
    CSVFormatError,
    FileAccessError,
    FileNotFoundAppError,
    FileStorageError,
)
from lab.models import Student


def _is_header_row(row: list[str]) -> bool:
    """Определяет, является ли первая строка файла заголовком."""
    if not row:
        return False

    first_cell = row[0].strip().lower()
    header_id_tokens = {"id", "ид", "student_id", "identifier", "#id"}
    header_name_tokens = {"name", "фио", "имя", "student_name", "студент"}

    if first_cell in header_id_tokens:
        return True

    if len(row) > 1 and row[1].strip().lower() in header_name_tokens:
        return True

    return False


def read_students_from_csv(file_path: str | Path) -> list[Student]:
    """Считывает студентов из CSV-файла с поддержкой хедеров и без."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundAppError(f"Файл не найден: {path}")

    try:
        with open(path, mode="r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            rows = [row for row in reader if row and any(c.strip() for c in row)]
    except PermissionError as err:
        raise FileAccessError(f"Нет прав на чтение файла: {path}") from err
    except OSError as err:
        raise FileStorageError(f"Ошибка при чтении файла {path}: {err}") from err

    if not rows:
        return []

    if _is_header_row(rows[0]):
        rows = rows[1:]

    students: list[Student] = []
    seen_ids: set[int] = set()

    for line_idx, row in enumerate(rows, start=1):
        if len(row) < 2:
            raise CSVFormatError(
                f"Строка {line_idx}: ожидается минимум 2 колонки (id, name), получено: {len(row)}"
            )

        try:
            student_id = int(row[0].strip())
        except ValueError as err:
            raise CSVFormatError(
                f"Строка {line_idx}: ID должен быть целым числом, получено '{row[0]}'"
            ) from err

        if student_id in seen_ids:
            raise CSVFormatError(
                f"Строка {line_idx}: обнаружен дубликат ID {student_id}"
            )
        seen_ids.add(student_id)

        name = row[1].strip()
        if not name:
            raise CSVFormatError(f"Строка {line_idx}: ФИО не может быть пустым.")

        grades = []
        for col_idx, cell in enumerate(row[2:], start=3):
            val = cell.strip()
            if not val or val in ("-", "_"):
                grades.append(None)
            else:
                try:
                    grade = int(val)
                    if not (0 <= grade <= 100):
                        raise CSVFormatError(
                            f"Строка {line_idx}, колонка {col_idx}: оценка {grade} вне диапазона 0..100"
                        )
                    grades.append(grade)
                except ValueError as err:
                    raise CSVFormatError(
                        f"Строка {line_idx}, колонка {col_idx}: некорректная отметка '{val}'"
                    ) from err

        students.append(Student(student_id=student_id, name=name, grades=grades))

    return students


def write_students_to_csv(file_path: str | Path, students: list[Student]) -> None:
    """Сохраняет студентов в CSV с выравниванием колонок оценок."""
    path = Path(file_path)
    try:
        max_grades = max((len(s.grades) for s in students), default=0)
        header = ["id", "name"] + [f"grade{i + 1}" for i in range(max_grades)]

        with open(path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)

            for s in students:
                row: list[int | str] = [s.id, s.name]
                for i in range(max_grades):
                    if i < len(s.grades) and s.grades[i] is not None:
                        row.append(s.grades[i])
                    else:
                        row.append("")
                writer.writerow(row)
    except PermissionError as err:
        raise FileAccessError(f"Нет прав на запись в файл: {path}") from err
    except OSError as err:
        raise FileStorageError(f"Ошибка при записи файла {path}: {err}") from err


def export_top_students_csv(file_path: str | Path, top_students: list[Student]) -> None:
    """Экспортирует ТОП студентов в формате: id, name, average, grades."""
    path = Path(file_path)
    try:
        with open(path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "average", "grades"])

            for s in top_students:
                grades_str = " ".join(
                    str(g) if g is not None else "-" for g in s.grades
                )
                writer.writerow([s.id, s.name, f"{s.average:.2f}", grades_str])
    except PermissionError as err:
        raise FileAccessError(f"Нет прав на запись файла: {path}") from err
    except OSError as err:
        raise FileStorageError(f"Ошибка при экспорте в {path}: {err}") from err
