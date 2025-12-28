# refactored/validators.py
"""
SRP - Single Responsibility Principle
Все валидаторы отделены в отдельные классы
"""

from .exceptions import InvalidDataError, FinancialValidationError


class BaseValidator:
    """Базовые методы валидации для всех классов"""
    
    @staticmethod
    def validate_not_empty_string(value: str, field_name: str) -> None:
        """Проверяет, что строка не пустая"""
        if not isinstance(value, str) or not value.strip():
            raise InvalidDataError(f"{field_name} не должно быть пустой строкой")
    
    @staticmethod
    def validate_positive_integer(value: int, field_name: str) -> None:
        """Проверяет, что число положительное целое"""
        if not isinstance(value, int) or value <= 0:
            raise InvalidDataError(f"{field_name} должно быть положительным целым числом")
    
    @staticmethod
    def validate_positive_number(value: float, field_name: str) -> None:
        """Проверяет, что число положительное (int или float)"""
        if not isinstance(value, (int, float)) or value <= 0:
            raise InvalidDataError(f"{field_name} должно быть положительным числом")
    
    @staticmethod
    def validate_type(value, expected_type, field_name: str) -> None:
        """Проверяет тип значения"""
        if not isinstance(value, expected_type):
            raise InvalidDataError(
                f"{field_name} должно быть типа {expected_type.__name__}, "
                f"получено {type(value).__name__}"
            )


class EmployeeValidator(BaseValidator):
    """Валидация данных Employee"""
    
    @staticmethod
    def validate_id(value: int) -> None:
        """Валидация ID сотрудника"""
        EmployeeValidator.validate_positive_integer(value, "ID сотрудника")
    
    @staticmethod
    def validate_name(value: str) -> None:
        """Валидация имени сотрудника"""
        EmployeeValidator.validate_not_empty_string(value, "Имя сотрудника")
    
    @staticmethod
    def validate_department(value: str) -> None:
        """Валидация названия отдела"""
        EmployeeValidator.validate_not_empty_string(value, "Название отдела")
    
    @staticmethod
    def validate_salary(value: float) -> None:
        """Валидация базовой зарплаты"""
        if not isinstance(value, (int, float)) or value <= 0:
            raise FinancialValidationError(
                "Базовая зарплата должна быть положительным числом"
            )


class DepartmentValidator(BaseValidator):
    """Валидация данных Department"""
    
    @staticmethod
    def validate_name(value: str) -> None:
        """Валидация названия отдела"""
        DepartmentValidator.validate_not_empty_string(value, "Название отдела")


class CompanyValidator(BaseValidator):
    """Валидация данных Company"""
    
    @staticmethod
    def validate_name(value: str) -> None:
        """Валидация названия компании"""
        CompanyValidator.validate_not_empty_string(value, "Название компании")


class ProjectValidator(BaseValidator):
    """Валидация данных Project"""
    
    @staticmethod
    def validate_project_id(value: int) -> None:
        """Валидация ID проекта"""
        ProjectValidator.validate_positive_integer(value, "ID проекта")
    
    @staticmethod
    def validate_name(value: str) -> None:
        """Валидация названия проекта"""
        ProjectValidator.validate_not_empty_string(value, "Название проекта")
    
    @staticmethod
    def validate_description(value: str) -> None:
        """Валидация описания проекта"""
        ProjectValidator.validate_type(value, str, "Описание проекта")
    
    @staticmethod
    def validate_status(value: str, valid_statuses: set) -> None:
        """Валидация статуса проекта"""
        if value not in valid_statuses:
            raise InvalidDataError(
                f"Статус должен быть одним из: {valid_statuses}"
            )
