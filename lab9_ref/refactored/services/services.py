# refactored/services/salary_calculator.py
"""
SRP - Single Responsibility Principle
Сервис для расчета зарплаты
Отвечает ТОЛЬКО за расчеты, ничего больше
"""

from typing import List, Dict
from ..interfaces import ISalaryCalculable


class SalaryCalculator:
    """Калькулятор зарплаты"""
    
    @staticmethod
    def calculate_salary(employee: ISalaryCalculable) -> float:
        """Рассчитать зарплату для одного сотрудника
        
        Args:
            employee: Сотрудник
        
        Returns:
            float: Рассчитанная зарплата
        """
        return employee.calculate_salary()
    
    @staticmethod
    def calculate_total_salary(employees: List[ISalaryCalculable]) -> float:
        """Рассчитать общую зарплату для списка сотрудников
        
        Args:
            employees: Список сотрудников
        
        Returns:
            float: Общая сумма зарплат
        """
        total = 0.0
        for employee in employees:
            total += employee.calculate_salary()
        return total
    
    @staticmethod
    def calculate_average_salary(employees: List[ISalaryCalculable]) -> float:
        """Рассчитать среднюю зарплату
        
        Args:
            employees: Список сотрудников
        
        Returns:
            float: Средняя зарплата
        """
        if not employees:
            return 0.0
        total = SalaryCalculator.calculate_total_salary(employees)
        return total / len(employees)
    
    @staticmethod
    def get_salary_statistics(employees: List[ISalaryCalculable]) -> Dict[str, float]:
        """Получить статистику по зарплатам
        
        Args:
            employees: Список сотрудников
        
        Returns:
            dict: Словарь со статистикой
                  {
                      'total': 500000,       # Общая сумма
                      'average': 50000,     # Средняя
                      'min': 30000,         # Минимальная
                      'max': 120000,        # Максимальная
                      'count': 10           # Количество сотрудников
                  }
        """
        if not employees:
            return {
                'total': 0.0,
                'average': 0.0,
                'min': 0.0,
                'max': 0.0,
                'count': 0
            }
        
        salaries = [emp.calculate_salary() for emp in employees]
        
        return {
            'total': sum(salaries),
            'average': sum(salaries) / len(salaries),
            'min': min(salaries),
            'max': max(salaries),
            'count': len(salaries)
        }
    
    @staticmethod
    def group_by_salary_range(employees: List[ISalaryCalculable], 
                            ranges: List[tuple] = None) -> Dict[str, List]:
        """Группировать сотрудников по диапазонам зарплат
        
        Args:
            employees: Список сотрудников
            ranges: Список кортежей (min, max) для диапазонов
                   По умолчанию: [(0, 50000), (50000, 100000), (100000, float('inf'))]
        
        Returns:
            dict: Словарь {диапазон: [сотрудники]}
        """
        if ranges is None:
            ranges = [(0, 50000), (50000, 100000), (100000, float('inf'))]
        
        groups = {}
        for min_val, max_val in ranges:
            key = f"{min_val:,} - {max_val:,}"
            groups[key] = []
        
        for employee in employees:
            salary = employee.calculate_salary()
            for min_val, max_val in ranges:
                if min_val <= salary < max_val:
                    key = f"{min_val:,} - {max_val:,}"
                    groups[key].append(employee)
                    break
        
        return {k: v for k, v in groups.items() if v}  # Только непустые группы


# refactored/services/department_manager.py
"""
SRP - Single Responsibility Principle
Сервис для управления отделом
Отвечает ТОЛЬКО за управление отделом, ничего больше
"""

from typing import List, Optional, Dict
from ..interfaces import IEmployeeRepository


class DepartmentManager:
    """Менеджер отдела (управление сотрудниками)"""
    
    def __init__(self, name: str, repository: IEmployeeRepository = None):
        """
        Args:
            name: Название отдела
            repository: Репозиторий сотрудников (по умолчанию in-memory)
        """
        self.name = name
        self.repository = repository
    
    def add_employee(self, employee) -> None:
        """Добавить сотрудника в отдел"""
        if self.repository:
            self.repository.add(employee)
    
    def remove_employee(self, employee_id: int) -> None:
        """Удалить сотрудника из отдела"""
        if self.repository:
            self.repository.remove(employee_id)
    
    def get_employee(self, employee_id: int):
        """Получить сотрудника по ID"""
        if self.repository:
            return self.repository.get_by_id(employee_id)
        return None
    
    def get_all_employees(self) -> List:
        """Получить всех сотрудников отдела"""
        if self.repository:
            return self.repository.get_all()
        return []
    
    def find_employees(self, criteria: Dict) -> List:
        """Найти сотрудников по критериям"""
        if self.repository:
            return self.repository.find(criteria)
        return []
    
    def get_employee_count(self) -> int:
        """Получить количество сотрудников"""
        return len(self.get_all_employees())
    
    def has_employees(self) -> bool:
        """Проверить, есть ли сотрудники"""
        return self.get_employee_count() > 0
    
    def get_employee_ids(self) -> List[int]:
        """Получить ID всех сотрудников"""
        return [emp.id for emp in self.get_all_employees()]
