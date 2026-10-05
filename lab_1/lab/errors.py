"""Иерархия исключений приложения."""


class StudentAppError(Exception):
    """Базовое исключение для ошибок приложения."""


class ValidationError(StudentAppError):
    """Ошибка валидации данных студента или параметров."""


class DuplicateStudentError(StudentAppError):
    """Студент с таким идентификатором уже существует."""


class StudentNotFoundError(StudentAppError):
    """Студент с указанным идентификатором не найден."""


class EmptyGroupError(StudentAppError):
    """Операция невозможна над пустой группой студентов."""


class FileStorageError(StudentAppError):
    """Базовая ошибка при работе с файловым хранилищем."""


class FileNotFoundAppError(FileStorageError):
    """Указанный файл не найден."""


class FileAccessError(FileStorageError):
    """Ошибка прав доступа при работе с файлом."""


class CSVFormatError(FileStorageError):
    """Файл CSV поврежден или имеет неверную структуру."""
