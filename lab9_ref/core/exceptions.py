"""исключения для системы учета сотрудников"""

class BaseAppError(Exception):
    """Базовое исключение приложения."""
    pass

class EmployeeNotFoundError(BaseAppError):
    """Исключение при отсутствии сотрудника."""
    def __init__(self, employee_id):
        super().__init__(f"Сотрудник с ID {employee_id} не найден")
        self.employee_id = employee_id


class DepartmentNotFoundError(BaseAppError):
    """Исключение при отсутствии отдела."""
    def __init__(self, department_name):
        super().__init__(f"Отдел '{department_name}' не найден")
        self.department_name = department_name


class ProjectNotFoundError(BaseAppError):
    """Исключение при отсутствии проекта."""
    def __init__(self, project_id):
        super().__init__(f"Проект с ID {project_id} не найден")
        self.project_id = project_id


class InvalidStatusError(BaseAppError):
    """Исключение при невалидном статусе."""
    def __init__(self, status, valid_statuses=None):
        msg = f"Невалидный статус: '{status}'"
        if valid_statuses:
            msg += f". Допустимые статусы: {', '.join(valid_statuses)}"
        super().__init__(msg)
        self.status = status
        self.valid_statuses = valid_statuses


class DuplicateIdError(BaseAppError):
    """Исключение при дублировании ID."""
    def __init__(self, entity_type, entity_id):
        super().__init__(f"{entity_type} с ID {entity_id} уже существует")
        self.entity_type = entity_type
        self.entity_id = entity_id

class ValidationError(BaseAppError):
    """Базовое исключение для ошибок валидации."""
    pass


class InvalidDataError(ValidationError):
    """Неверные данные."""
    def __init__(self, field, value, expected=None):
        msg = f"Неверное значение для {field}: {value}"
        if expected:
            msg += f". Ожидается: {expected}"
        super().__init__(msg)
        self.field = field
        self.value = value
        self.expected = expected


class FinancialValidationError(ValidationError):
    """Ошибка валидации финансовых данных."""
    def __init__(self, message):
        super().__init__(f"Финансовая ошибка: {message}")


class DatabaseError(BaseAppError):
    """Ошибка базы данных."""
    pass


class PermissionError(BaseAppError):
    """Ошибка доступа."""
    pass
