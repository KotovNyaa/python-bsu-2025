# Учет успеваемости студентов (CSV)

Консольное и веб-приложение для управления списком студентов и их оценок на основе CSV-файлов.

---

## Быстрый запуск через Pixi

Проект использует [Pixi](https://pixi.sh) для управления окружением и задачами:

```bash
# Установка всех зависимостей
pixi install

# Запуск консольного приложения (CLI)
pixi run start

# Запуск локального веб-сервера (http://localhost:5000)
pixi run start-web

# Запуск автотестов
pixi run test

# Проверка стиля (линтер) и форматирование
pixi run lint
pixi run format
```

---

## Запуск без Pixi (Python 3.10+)

```bash
# Установка базовых зависимостей
pip install flask pytest ruff

# Запуск CLI
python -m lab.main

# Запуск веб-приложения
python -m lab.web_main

# Прогон тестов
pytest -q
```

---

## Запуск в Docker

```bash
docker build -t students-app .
docker run --rm -p 5000:5000 students-app
```

---

## Структура проекта

* `lab/models.py` — модель данных `Student` и расчет среднего балла.
* `lab/processing.py` — контейнер `StudentGroup`, фильтрация, сортировка, статистика.
* `lab/io_utils.py` — потоковый ввод/вывод CSV, автодетекция заголовков, экспорт ТОП-N.
* `lab/errors.py` — иерархия специализированных исключений.
* `lab/cli/` — консольное меню и форматирование ASCII-таблиц.
* `lab/web/` — веб-интерфейс на Flask (дашборд и управление).
* `data/students.csv` — пример входного файла данных.
* `tests/` — набор тестов pytest (модели, логика, ввод/вывод, CLI).
