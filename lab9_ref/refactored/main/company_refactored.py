# refactored/models/company_refactored.py
"""
Рефакторенный Company с применением SOLID принципов
SRP - разделена на DepartmentManager, ProjectManager, FinancialCalculator
DIP - использует репозитории для хранилищ
OCP - система расширяется БЕЗ изменения Company
"""

from typing import List, Dict, Optional, Any
from ..validators import CompanyValidator
from ..interfaces import IDepartmentRepository, IProjectRepository
from ..repository import InMemoryDepartmentRepository, InMemoryProjectRepository
from ..services import SalaryCalculator
from ..exceptions import EmployeeNotFoundError, DepartmentNotFoundError
from .department_refactored import Department


class DepartmentManager:
    """SRP - управление отделами отделено"""
    
    def __init__(self, repository: IDepartmentRepository = None):
        self.__repository = repository or InMemoryDepartmentRepository()
    
    def add_department(self, department: Department) -> None:
        """Добавить отдел"""
        self.__repository.add(department)
    
    def get_department(self, name: str) -> Department:
        """Получить отдел по названию"""
        return self.__repository.get_by_id(name)
    
    def get_all_departments(self) -> List[Department]:
        """Получить все отделы"""
        return self.__repository.get_all()
    
    def get_department_count(self) -> int:
        """Получить количество отделов"""
        return len(self.get_all_departments())


class ProjectManager:
    """SRP - управление проектами отделено"""
    
    def __init__(self, repository: IProjectRepository = None):
        self.__repository = repository or InMemoryProjectRepository()
        self.__projects = {}
    
    def create_project(self, name: str, budget: float) -> None:
        """Создать проект"""
        if name in self.__projects:
            raise ValueError(f"Проект '{name}' уже существует")
        self.__projects[name] = {'budget': budget, 'employees': []}
    
    def add_employee_to_project(self, project_name: str, employee) -> None:
        """Добавить сотрудника в проект"""
        if project_name not in self.__projects:
            raise ValueError(f"Проект '{project_name}' не найден")
        self.__projects[project_name]['employees'].append(employee)
    
    def get_projects(self) -> Dict:
        """Получить все проекты"""
        return self.__projects.copy()
    
    def get_project_info(self, name: str) -> Dict:
        """Получить информацию о проекте"""
        if name not in self.__projects:
            raise ValueError(f"Проект '{name}' не найден")
        
        project = self.__projects[name]
        return {
            'name': name,
            'budget': project['budget'],
            'employees': len(project['employees']),
            'employee_list': [e.name for e in project['employees']]
        }


class FinancialCalculator:
    """SRP - финансовые расчеты отделены"""
    
    def __init__(self):
        pass
    
    def calculate_total_salary(self, employees: List) -> float:
        """Рассчитать общую зарплату"""
        return sum(e.calculate_salary() for e in employees)
    
    def calculate_total_expenses(self, departments: List[Department]) -> float:
        """Рассчитать общие расходы на зарплаты"""
        total = 0
        for dept in departments:
            total += dept.calculate_total_salary()
        return total
    
    def calculate_budget_per_department(self, departments: List[Department]) -> Dict:
        """Рассчитать бюджет по отделам"""
        return {
            dept.name: dept.calculate_total_salary()
            for dept in departments
        }
    
    def calculate_payroll_percentage(self, salary: float, total: float) -> float:
        """Рассчитать процент зарплаты от бюджета"""
        if total == 0:
            return 0
        return (salary / total) * 100
    
    def get_financial_report(self, departments: List[Department]) -> Dict:
        """Получить финансовый отчет"""
        total_expenses = self.calculate_total_expenses(departments)
        budget_by_dept = self.calculate_budget_per_department(departments)
        
        return {
            'total_salary_expenses': total_expenses,
            'budget_by_department': budget_by_dept,
            'average_salary_per_department': {
                name: total / len(dept.get_employees()) if dept.get_employees() else 0
                for name, total in budget_by_dept.items()
                for dept in departments if dept.name == name
            }
        }


