# refactored/interfaces.py
"""
ISP - Interface Segregation Principle
Разделение интерфейсов по функциональности
Классы реализуют только те интерфейсы, которые им нужны
"""

from abc import ABC, abstractmethod
from typing import List


class ISalaryCalculable(ABC):
    """Интерфейс для объектов, у которых можно рассчитать зарплату"""
    
    @abstractmethod
    def calculate_salary(self) -> float:
        """Расчет зарплаты
        
        Returns:
            float: Рассчитанная зарплата
        """
        pass


class IInfoProvidable(ABC):
    """Интерфейс для объектов, которые могут предоставить информацию о себе"""
    
    @abstractmethod
    def get_info(self) -> str:
        """Получить информацию об объекте
        
        Returns:
            str: Информация в виде строки
        """
        pass


class ISkillManageable(ABC):
    """Интерфейс для управления навыками (для разработчиков)"""
    
    @abstractmethod
    def add_skill(self, skill: str) -> None:
        """Добавить навык"""
        pass
    
    @abstractmethod
    def remove_skill(self, skill: str) -> None:
        """Удалить навык"""
        pass
    
    @abstractmethod
    def get_skills(self) -> List[str]:
        """Получить список навыков"""
        pass


class IBonusCalculable(ABC):
    """Интерфейс для расчета бонусов (для менеджеров)"""
    
    @abstractmethod
    def calculate_bonus(self) -> float:
        """Расчет бонуса
        
        Returns:
            float: Размер бонуса
        """
        pass


class ICommissionCalculable(ABC):
    """Интерфейс для расчета комиссий (для менеджеров по продажам)"""
    
    @abstractmethod
    def calculate_commission(self) -> float:
        """Расчет комиссии
        
        Returns:
            float: Размер комиссии
        """
        pass


class ITargetable(ABC):
    """Интерфейс для объектов с целевыми показателями"""
    
    @abstractmethod
    def set_target(self, target: float) -> None:
        """Установить целевой показатель"""
        pass
    
    @abstractmethod
    def get_target(self) -> float:
        """Получить целевой показатель"""
        pass
    
    @abstractmethod
    def get_achievement(self) -> float:
        """Получить процент выполнения цели"""
        pass


class IEmployeeRepository(ABC):
    """Интерфейс хранилища сотрудников (DIP)"""
    
    @abstractmethod
    def add(self, employee) -> None:
        """Добавить сотрудника"""
        pass
    
    @abstractmethod
    def remove(self, employee_id: int) -> None:
        """Удалить сотрудника по ID"""
        pass
    
    @abstractmethod
    def get_by_id(self, employee_id: int):
        """Получить сотрудника по ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List:
        """Получить всех сотрудников"""
        pass
    
    @abstractmethod
    def find(self, criteria: dict) -> List:
        """Найти сотрудников по критериям"""
        pass


class IDepartmentRepository(ABC):
    """Интерфейс хранилища отделов"""
    
    @abstractmethod
    def add(self, department) -> None:
        """Добавить отдел"""
        pass
    
    @abstractmethod
    def remove(self, department_name: str) -> None:
        """Удалить отдел"""
        pass
    
    @abstractmethod
    def get_by_name(self, name: str):
        """Получить отдел по названию"""
        pass
    
    @abstractmethod
    def get_all(self) -> List:
        """Получить все отделы"""
        pass


class IProjectRepository(ABC):
    """Интерфейс хранилища проектов"""
    
    @abstractmethod
    def add(self, project) -> None:
        """Добавить проект"""
        pass
    
    @abstractmethod
    def remove(self, project_id: int) -> None:
        """Удалить проект"""
        pass
    
    @abstractmethod
    def get_by_id(self, project_id: int):
        """Получить проект по ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List:
        """Получить все проекты"""
        pass


class IFinancialCalculator(ABC):
    """Интерфейс для финансовых расчетов"""
    
    @abstractmethod
    def calculate_total_salary(self, employees: List) -> float:
        """Рассчитать общую зарплату"""
        pass
    
    @abstractmethod
    def calculate_department_cost(self, department) -> float:
        """Рассчитать стоимость отдела"""
        pass
    
    @abstractmethod
    def get_salary_statistics(self, employees: List) -> dict:
        """Получить статистику по зарплатам"""
        pass
