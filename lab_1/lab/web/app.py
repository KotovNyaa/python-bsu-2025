"""Маршруты и логика Flask-приложения."""

import tempfile
from pathlib import Path
from typing import Any

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

from lab.errors import StudentAppError
from lab.io_utils import (
    export_top_students_csv,
    read_students_from_csv,
)
from lab.models import Student
from lab.processing import StudentGroup

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DEFAULT_CSV = DATA_DIR / "students.csv"


def create_app() -> Flask:
    """Создает и настраивает экземпляр приложения Flask."""
    app = Flask(__name__)
    app.secret_key = "lab-students-secret-key"

    group = StudentGroup()

    if DEFAULT_CSV.is_file():
        try:
            for s in read_students_from_csv(DEFAULT_CSV):
                group.add(s)
        except StudentAppError:
            pass

    @app.route("/", methods=["GET"])
    def index() -> str:
        """Отображает главную страницу с таблицей и статистикой."""
        sort_by = request.args.get("sort", "id")
        try:
            students = group.sort(by=sort_by)
        except StudentAppError:
            students = group.get_all()

        max_grades = max((len(s.grades) for s in students), default=0)
        stats: dict[str, Any] = group.get_stats()
        return render_template(
            "index.html",
            students=students,
            stats=stats,
            current_sort=sort_by,
            total_count=len(group),
            max_grades=max_grades,
        )

    @app.route("/upload", methods=["POST"])
    def upload_csv() -> Any:
        """Загружает CSV-файл и обновляет список студентов."""
        file = request.files.get("file")
        if not file or not file.filename:
            flash("Файл не выбран.", "danger")
            return redirect(url_for("index"))

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        save_path = DATA_DIR / Path(file.filename).name
        file.save(save_path)

        try:
            loaded = read_students_from_csv(save_path)
            group.clear()
            for s in loaded:
                group.add(s)
            flash(
                f"Успешно загружено {len(loaded)} записей из файла {file.filename}.",
                "success",
            )
        except StudentAppError as err:
            flash(f"Ошибка загрузки: {err}", "danger")

        return redirect(url_for("index"))

    @app.route("/reset-default", methods=["POST"])
    def reset_default() -> Any:
        """Сбрасывает данные к исходному файлу students.csv."""
        if not DEFAULT_CSV.is_file():
            flash("Базовый файл students.csv не найден.", "danger")
            return redirect(url_for("index"))

        try:
            loaded = read_students_from_csv(DEFAULT_CSV)
            group.clear()
            for s in loaded:
                group.add(s)
            flash("Список сброшен к базовому файлу students.csv.", "success")
        except StudentAppError as err:
            flash(f"Ошибка сброса: {err}", "danger")

        return redirect(url_for("index"))

    @app.route("/students/add", methods=["POST"])
    def add_student() -> Any:
        """Добавляет нового студента."""
        try:
            s_id = int(request.form.get("id", "").strip())
            name = request.form.get("name", "").strip()
            raw_grades = request.form.get("grades", "").strip()

            grades: list[int | None] = []
            if raw_grades:
                for token in raw_grades.split():
                    if token in ("-", "_", "none", "None"):
                        grades.append(None)
                    else:
                        grades.append(int(token))

            student = Student(student_id=s_id, name=name, grades=grades)
            group.add(student)
            flash(f"Студент {name} (ID: {s_id}) успешно добавлен.", "success")
        except ValueError:
            flash("Ошибка: ID и оценки должны быть корректными числами.", "danger")
        except StudentAppError as err:
            flash(f"Ошибка добавления: {err}", "danger")

        return redirect(url_for("index"))

    @app.route("/students/update-grades", methods=["POST"])
    def update_grades() -> Any:
        """Обновляет оценки студента по ID."""
        try:
            s_id = int(request.form.get("id", "").strip())
            raw_grades = request.form.get("grades", "").strip()

            grades: list[int | None] = []
            if raw_grades:
                for token in raw_grades.split():
                    if token in ("-", "_", "none", "None"):
                        grades.append(None)
                    else:
                        grades.append(int(token))

            group.update_grades(s_id, grades)
            flash(f"Оценки студента ID {s_id} обновлены.", "success")
        except ValueError:
            flash("Ошибка формата оценок или ID.", "danger")
        except StudentAppError as err:
            flash(f"Ошибка обновления: {err}", "danger")

        return redirect(url_for("index"))

    @app.route("/students/delete", methods=["POST"])
    def delete_student() -> Any:
        """Удаляет студента по ID."""
        try:
            s_id = int(request.form.get("id", "").strip())
            removed = group.remove(s_id)
            flash(f"Студент {removed.name} (ID: {removed.id}) удален.", "success")
        except (ValueError, StudentAppError) as err:
            flash(f"Ошибка удаления: {err}", "danger")

        return redirect(url_for("index"))

    @app.route("/export-top", methods=["GET"])
    def export_top() -> Any:
        """Экспортирует ТОП-N студентов в файл CSV."""
        if len(group) == 0:
            flash("Список пуст, экспорт невозможен.", "warning")
            return redirect(url_for("index"))

        try:
            n = int(request.args.get("n", 3))
            n = max(1, min(n, len(group)))
            top_students = group.get_top(n)

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False, encoding="utf-8"
            ) as tmp_file:
                tmp_path = Path(tmp_file.name)

            export_top_students_csv(tmp_path, top_students)
            return send_file(
                tmp_path,
                as_attachment=True,
                download_name=f"top_{n}_students.csv",
                mimetype="text/csv",
            )
        except (ValueError, StudentAppError) as err:
            flash(f"Ошибка экспорта: {err}", "danger")
            return redirect(url_for("index"))

    return app
