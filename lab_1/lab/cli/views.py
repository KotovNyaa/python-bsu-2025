"""Функции форматирования и отрисовки данных в консоли."""

from typing import Any

from lab.models import Student


def print_header(title: str) -> None:
    """Выводит заголовок секции."""
    print(f"\n--- {title} ---")


def print_menu(current_file: str | None, total_students: int) -> None:
    """Отрисовывает меню и статус открытого файла."""
    file_status = current_file if current_file else "не выбран"
    print("\n" + "=" * 52)
    print(" УПРАВЛЕНИЕ СПИСКОМ СТУДЕНТОВ")
    print(f" Файл: {file_status} | В памяти: {total_students}")
    print("=" * 52)
    print(" 1. Загрузить из CSV")
    print(" 2. Сохранить в CSV")
    print(" 3. Показать всех студентов")
    print(" 4. Добавить студента")
    print(" 5. Удалить по ID")
    print(" 6. Обновить оценки по ID")
    print(" 7. Статистика по группе")
    print(" 8. Экспорт ТОП-N студентов в CSV")
    print(" 9. Сортировка (avg / name / id) и показ")
    print(" 0. Выход")
    print("-" * 52)


def format_grade(grade: int | None) -> str:
    """Форматирует оценку в 3 символа или прочерк."""
    return f"{grade:>3}" if grade is not None else "  -"


def print_table(students: list[Student]) -> None:
    """Выводит список студентов в виде ровной ASCII-таблицы."""
    if not students:
        print("Список студентов пуст.")
        return

    max_grades_count = max(len(s.grades) for s in students)
    max_grades_count = max(max_grades_count, 1)

    grades_header_title = "Оценки"
    min_grades_width = max_grades_count * 4 - 1
    grades_col_width = max(len(grades_header_title), min_grades_width)

    id_w, name_w, avg_w = 5, 24, 8

    print(
        f"{'ID':<{id_w}} | {'ФИО':<{name_w}} | "
        f"{grades_header_title:<{grades_col_width}} | {'Ср. балл':>{avg_w}}"
    )
    divider_len = id_w + name_w + grades_col_width + avg_w + 9
    print("-" * divider_len)

    for s in students:
        rendered_grades = []
        for i in range(max_grades_count):
            if i < len(s.grades):
                rendered_grades.append(format_grade(s.grades[i]))
            else:
                rendered_grades.append("  -")
        grades_str = " ".join(rendered_grades)

        print(
            f"{s.id:<{id_w}} | {s.name:<{name_w}} | "
            f"{grades_str:<{grades_col_width}} | {s.average:>{avg_w}.2f}"
        )


def print_stats(stats: dict[str, Any]) -> None:
    """Выводит сводную статистику группы."""
    print_header("Статистика по группе")
    print(f"Всего студентов      : {stats['count']}")
    print(f"Общий средний балл   : {stats['overall_avg']:.2f}")

    best = stats.get("best")
    worst = stats.get("worst")

    best_str = (
        f"{best.name} (ID: {best.id}, ср.: {best.average:.2f})"
        if best
        else "нет данных"
    )
    worst_str = (
        f"{worst.name} (ID: {worst.id}, ср.: {worst.average:.2f})"
        if worst
        else "нет данных"
    )

    print(f"Лучший студент       : {best_str}")
    print(f"Худший студент       : {worst_str}")
