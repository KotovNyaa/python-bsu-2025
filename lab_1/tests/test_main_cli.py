"""Интеграционные тесты консольного интерфейса пользователя."""

from pathlib import Path

import pytest

from lab.cli.app import CLIApp


def test_cli_exit_immediately(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Проверяет чистый выход из меню по команде 0."""
    monkeypatch.setattr("builtins.input", lambda _: "0")
    app = CLIApp()
    app.run()

    captured = capsys.readouterr().out
    assert "Работа завершена. До свидания!" in captured


def test_cli_help_menu(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Проверяет вызов справки по команде '?'."""
    inputs = iter(["?", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    app = CLIApp()
    app.run()

    captured = capsys.readouterr().out
    assert "УПРАВЛЕНИЕ СПИСКОМ СТУДЕНТОВ" in captured


def test_cli_happy_path(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    sample_csv_with_header: Path,
) -> None:
    """Проверяет сквозной сценарий: загрузка, просмотр, статистика, сортировка, выход."""
    inputs = iter(
        [
            "1",
            str(sample_csv_with_header),
            "3",
            "7",
            "9",
            "avg",
            "0",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    app = CLIApp()
    app.run()

    captured = capsys.readouterr().out
    assert "Успешно загружено студентов: 3" in captured
    assert "Иванов Иван" in captured
    assert "Статистика по группе" in captured
    assert "Результат сортировки по 'avg':" in captured


def test_cli_resilience_to_errors(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Проверяет, что при ошибках (неверный файл, удаление) CLI не падает."""
    inputs = iter(
        [
            "1",
            "non_existent_file_123.csv",
            "5",
            "0",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    app = CLIApp()
    app.run()

    captured = capsys.readouterr().out
    assert "Ошибка" in captured
    assert "Список студентов пуст. Удалять некого." in captured
    assert "Работа завершена" in captured
