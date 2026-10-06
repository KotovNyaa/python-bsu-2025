"""Точка входа для запуска консольного приложения."""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

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
