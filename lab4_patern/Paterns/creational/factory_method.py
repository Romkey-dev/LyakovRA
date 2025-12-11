from abc import ABC, abstractmethod
from core_OOP.Employee import Employee, Manager, Developer, Salesperson

class EmployeeFactory(ABC):
    """Абстрактная фабрика сотрудников (Factory Method)"""
    
    @abstractmethod
    def create_employee(self, **kwargs):
        pass


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
