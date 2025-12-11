import json
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime
from .exceptions import (
    InvalidDataError,
    FinancialValidationError,
    DuplicateIdError
)

class Employee(AbstractEmployee):
    def __init__(self, id_empl, name, department, base_salary):
        self.__validate_id(id_empl)
        self.__validate_name(name)
        self.__validate_department(department)
        self.__validate_salary(base_salary)

        self.__id = id_empl
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary

    def __validate_id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise InvalidDataError("ID должен быть положительным целым числом")

    def __validate_name(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise InvalidDataError("Имя не должно быть пустой строкой")

    def __validate_department(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise InvalidDataError("Отдел не должен быть пустой строкой")

    def __validate_salary(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise FinancialValidationError("Зарплата должна быть положительным числом")

    def get_all(self):
        return (self.__id, self.__name, self.__department, self.__base_salary)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__validate_id(value)
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__validate_name(value)
        self.__name = value

    @property
    def department(self):
        return self.__department

    @department.setter
    def department(self, value):
        self.__validate_department(value)
        self.__department = value

    @property
    def base_salary(self):
        return self.__base_salary

    @base_salary.setter
    def base_salary(self, value):
        self.__validate_salary(value)
        self.__base_salary = value

    def __str__(self):
        return f"Сотрудник [id: {self.__id}, имя: {self.__name}, отдел: {self.__department}, базовая зарплата: {self.__base_salary}]"

    def calculate_salary(self) -> float:
        return self.__base_salary

    def get_info(self) -> str:
        return f"{self.__str__()}, Рассчитанная зарплата: {self.calculate_salary()}"

    def to_dict(self) -> dict:
        """Конвертирует сотрудника в словарь"""
        return {
            'type': self.__class__.__name__,
            'id': self.__id,
            'name': self.__name,
            'department': self.__department,
            'base_salary': self.__base_salary
        }

@classmethod
    def from_dict(cls, data: dict) -> 'Employee':
        """Создает сотрудника из словаря с валидацией"""
        required_fields = ['id', 'name', 'department', 'base_salary']
        
        for field in required_fields:
            if field not in data:
                raise InvalidDataError(
                    field=f"обязательное поле '{field}'",
                    value="отсутствует",
                    expected="присутствует в данных"
                )
        
        # Проверяем тип данных
        if not isinstance(data['id'], int):
            raise InvalidDataError(
                field="id",
                value=data['id'],
                expected="целое число"
            )
        
        return cls(
            id_empl=data['id'],
            name=data['name'],
            department=data['department'],
            base_salary=data['base_salary']
        )
