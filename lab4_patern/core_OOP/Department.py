import json
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime

class Department:
    """Класс для отделов компании"""

    def __init__(self, name: str):
        """
        Args:
            name: Название отдела
        """
        if not isinstance(name, str) or name.strip() == "":
            raise InvalidDataError("Название отдела не должно быть пустой строкой")
        self.__name = name
        self.__employees: List[AbstractEmployee] = []

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        """Устанавливает название отдела"""
        if not isinstance(value, str) or value.strip() == "":
            raise InvalidDataError("Название отдела не должно быть пустой строкой")
        self.__name = value

    def add_employee(self, employee: AbstractEmployee) -> None:
        """
        Добавляет сотрудника

        Args:
            employee: Объект сотрудника для добавления

        ValueError: Если сотрудник уже есть в отделе
        """
        if not isinstance(employee, AbstractEmployee):
            raise InvalidDataError("Можно добавить только объект типа AbstractEmployee")

        # Проверка уникальности ID
        for emp in self.__employees:
            if emp.id == employee.id:
                raise DuplicateIdError(f"Сотрудник с ID {employee.id} уже есть в отделе")

        self.__employees.append(employee)

    def remove_employee(self, employee_id: int) -> None:
        """
        Удаляет сотрудника по ID

        Args:
            employee_id: ID сотрудника для удаления

        ValueError: Если сотрудник с таким ID не найден
        """
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise InvalidDataError("ID должен быть положительным целым числом")

        for i, emp in enumerate(self.__employees):
            if emp.id == employee_id:
                del self.__employees[i]
                return

        raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден в отделе")

    def get_employees(self) -> List[AbstractEmployee]:
        """
        Возвращает список всех сотрудников

        Returns:
            Копию списка сотрудников
        """
        return self.__employees.copy()

    def calculate_total_salary(self) -> float:
        """
        Вычисляет общую ЗП всех сотрудников

        Return:
            Сумма зарплат всех сотрудников
        """
        total = 0.0
        for employee in self.__employees:
            total += employee.calculate_salary()
        return total

    def get_employee_count(self) -> dict[str, int]:
        """
        Возвращает статистику по типам сотрудников

        Returns:
            Словарь {тип_сотрудника: количество}
        """
        counts = {
            "Employee": 0,
            "Manager": 0,
            "Developer": 0,
            "Salesperson": 0
        }

        for employee in self.__employees:
            class_name = employee.__class__.__name__
            if class_name in counts:
                counts[class_name] += 1
            else:
                counts[class_name] = 1

        # Удаляем нулевые знач
        return {k: v for k, v in counts.items() if v > 0}

    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """
        Ищет сотрудника по ID

        Args:
            employee_id: ID сотрудника для поиска

        Returns:
            Найденный сотрудник или None, если не найден
        """
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise InvalidDataError("ID должен быть положительным целым числом")

        for employee in self.__employees:
            if employee.id == employee_id:
                return employee

        return None

    def to_dict(self) -> dict:
        """Конвертирует отдел в словарь"""
        return {
            'name': self.__name,
            'employees': [emp.to_dict() for emp in self.__employees]
        }

    def save_to_file(self, filename: str) -> None:
        """
        Сохраняет всех сотрудников отдела в JSON файл.

        Args:
            filename: Имя файла для сохранения
:
        Error: Если не удалось сохранить файл
        """
        try:
            data = self.to_dict()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except (IOError, OSError) as e:
            raise IOError(f"Не удалось сохранить файл {filename}: {e}")

    @classmethod
    def load_from_file(cls, filename: str) -> 'Department':
        """
        Загружает отдел из JSON

        Args:
            filename: Имя файла для загрузки

        Returns:
            Загруженный отдел

        Error: Если не удалось загрузить файл
        ValueError: Если данные в файле некорректны
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (IOError, OSError, json.JSONDecodeError) as e:
            raise IOError(f"Не удалось загрузить файл {filename}: {e}")

        if 'name' not in data:
            raise InvalidDataError("Файл должен содержать поле 'name'")
        if 'employees' not in data:
            raise InvalidDataError("Файл должен содержать поле 'employees'")

        department = cls(data['name'])

        for emp_data in data['employees']:
            try:
                employee = EmployeeFactory.from_dict(emp_data)
                department.add_employee(employee)
            except (InvalidDataError, DuplicateIdError) as e:
                print(f"Предупреждение: не удалось загрузить сотрудника: {e}")
                continue

        return department

    # Перегрузка операторов
    def __len__(self) -> int:
        """Возвращает количество сотрудников в отделе"""
        return len(self.__employees)

    def __getitem__(self, key) -> AbstractEmployee:
        """
        Доступ к сотруднику по индексу

        Args:
            key: Индекс сотрудника или срез

        Returns:
            Сотрудник или список сотрудников

        IndError: Если индекс вне диапазона
        TypeError: Если ключ не int или slice
        """
        if isinstance(key, int):
            if key < 0:
                key = len(self.__employees) + key
            if 0 <= key < len(self.__employees):
                return self.__employees[key]
            raise IndexError(f"Индекс {key} вне диапазона [0, {len(self.__employees) - 1}]")
        elif isinstance(key, slice):
            return self.__employees[key]
        else:
            raise TypeError(f"Индекс должен быть int или slice, а не {type(key).__name__}")

    def __contains__(self, employee: AbstractEmployee) -> bool:
        """
        Проверка принадлежности сотрудника отделу

        Args:
            employee: Сотрудник для проверки

        Returns:
            True если сотрудник в отделе, иначе False
        """
        if not isinstance(employee, AbstractEmployee):
            return False

        for emp in self.__employees:
            if emp == employee:
                return True
        return False

    def __str__(self) -> str:
        """Строковое представление отдела"""
        return f"Отдел: {self.__name}, Сотрудников: {len(self)}"

    def __iter__(self):
        """Итератор по сотрудникам отдела"""
        return iter(self.__employees)

    def __repr__(self) -> str:
        """Официальное строковое представление"""
        return f"Department(name='{self.__name}', employees={len(self.__employees)})"

    # связи
    def has_employees(self) -> bool:
        """
        Проверяет, есть ли сотрудники в отделе

        Returns:
            True если есть сотрудники, иначе False
        """
        return len(self.__employees) > 0

    def get_employee_ids(self) -> List[int]:
        """
        Возвращает список ID всех сотрудников отдела

        Returns:
            Список ID сотрудников
        """
        return [emp.id for emp in self.__employees]
