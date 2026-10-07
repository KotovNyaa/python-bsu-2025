"""Точка входа для локального запуска веб-сервера."""

import os

from lab.web.app import create_app


def main() -> None:
    """Запускает веб-приложение."""
    app = create_app()
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
