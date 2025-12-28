# refactored/models/employee_refactored.py
"""
Рефакторенный Employee с применением принципов SOLID
SRP - валидация отделена в отдельный класс
LSP - правильная иерархия наследования
ISP - реализует только нужные интерфейсы
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..validators import EmployeeValidator
from ..interfaces import ISalaryCalculable, IInfoProvidable, ISkillManageable, IBonusCalculable, ICommissionCalculable


class AbstractEmployee(ISalaryCalculable, IInfoProvidable, ABC):
    """Абстрактный класс для всех сотрудников"""
    
    def __init__(self, id_empl: int, name: str, department: str, base_salary: float):
        """
        Args:
            id_empl: ID сотрудника
            name: Имя
            department: Название отдела
            base_salary: Базовая зарплата
        """
        # Используем валидаторы (SRP)
        EmployeeValidator.validate_id(id_empl)
        EmployeeValidator.validate_name(name)
        EmployeeValidator.validate_department(department)
        EmployeeValidator.validate_salary(base_salary)
        
        self.__id = id_empl
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary
    
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def department(self) -> str:
        return self.__department
    
    @property
    def base_salary(self) -> float:
        return self.__base_salary
    
    @abstractmethod
    def calculate_salary(self) -> float:
        """Рассчитать зарплату"""
        pass
    
    @abstractmethod
    def get_info(self) -> str:
        """Получить информацию о сотруднике"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертировать в словарь"""
        return {
            'type': self.__class__.__name__,
            'id': self.__id,
            'name': self.__name,
            'department': self.__department,
            'base_salary': self.__base_salary
        }
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.__id}, name='{self.__name}', dept='{self.__department}')"
    
    def __repr__(self) -> str:
        return self.__str__()


class Employee(AbstractEmployee):
    """Обычный сотрудник (базовый класс)"""
    
    def calculate_salary(self) -> float:
        """Зарплата = базовая зарплата"""
        return self.base_salary
    
    def get_info(self) -> str:
        """Информация о сотруднике"""
        return (f"Сотрудник: {self.name}\n"
                f"ID: {self.id}\n"
                f"Отдел: {self.department}\n"
                f"Зарплата: {self.calculate_salary():.2f}")


class Developer(AbstractEmployee, ISkillManageable):
    """Разработчик (Developer + Skills)"""
    
    def __init__(self, id_empl: int, name: str, department: str, 
                 base_salary: float, level: str = "junior"):
        """
        Args:
            level: Уровень (junior/middle/senior)
        """
        super().__init__(id_empl, name, department, base_salary)
        self.level = level
        self.__skills: List[str] = []
    
    def calculate_salary(self) -> float:
        """Зарплата зависит от уровня"""
        multipliers = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
        return self.base_salary * multipliers.get(self.level, 1.0)
    
    def add_skill(self, skill: str) -> None:
        """Добавить навык"""
        if skill not in self.__skills:
            self.__skills.append(skill)
    
    def remove_skill(self, skill: str) -> None:
        """Удалить навык"""
        if skill in self.__skills:
            self.__skills.remove(skill)
    
    def get_skills(self) -> List[str]:
        """Получить список навыков"""
        return self.__skills.copy()
    
    def get_info(self) -> str:
        """Информация о разработчике"""
        skills_str = ", ".join(self.__skills) if self.__skills else "нет"
        return (f"Разработчик: {self.name} ({self.level})\n"
                f"ID: {self.id}\n"
                f"Отдел: {self.department}\n"
                f"Навыки: {skills_str}\n"
                f"Зарплата: {self.calculate_salary():.2f}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертировать в словарь"""
        data = super().to_dict()
        data['level'] = self.level
        data['skills'] = self.__skills.copy()
        return data


class Manager(AbstractEmployee, IBonusCalculable):
    """Менеджер (Manager + Bonus)"""
    
    def __init__(self, id_empl: int, name: str, department: str, 
                 base_salary: float, bonus_strategy=None):
        """
        Args:
            bonus_strategy: Стратегия расчета бонуса (Strategy Pattern)
        """
        super().__init__(id_empl, name, department, base_salary)
        from ..strategies.bonus_strategy import NoBonusStrategy
        self.bonus_strategy = bonus_strategy or NoBonusStrategy()
    
    def calculate_salary(self) -> float:
        """Зарплата = базовая + бонус"""
        return self.base_salary + self.calculate_bonus()
    
    def calculate_bonus(self) -> float:
        """Рассчитать бонус используя стратегию"""
        return self.bonus_strategy.calculate(self)
    
    def set_bonus_strategy(self, strategy) -> None:
        """Изменить стратегию расчета бонуса (OCP)"""
        self.bonus_strategy = strategy
    
    def get_info(self) -> str:
        """Информация о менеджере"""
        return (f"Менеджер: {self.name}\n"
                f"ID: {self.id}\n"
                f"Отдел: {self.department}\n"
                f"Базовая зарплата: {self.base_salary:.2f}\n"
                f"Бонус: {self.calculate_bonus():.2f}\n"
                f"Итого: {self.calculate_salary():.2f}\n"
                f"Стратегия: {self.bonus_strategy.get_name()}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертировать в словарь"""
        data = super().to_dict()
        data['bonus'] = self.calculate_bonus()
        return data


class Salesperson(AbstractEmployee, ICommissionCalculable):
    """Менеджер по продажам (Salesperson + Commission)"""
    
    def __init__(self, id_empl: int, name: str, department: str, 
                 base_salary: float, commission_rate: float = 0.05):
        """
        Args:
            commission_rate: Процент комиссии (0.05 = 5%)
        """
        super().__init__(id_empl, name, department, base_salary)
        self.commission_rate = commission_rate
        self.sales_amount = 0.0
    
    def calculate_salary(self) -> float:
        """Зарплата = базовая + комиссия"""
        return self.base_salary + self.calculate_commission()
    
    def calculate_commission(self) -> float:
        """Рассчитать комиссию от объема продаж"""
        return self.sales_amount * self.commission_rate
    
    def set_sales_amount(self, amount: float) -> None:
        """Установить объем продаж"""
        if amount < 0:
            raise ValueError("Объем продаж не может быть отрицательным")
        self.sales_amount = amount
    
    def get_info(self) -> str:
        """Информация о менеджере по продажам"""
        return (f"Менеджер по продажам: {self.name}\n"
                f"ID: {self.id}\n"
                f"Отдел: {self.department}\n"
                f"Базовая зарплата: {self.base_salary:.2f}\n"
                f"Объем продаж: {self.sales_amount:.2f}\n"
                f"Комиссия ({self.commission_rate*100}%): {self.calculate_commission():.2f}\n"
                f"Итого: {self.calculate_salary():.2f}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертировать в словарь"""
        data = super().to_dict()
        data['commission_rate'] = self.commission_rate
        data['sales_amount'] = self.sales_amount
        return data
