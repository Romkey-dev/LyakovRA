import json
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime

class Company:
    """компания"""

    def __init__(self, name: str):
        """
        Args:
            name: Название компании

        ValueError: Если название пустое
        """
        if not isinstance(name, str) or name.strip() == "":
            raise InvalidDataError("Название компании не должно быть пустой строкой")

        self.__name = name
        self.__departments: List[Department] = []
        self.__projects: List[Project] = []

    @property
    def name(self) -> str:
        """Возвращает название комп"""
        return self.__name

    # управления отделами

    def add_department(self, department: Department) -> None:
        """
        Добавляет отдел в компанию

        Args:
            department: Отдел для добавления

        ValueError: Если отдел уже есть в компании
        """
        if not isinstance(department, Department):
            raise InvalidDataError("Можно добавить только объект типа Department")

        # Проверка
        for dept in self.__departments:
            if dept.name == department.name:
                raise DuplicateIdError(f"Отдел с названием '{department.name}' уже существует")

        self.__departments.append(department)

    def remove_department(self, department_name: str) -> None:
        """
        Удаляет отдел по названию

        Args:
            department_name: Название отдела для удаления

        ValueError: Если отдел не найден
        """
        for i, dept in enumerate(self.__departments):
            if dept.name == department_name:
                del self.__departments[i]
                return

        raise DepartmentNotFoundError(f"Отдел с названием '{department_name}' не найден")

    def get_departments(self) -> List[Department]:
        """
        Возвращает список всех отделов

        Returns:
            Копию списка отделов
        """
        return self.__departments.copy()

    # управление проектами

    def add_project(self, project: Project) -> None:
        """
        Добавляет проект в компанию

        Args:
            project: Проект для добавления

        ValueError: Если проект уже есть в компании
        """
        if not isinstance(project, Project):
            raise InvalidDataError("Можно добавить только объект типа Project")

        # Проверка на id
        for proj in self.__projects:
            if proj.project_id == project.project_id:
                raise DuplicateIdError(f"Проект с ID {project.project_id} уже существует")

        self.__projects.append(project)

    def remove_project(self, project_id: int) -> None:
        """
        Удаляет проект по ID

        Args:
            project_id: ID проекта для удаления

        ValueError: Если проект не найден
        """
        for i, proj in enumerate(self.__projects):
            if proj.project_id == project_id:
                del self.__projects[i]
                return

        raise ProjectNotFoundError(f"Проект с ID {project_id} не найден")

    def get_projects(self) -> List[Project]:
        """
        Возвращает список всех проектов

        Returns:
            Копию списка проектов
        """
        return self.__projects.copy()

    # Общие методы

    def get_all_employees(self) -> List[AbstractEmployee]:
        """
        Получение всех сотрудников компании

        Returns:
            Список всех сотрудников всех отделов
        """
        all_employees = []
        for department in self.__departments:
            all_employees.extend(department.get_employees())
        return all_employees

    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """
        Поиск сотрудника по ID во всех отделах

        Args:
            employee_id: ID сотрудника для поиска

        Returns:
            Найденный сотрудник или None
        """
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise InvalidDataError("ID должен быть положительным целым числом")

        for department in self.__departments:
            employee = department.find_employee_by_id(employee_id)
            if employee:
                return employee
        return None

    def calculate_total_monthly_cost(self) -> float:
        """
        Расчет общих месячных зп

        Returns:
            Сумма зарплат всех сотрудников компании
        """
        total = 0.0
        for department in self.__departments:
            total += department.calculate_total_salary()
        return total

    def get_projects_by_status(self, status: str) -> List[Project]:
        """
        Фильтрация проектов по статусу

        Args:
            status: Статус для фильтрации

        Returns:
            Список проектов с указанным статусом
        """
        if status not in Project.VALID_STATUSES:
            raise InvalidStatusError(f"Статус должен быть одним из: {Project.VALID_STATUSES}")

        return [project for project in self.__projects if project.status == status]

    def get_company_info(self) -> str:
        """
        Полная информация о компании

        Returns:
            Строка с информацией
        """
        total_employees = sum(len(dept) for dept in self.__departments)
        total_projects = len(self.__projects)

        return (f"Компания: {self.__name}\n"
                f"Отделов: {len(self.__departments)}\n"
                f"Сотрудников: {total_employees}\n"
                f"Проектов: {total_projects}\n"
                f"Месячные затраты: {self.calculate_total_monthly_cost():.2f}")

    def __str__(self) -> str:
        """Строковое представление компании"""
        total_employees = sum(len(dept) for dept in self.__departments)
        return f"Компания: {self.__name} (Отделов: {len(self.__departments)}, Сотрудников: {total_employees})"

    def __len__(self) -> int:
        """Возвращает общее количество сотрудников"""
        return sum(len(dept) for dept in self.__departments)


    # связи
    def remove_department(self, department_name: str, force: bool = False) -> None:
        """
        Удаляет отдел по названию

        Args:
            department_name: Название отдела для удаления
            force: Принудительное удаление даже если в отделе есть сотрудники

        ValueError: Если отдел не найден
        RuntimeError: Если в отделе есть сотрудники и не установлен force=True
        """
        for i, dept in enumerate(self.__departments):
            if dept.name == department_name:
                # Проверка наличия сотрудников в отделе
                if dept.has_employees() and not force:
                    raise RuntimeError(
                        f"Нельзя удалить отдел '{department_name}', так как в нем есть сотрудники. "
                        f"Используйте force=True для принудительного удаления или перенесите сотрудников."
                    )
                del self.__departments[i]
                return

        raise DepartmentNotFoundError(f"Отдел с названием '{department_name}' не найден")

    def transfer_employee(self, employee_id: int, from_dept_name: str, to_dept_name: str) -> None:
        """
        Переносит сотрудника из одного отдела в другой

        Args:
            employee_id: ID сотрудника для переноса
            from_dept_name: Название отдела-источника
            to_dept_name: Название отдела-назначения

        ValueError: Если отделы не найдены или сотрудник не найден
        """
        # Поиск отделов
        from_dept = None
        to_dept = None

        for dept in self.__departments:
            if dept.name == from_dept_name:
                from_dept = dept
            if dept.name == to_dept_name:
                to_dept = dept

        if from_dept is None:
            raise DepartmentNotFoundError(f"Исходный отдел '{from_dept_name}' не найден")
        if to_dept is None:
            raise DepartmentNotFoundError(f"Целевой отдел '{to_dept_name}' не найден")

        # Поиск сотрудника в исходном отделе
        employee = from_dept.find_employee_by_id(employee_id)
        if employee is None:
            raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден в отделе '{from_dept_name}'")

        # Проверка, что сотрудник не участвует в проектах
        if self.__is_employee_in_projects(employee_id):
            raise RuntimeError(
                f"Сотрудник с ID {employee_id} участвует в проектах. "
                f"Сначала удалите его из всех проектов."
            )

        # Удаление из исходного отдела и добавление в целевой
        from_dept.remove_employee(employee_id)
        to_dept.add_employee(employee)

    def __is_employee_in_projects(self, employee_id: int) -> bool:
        """
        Проверяет, участвует ли сотрудник в каких-либо проектах

        Args:
            employee_id: ID сотрудника

        Returns:
            True если сотрудник участвует в проектах, иначе False
        """
        for project in self.__projects:
            for team_member in project.get_team():
                if team_member.id == employee_id:
                    return True
        return False

    #проверка связей
    def remove_employee(self, employee_id: int, force: bool = False) -> None:
        """
        Удаляет сотрудника из компании по ID

        Args:
            employee_id: ID сотрудника для удаления
            force: Принудительное удаление даже если сотрудник участвует в проектах

        ValueError: Если сотрудник не найден
        RuntimeError: Если сотрудник участвует в проектах и не установлен force=True
        """
        # Поиск отдела с сотрудником
        department_with_employee = None
        for dept in self.__departments:
            if dept.find_employee_by_id(employee_id) is not None:
                department_with_employee = dept
                break

        if department_with_employee is None:
            raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден в компании")

        # Проверка участия в проектах
        if self.__is_employee_in_projects(employee_id) and not force:
            raise RuntimeError(
                f"Нельзя удалить сотрудника с ID {employee_id}, так как он участвует в проектах. "
                f"Используйте force=True для принудительного удаления или сначала удалите его из проектов."
            )

        # Удаление сотрудника
        department_with_employee.remove_employee(employee_id)

    def remove_project(self, project_id: int, force: bool = False) -> None:
        """
        Удаляет проект по ID

        Args:
            project_id: ID проекта для удаления
            force: Принудительное удаление даже если в проекте есть команда

        ValueError: Если проект не найден
        RuntimeError: Если в проекте есть команда и не установлен force=True
        """
        for i, proj in enumerate(self.__projects):
            if proj.project_id == project_id:
                # Проверка наличия команды в проекте
                if proj.get_team_size() > 0 and not force:
                    raise RuntimeError(
                        f"Нельзя удалить проект с ID {project_id}, так как в нем есть команда. "
                        f"Используйте force=True для принудительного удаления или сначала удалите всех сотрудников из проекта."
                    )
                del self.__projects[i]
                return

        raise ProjectNotFoundError(f"Проект с ID {project_id} не найден")

    def get_employee_projects(self, employee_id: int) -> List[Project]:
        """
        Возвращает список проектов, в которых участвует сотрудник

        Args:
            employee_id: ID сотрудника

        Returns:
            Список проектов
        """
        projects = []
        for project in self.__projects:
            for team_member in project.get_team():
                if team_member.id == employee_id:
                    projects.append(project)
                    break
        return projects

    def remove_employee_from_all_projects(self, employee_id: int) -> None:
        """
        Удаляет сотрудника из всех проектов

        Args:
            employee_id: ID сотрудника

        EmployeeNotFoundError: Если сотрудник не найден в проектах
        """
        removed_from_projects = []

        for project in self.__projects:
            try:
                project.remove_team_member(employee_id)
                removed_from_projects.append(project.name)
            except EmployeeNotFoundError:
                pass

        if not removed_from_projects:
            raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден ни в одном проекте")
