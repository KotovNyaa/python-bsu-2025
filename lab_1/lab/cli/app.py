"""Главный контроллер консольного приложения."""

from pathlib import Path

from lab.cli.inputs import ask_grades, ask_int, ask_menu_choice, ask_string
from lab.cli.views import (
    print_header,
    print_menu,
    print_stats,
    print_table,
)
from lab.errors import StudentAppError
from lab.io_utils import (
    export_top_students_csv,
    read_students_from_csv,
    write_students_to_csv,
)
from lab.models import Student
from lab.processing import StudentGroup


class CLIApp:
    """Класс управления жизненным циклом программы и командами меню."""

    def __init__(self) -> None:
        self.current_file: str | None = None
        self.group = StudentGroup()

    @staticmethod
    def _resolve_read_path(raw_path: str) -> str:
        """Проверяет путь и автоматически ищет файл в папке data/."""
        path = Path(raw_path)
        if not path.is_file():
            fallback = Path("data") / raw_path
            if fallback.is_file():
                print(f"-> Файл найден в директории 'data/': {fallback}")
                return str(fallback)
        return raw_path

    def run(self) -> None:
        """Запускает основной цикл меню."""
        print_menu(self.current_file, len(self.group))

        while True:
            file_name = self.current_file if self.current_file else "файл не выбран"
            prompt = f"\n[{file_name} | студентов: {len(self.group)}] Команда (0-9, ? - меню) > "
            choice = ask_menu_choice(prompt)

            if choice in ("?", "h", "help"):
                print_menu(self.current_file, len(self.group))
                continue

            cmd_num = int(choice)
            if cmd_num == 0:
                print("\nРабота завершена. До свидания!")
                break

            try:
                self._dispatch(cmd_num)
            except StudentAppError as err:
                print(f"\n[Ошибка]: {err}")
            except Exception as err:  # noqa: BLE001
                print(f"\n[Непредвиденная ошибка]: {err}")

    def _dispatch(self, choice: int) -> None:
        handlers = {
            1: self._load_from_csv,
            2: self._save_to_csv,
            3: self._show_all,
            4: self._add_student,
            5: self._remove_student,
            6: self._update_grades,
            7: self._show_stats,
            8: self._export_top,
            9: self._sort_students,
        }
        handler = handlers.get(choice)
        if handler:
            handler()

    def _load_from_csv(self) -> None:
        print_header("Загрузка из CSV")
        raw_path = ask_string("Введите путь к CSV файлу: ")
        path = self._resolve_read_path(raw_path)

        loaded = read_students_from_csv(path)
        self.group.clear()
        for s in loaded:
            self.group.add(s)

        self.current_file = path
        print(f"Успешно загружено студентов: {len(self.group)} из '{path}'")

    def _save_to_csv(self) -> None:
        print_header("Сохранение в CSV")
        if len(self.group) == 0:
            print("Предупреждение: список студентов пуст.")

        default_prompt = f" [{self.current_file}]" if self.current_file else ""
        raw = input(f"Путь для сохранения{default_prompt}: ").strip()
        path = raw or self.current_file
        if not path:
            print("Ошибка: путь сохранения не указан.")
            return

        write_students_to_csv(path, self.group.get_all())
        self.current_file = path
        print(f"Данные ({len(self.group)} студентов) успешно сохранены в '{path}'")

    def _show_all(self) -> None:
        print_header("Список всех студентов")
        print_table(self.group.get_all())

    def _add_student(self) -> None:
        print_header("Добавление студента")
        s_id = ask_int("ID студента (> 0): ", min_val=1)
        name = ask_string("ФИО студента: ")
        grades = ask_grades("Оценки через пробел ('-' для пропуска, Enter если нет): ")

        student = Student(student_id=s_id, name=name, grades=grades)
        self.group.add(student)
        print(f"Студент '{name}' (ID: {s_id}) успешно добавлен.")

    def _remove_student(self) -> None:
        print_header("Удаление студента")
        if len(self.group) == 0:
            print("Список студентов пуст. Удалять некого.")
            return

        s_id = ask_int("Введите ID студента для удаления: ", min_val=1)
        removed = self.group.remove(s_id)
        print(f"Студент '{removed.name}' (ID: {removed.id}) успешно удален.")

    def _update_grades(self) -> None:
        print_header("Обновление оценок по ID")
        if len(self.group) == 0:
            print("Список студентов пуст.")
            return

        s_id = ask_int("Введите ID студента: ", min_val=1)
        student = self.group.get(s_id)
        print(f"Текущие оценки студента {student.name}: {student.grades}")

        new_grades = ask_grades("Новые оценки через пробел ('-' для пропуска): ")
        self.group.update_grades(s_id, new_grades)
        print(f"Оценки студента ID {s_id} успешно обновлены.")

    def _show_stats(self) -> None:
        if len(self.group) == 0:
            print("Список студентов пуст. Статистика недоступна.")
            return
        stats = self.group.get_stats()
        print_stats(stats)

    def _export_top(self) -> None:
        print_header("Экспорт ТОП-N студентов")
        if len(self.group) == 0:
            print("Список студентов пуст. Экспорт невозможен.")
            return

        n = ask_int(
            f"Количество студентов (1..{len(self.group)}): ",
            min_val=1,
            max_val=len(self.group),
        )
        path = ask_string("Путь к CSV для сохранения ТОП-N: ")
        top_list = self.group.get_top(n)
        export_top_students_csv(path, top_list)
        print(f"ТОП-{n} студентов успешно экспортирован в '{path}'")

    def _sort_students(self) -> None:
        print_header("Сортировка списка")
        if len(self.group) == 0:
            print("Список студентов пуст. Сортировать нечего.")
            return

        print(
            "Доступные критерии: avg (по среднему баллу), name (по ФИО), id (по номеру)"
        )
        while True:
            by = ask_string("Критерий: ").lower()
            if by in ("avg", "name", "id"):
                break
            print("Ошибка: введите avg, name или id.")

        sorted_students = self.group.sort(by=by)
        print(f"\nРезультат сортировки по '{by}':")
        print_table(sorted_students)