class Company:
    """
    Главный класс компании
    SRP - координирует менеджеры (не содержит их логику)
    DIP - использует менеджеры через интерфейсы
    """
    
    def __init__(self, name: str):
        """
        Args:
            name: Название компании
        """
        CompanyValidator.validate_company_name(name)
        
        self.__name = name
        self.__department_manager = DepartmentManager()
        self.__project_manager = ProjectManager()
        self.__financial_calculator = FinancialCalculator()
    
    @property
    def name(self) -> str:
        """Получить название компании"""
        return self.__name
    
    # ===== ОТДЕЛЫ =====
    
    def add_department(self, department: Department) -> None:
        """Добавить отдел"""
        self.__department_manager.add_department(department)
    
    def get_department(self, name: str) -> Department:
        """Получить отдел по названию"""
        return self.__department_manager.get_department(name)
    
    def get_all_departments(self) -> List[Department]:
        """Получить все отделы"""
        return self.__department_manager.get_all_departments()
    
    def get_department_count(self) -> int:
        """Получить количество отделов"""
        return self.__department_manager.get_department_count()
    
    # ===== ПРОЕКТЫ =====
    
    def create_project(self, name: str, budget: float) -> None:
        """Создать проект"""
        self.__project_manager.create_project(name, budget)
    
    def add_employee_to_project(self, project_name: str, employee) -> None:
        """Добавить сотрудника в проект"""
        self.__project_manager.add_employee_to_project(project_name, employee)
    
    def get_projects(self) -> Dict:
        """Получить все проекты"""
        return self.__project_manager.get_projects()
    
    def get_project_info(self, name: str) -> Dict:
        """Получить информацию о проекте"""
        return self.__project_manager.get_project_info(name)
    
    # ===== ФИНАНСЫ =====
    
    def get_total_salary_expenses(self) -> float:
        """Получить общие расходы на зарплаты"""
        return self.__financial_calculator.calculate_total_expenses(
            self.get_all_departments()
        )
    
    def get_financial_report(self) -> Dict:
        """Получить финансовый отчет"""
        return self.__financial_calculator.get_financial_report(
            self.get_all_departments()
        )
    
    def get_budget_by_department(self) -> Dict:
        """Получить бюджет по отделам"""
        return self.__financial_calculator.calculate_budget_per_department(
            self.get_all_departments()
        )
    
    # ===== ИНФОРМАЦИЯ =====
    
    def get_total_employee_count(self) -> int:
        """Получить общее количество сотрудников"""
        return sum(dept.get_employee_count() for dept in self.get_all_departments())
    
    def get_average_salary_per_employee(self) -> float:
        """Получить среднюю зарплату на сотрудника"""
        total_salary = self.get_total_salary_expenses()
        total_employees = self.get_total_employee_count()
        
        if total_employees == 0:
            return 0
        return total_salary / total_employees
    
    def get_info(self) -> str:
        """Получить информацию о компании"""
        depts = self.get_all_departments()
        return (f"Компания: {self.__name}\n"
                f"Отделов: {self.get_department_count()}\n"
                f"Сотрудников: {self.get_total_employee_count()}\n"
                f"Расходы на зарплату: {self.get_total_salary_expenses():.2f}\n"
                f"Средняя зарплата: {self.get_average_salary_per_employee():.2f}")
    
    def get_full_report(self) -> Dict[str, Any]:
        """Получить полный отчет о компании"""
        return {
            'company': self.__name,
            'departments': len(self.get_all_departments()),
            'total_employees': self.get_total_employee_count(),
            'financial_report': self.get_financial_report(),
            'projects': self.get_projects(),
            'average_salary': self.get_average_salary_per_employee()
        }
    
    # ===== ОПЕРАТОРЫ =====
    
    def __str__(self) -> str:
        """Строковое представление"""
        return f"Компания '{self.__name}' ({self.get_department_count()} отделов, {self.get_total_employee_count()} человек)"
    
    def __repr__(self) -> str:
        """Официальное представление"""
        return f"Company(name='{self.__name}', departments={self.get_department_count()}, employees={self.get_total_employee_count()})"
