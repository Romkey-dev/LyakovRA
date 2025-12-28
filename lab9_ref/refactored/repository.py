# refactored/repository.py
"""
DIP - Dependency Inversion Principle
Repository Pattern для управления хранилищем сотрудников
Система зависит от интерфейса, а не от конкретной реализации
"""

from typing import List, Optional, Dict, Any
from .interfaces import IEmployeeRepository, IDepartmentRepository, IProjectRepository
from .exceptions import DuplicateIdError, EmployeeNotFoundError, DepartmentNotFoundError


class InMemoryEmployeeRepository(IEmployeeRepository):
    """Хранилище сотрудников в памяти"""
    
    def __init__(self):
        self.__employees: List[Any] = []
    
    def add(self, employee) -> None:
        """Добавить сотрудника"""
        if any(e.id == employee.id for e in self.__employees):
            raise DuplicateIdError(
                entity_type="Сотрудник",
                entity_id=employee.id
            )
        self.__employees.append(employee)
    
    def remove(self, employee_id: int) -> None:
        """Удалить сотрудника по ID"""
        for i, emp in enumerate(self.__employees):
            if emp.id == employee_id:
                del self.__employees[i]
                return
        raise EmployeeNotFoundError(employee_id)
    
    def get_by_id(self, employee_id: int) -> Optional[Any]:
        """Получить сотрудника по ID"""
        for emp in self.__employees:
            if emp.id == employee_id:
                return emp
        return None
    
    def get_all(self) -> List[Any]:
        """Получить всех сотрудников"""
        return self.__employees.copy()
    
    def find(self, criteria: Dict[str, Any]) -> List[Any]:
        """Найти сотрудников по критериям
        
        Args:
            criteria: Словарь с критериями поиска
                      {'department': 'IT', 'level': 'senior'}
        
        Returns:
            Список найденных сотрудников
        """
        results = []
        for emp in self.__employees:
            match = True
            for key, value in criteria.items():
                if not hasattr(emp, key) or getattr(emp, key) != value:
                    match = False
                    break
            if match:
                results.append(emp)
        return results
    
    def update(self, employee_id: int, employee) -> None:
        """Обновить данные сотрудника"""
        for i, emp in enumerate(self.__employees):
            if emp.id == employee_id:
                self.__employees[i] = employee
                return
        raise EmployeeNotFoundError(employee_id)
    
    def clear(self) -> None:
        """Очистить хранилище (полезно для тестов)"""
        self.__employees.clear()
    
    def count(self) -> int:
        """Получить количество сотрудников"""
        return len(self.__employees)


class DatabaseEmployeeRepository(IEmployeeRepository):
    """Хранилище сотрудников в базе данных"""
    
    def __init__(self, connection=None):
        """
        Args:
            connection: Объект подключения к БД
        """
        self.connection = connection
    
    def add(self, employee) -> None:
        """Добавить сотрудника в БД"""
        # Реализация сохранения в БД
        if self.connection is None:
            raise RuntimeError("Подключение к БД не установлено")
        # TODO: SQL INSERT запрос
        pass
    
    def remove(self, employee_id: int) -> None:
        """Удалить сотрудника из БД"""
        # TODO: SQL DELETE запрос
        pass
    
    def get_by_id(self, employee_id: int) -> Optional[Any]:
        """Получить сотрудника из БД"""
        # TODO: SQL SELECT запрос
        pass
    
    def get_all(self) -> List[Any]:
        """Получить всех сотрудников из БД"""
        # TODO: SQL SELECT запрос
        pass
    
    def find(self, criteria: Dict[str, Any]) -> List[Any]:
        """Найти сотрудников в БД по критериям"""
        # TODO: SQL SELECT с WHERE
        pass


class InMemoryDepartmentRepository(IDepartmentRepository):
    """Хранилище отделов в памяти"""
    
    def __init__(self):
        self.__departments: List[Any] = []
    
    def add(self, department) -> None:
        """Добавить отдел"""
        if any(d.name == department.name for d in self.__departments):
            raise DuplicateIdError(
                entity_type="Отдел",
                entity_id=department.name
            )
        self.__departments.append(department)
    
    def remove(self, department_name: str) -> None:
        """Удалить отдел"""
        for i, dept in enumerate(self.__departments):
            if dept.name == department_name:
                del self.__departments[i]
                return
        raise DepartmentNotFoundError(f"Отдел '{department_name}' не найден")
    
    def get_by_name(self, name: str) -> Optional[Any]:
        """Получить отдел по названию"""
        for dept in self.__departments:
            if dept.name == name:
                return dept
        return None
    
    def get_all(self) -> List[Any]:
        """Получить все отделы"""
        return self.__departments.copy()


class InMemoryProjectRepository(IProjectRepository):
    """Хранилище проектов в памяти"""
    
    def __init__(self):
        self.__projects: List[Any] = []
    
    def add(self, project) -> None:
        """Добавить проект"""
        if any(p.project_id == project.project_id for p in self.__projects):
            raise DuplicateIdError(
                entity_type="Проект",
                entity_id=project.project_id
            )
        self.__projects.append(project)
    
    def remove(self, project_id: int) -> None:
        """Удалить проект"""
        for i, proj in enumerate(self.__projects):
            if proj.project_id == project_id:
                del self.__projects[i]
                return
        raise EmployeeNotFoundError(f"Проект с ID {project_id} не найден")
    
    def get_by_id(self, project_id: int) -> Optional[Any]:
        """Получить проект по ID"""
        for proj in self.__projects:
            if proj.project_id == project_id:
                return proj
        return None
    
    def get_all(self) -> List[Any]:
        """Получить все проекты"""
        return self.__projects.copy()
    
    def find_by_status(self, status: str) -> List[Any]:
        """Найти проекты по статусу"""
        return [p for p in self.__projects if p.status == status]
