"""Точка входа для запуска консольного приложения."""

import sys

from lab.cli.app import CLIApp


def main() -> None:
    """Инициализирует и запускает приложение."""
    try:
        app = CLIApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nПрервано пользователем. Выход.")
        sys.exit(0)


if __name__ == "__main__":
    main()
