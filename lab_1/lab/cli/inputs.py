"""Утилиты для безопасного считывания пользовательского ввода."""


def ask_string(prompt: str) -> str:
    """Запрашивает непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: значение не может быть пустым.")


def ask_int(prompt: str, min_val: int | None = None, max_val: int | None = None) -> int:
    """Запрашивает целое число с проверкой диапазона."""
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if min_val is not None and val < min_val:
                print(f"Ошибка: число должно быть >= {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Ошибка: число должно быть <= {max_val}.")
                continue
            return val
        except ValueError:
            print("Ошибка: введите корректное целое число.")


def ask_menu_choice(prompt: str) -> str:
    """Считывает выбор меню: цифру от 0 до 9 или команду '?' / 'help'."""
    while True:
        raw = input(prompt).strip().lower()
        if raw in [str(i) for i in range(10)] or raw in ("?", "h", "help"):
            return raw
        print("Ошибка: введите цифру [0-9] или '?' для вызова меню.")


def ask_grades(prompt: str) -> list[int | None]:
    """Считывает оценки через пробел. Символ '-' или пустота означает пропуск."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            return []

        tokens = raw.split()
        grades: list[int | None] = []
        valid = True

        for token in tokens:
            if token in ("-", "_", "none", "None"):
                grades.append(None)
                continue
            try:
                grade = int(token)
                if not (0 <= grade <= 100):
                    print(f"Ошибка: оценка '{grade}' вне диапазона от 0 до 100.")
                    valid = False
                    break
                grades.append(grade)
            except ValueError:
                print(f"Ошибка: некорректная отметка '{token}'.")
                valid = False
                break

        if valid:
            return grades
