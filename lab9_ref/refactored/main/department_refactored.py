# refactored/models/department_refactored.py
"""
Рефакторенный Department с применением SOLID принципов
SRP - управление отделом отделено в отдельный класс
ISP - реализует только нужные интерфейсы
DIP - использует IEmployeeRepository вместо прямого списка
"""

from typing import List, Optional, Dict, Any
from ..validators import DepartmentValidator
from ..interfaces import IEmployeeRepository
from ..repository import InMemoryEmployeeRepository
from ..services import SalaryCalculator
from ..exceptions import EmployeeNotFoundError, DuplicateIdError


class Department:
    """Отдел компании с рефакторингом"""
    
    def __init__(self, name: str, repository: IEmployeeRepository = None):
        """
        Args:
            name: Название отдела
            repository: Репозиторий сотрудников (DIP)
                       По умолчанию в памяти
        """
        DepartmentValidator.validate_name(name)
        
        self.__name = name
        # DIP - используем интерфейс, а не конкретный класс
        self.__repository = repository or InMemoryEmployeeRepository()
    
    @property
    def name(self) -> str:
        """Возвращает название отдела"""
        return self.__name
    
    @name.setter
    def name(self, value: str) -> None:
        """Устанавливает название отдела"""
        DepartmentValidator.validate_name(value)
        self.__name = value
    
    # ===== УПРАВЛЕНИЕ СОТРУДНИКАМИ =====
    
    def add_employee(self, employee) -> None:
        """Добавить сотрудника в отдел"""
        try:
            self.__repository.add(employee)
        except DuplicateIdError as e:
            raise DuplicateIdError(
                entity_type="Сотрудник",
                entity_id=employee.id
            )
    
    def remove_employee(self, employee_id: int) -> None:
        """Удалить сотрудника по ID"""
        try:
            self.__repository.remove(employee_id)
        except EmployeeNotFoundError:
            raise EmployeeNotFoundError(employee_id)
    
    def get_employee(self, employee_id: int):
        """Получить сотрудника по ID"""
        return self.__repository.get_by_id(employee_id)
    
    def get_employees(self) -> List:
        """Получить всех сотрудников отдела"""
        return self.__repository.get_all()
    
    def find_employees(self, criteria: Dict) -> List:
        """Найти сотрудников по критериям"""
        return self.__repository.find(criteria)
    
    # ===== СТАТИСТИКА =====
    
    def get_employee_count(self) -> int:
        """Получить количество сотрудников"""
        return len(self.get_employees())
    
    def has_employees(self) -> bool:
        """Проверить, есть ли сотрудники в отделе"""
        return self.get_employee_count() > 0
    
    def get_employee_ids(self) -> List[int]:
        """Получить список ID сотрудников"""
        return [emp.id for emp in self.get_employees()]
    
    def get_employee_count_by_type(self) -> Dict[str, int]:
        """Получить статистику по типам сотрудников"""
        counts = {}
        for emp in self.get_employees():
            emp_type = emp.__class__.__name__
            counts[emp_type] = counts.get(emp_type, 0) + 1
        return counts
    
    # ===== ФИНАНСЫ =====
    
    def calculate_total_salary(self) -> float:
        """Рассчитать общую зарплату всех сотрудников"""
        return SalaryCalculator.calculate_total_salary(self.get_employees())
    
    def calculate_average_salary(self) -> float:
        """Рассчитать среднюю зарплату"""
        return SalaryCalculator.calculate_average_salary(self.get_employees())
    
    def get_salary_statistics(self) -> Dict[str, float]:
        """Получить статистику по зарплатам"""
        return SalaryCalculator.get_salary_statistics(self.get_employees())
    
    # ===== ИНФОРМАЦИЯ =====
    
    def get_info(self) -> str:
        """Получить информацию об отделе"""
        stats = self.get_employee_count_by_type()
        stats_str = ", ".join([f"{k}: {v}" for k, v in stats.items()])
        
        return (f"Отдел: {self.__name}\n"
                f"Сотрудников: {self.get_employee_count()}\n"
                f"По типам: {stats_str}\n"
                f"Общая зарплата: {self.calculate_total_salary():.2f}\n"
                f"Средняя зарплата: {self.calculate_average_salary():.2f}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертировать в словарь"""
        return {
            'name': self.__name,
            'employees': [emp.to_dict() for emp in self.get_employees()],
            'count': self.get_employee_count(),
            'total_salary': self.calculate_total_salary()
        }
    
    # ===== ОПЕРАТОРЫ =====
    
    def __str__(self) -> str:
        """Строковое представление"""
        return f"Отдел '{self.__name}' ({self.get_employee_count()} человек)"
    
    def __repr__(self) -> str:
        """Официальное представление"""
        return f"Department(name='{self.__name}', employees={self.get_employee_count()})"
    
    def __len__(self) -> int:
        """Количество сотрудников"""
        return self.get_employee_count()
    
    def __iter__(self):
        """Итератор по сотрудникам"""
        return iter(self.get_employees())
    
    def __getitem__(self, index: int):
        """Доступ по индексу"""
        employees = self.get_employees()
        if isinstance(index, int):
            if index < 0:
                index = len(employees) + index
            if 0 <= index < len(employees):
                return employees[index]
            raise IndexError(f"Индекс {index} вне диапазона")
        elif isinstance(index, slice):
            return employees[index]
        else:
            raise TypeError(f"Индекс должен быть int или slice")
    
    def __contains__(self, employee) -> bool:
        """Проверка наличия сотрудника"""
        return any(e.id == employee.id for e in self.get_employees())
