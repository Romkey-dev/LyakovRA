from abc import ABC, abstractmethod
from core_OOP.Employee import Employee, Manager, Developer, Salesperson
from core_OOP.exceptions import InvalidDataError


class EmployeeFactory(ABC):
    """Абстрактная фабрика сотрудников (Factory Method)"""
    
    @staticmethod
    def create_employee(emp_type: str, **kwargs):
        if emp_type not in cls._employee_classes:
            available = ', '.join(cls._employee_classes.keys())
            raise InvalidDataError(
                field="тип сотрудника",
                value=emp_type,
                expected=f"один из: {available}"
            )
        
        required = cls._required_params[emp_type]
        missing = [param for param in required if param not in kwargs]
        
        if missing:
            raise InvalidDataError(
                field="обязательные параметры",
                value="отсутствуют",
                expected=f"присутствуют: {', '.join(missing)}"
            )


class DeveloperFactory(EmployeeFactory):
    """Фабрика для создания разработчиков"""
    
    def create_employee(self, **kwargs):
        return Developer(
            id_empl=kwargs['id'],
            name=kwargs['name'],
            department=kwargs.get('department', 'Development'),
            base_salary=kwargs['base_salary'],
            tech_stack=kwargs.get('tech_stack', []),
            seniority_level=kwargs.get('seniority_level', 'junior')
        )


class ManagerFactory(EmployeeFactory):
    """Фабрика для создания менеджеров"""
    
    def create_employee(self, **kwargs):
        return Manager(
            id_empl=kwargs['id'],
            name=kwargs['name'],
            department=kwargs.get('department', 'Management'),
            base_salary=kwargs['base_salary'],
            bonus=kwargs.get('bonus', 0)
        )
