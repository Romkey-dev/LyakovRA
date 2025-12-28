import json
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime


class Project:
    """проект компании"""

    VALID_STATUSES = {"planning", "active", "completed", "cancelled"}

    def __init__(self, project_id: int, name: str, description: str, deadline: datetime, status: str = "planning"):
        """
        Args:
            project_id: id проекта
            name: Название
            description: Описание
            deadline: Срок выполнения
            status:  planning, active, completed, cancelled

        ValueError: Если данные некорректны
        """
        self.__validate_project_id(project_id)
        self.__validate_name(name)
        self.__validate_description(description)
        self.__validate_deadline(deadline)
        self.__validate_status(status)

        self.__project_id = project_id
        self.__name = name
        self.__description = description
        self.__deadline = deadline
        self.__status = status
        self.__team: List[AbstractEmployee] = []

    def __validate_project_id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise InvalidDataError("ID проекта должен быть положительным целым числом")

    def __validate_name(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise InvalidDataError("Название проекта не должно быть пустой строкой")

    def __validate_description(self, value):
        if not isinstance(value, str):
            raise InvalidDataError("Описание проекта должно быть строкой")

    def __validate_deadline(self, value):
        if not isinstance(value, datetime):
            raise InvalidDataError("Срок должен быть объектом datetime")

    def __validate_status(self, value):
        if value not in self.VALID_STATUSES:
            raise InvalidStatusError(f"Статус должен быть одним из: {self.VALID_STATUSES}")

    @property
    def project_id(self) -> int:
        """Возвращает ID """
        return self.__project_id

    @property
    def name(self) -> str:
        """Возвращает название"""
        return self.__name

    @property
    def description(self) -> str:
        """Возвращает описание"""
        return self.__description

    @property
    def deadline(self) -> datetime:
        """Возвращает срок выполнения"""
        return self.__deadline

    @property
    def status(self) -> str:
        """Возвращает статус"""
        return self.__status

    def add_team_member(self, employee: AbstractEmployee) -> None:
        """
        Добавляет сотрудника

        Args:
            employee: Сотрудник для добавления

        ValueError: Если сотрудник уже в проекте или проект завершен/отменен
        """
        if not isinstance(employee, AbstractEmployee):
            raise InvalidDataError("Можно добавить только объект типа AbstractEmployee")

        if self.__status in {"completed", "cancelled"}:
            raise InvalidStatusError(f"Нельзя добавить сотрудника в проект со статусом '{self.__status}'")

        # Проверка если ли уже сотрудник
        for team_member in self.__team:
            if team_member.id == employee.id:
                raise DuplicateIdError(f"Сотрудник с ID {employee.id} уже в проекте")

        self.__team.append(employee)

    def remove_team_member(self, employee_id: int) -> None:
        """
        Удаляет сотрудника по ID

        Args:
            employee_id: ID сотрудника для удаления

        ValueError: Если сотрудник не найден
        """
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise InvalidDataError("ID должен быть положительным целым числом")

        for i, team_member in enumerate(self.__team):
            if team_member.id == employee_id:
                del self.__team[i]
                return

        raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден в проекте")

    def get_team(self) -> List[AbstractEmployee]:
        """
        Возвращает список команды
        """
        return self.__team.copy()

    def get_team_size(self) -> int:
        """
        Возвращает размер команды

        Returns:
            Количество сотрудников в проекте
        """
        return len(self.__team)

    def calculate_total_salary(self) -> float:
        """
        Расчет суммарной зарплаты команды

        Returns:
            Сумма зарплат
        """
        total = 0.0
        for employee in self.__team:
            total += employee.calculate_salary()
        return total

    def get_project_info(self) -> str:
        """
        Полная информация о проекте

        Returns:
            Строка с информацией
        """
        return (f"Проект #{self.__project_id}: {self.__name}\n"
                f"Описание: {self.__description}\n"
                f"Срок: {self.__deadline.strftime('%d.%m.%Y')}\n"
                f"Статус: {self.__status}\n"
                f"Команда: {len(self.__team)} сотрудников\n"
                f"Общая зарплата команды: {self.calculate_total_salary():.2f}")

    def change_status(self, new_status: str) -> None:
        """
        Изменение статуса

        Args:
            new_status: Новый статус проекта

        ValueError: Если статус некорректен
        """
        if new_status not in self.VALID_STATUSES:
            raise InvalidStatusError(f"Статус должен быть одним из: {self.VALID_STATUSES}")

        self.__status = new_status

    def __str__(self) -> str:
        """Строковое представление проекта"""
        return f"Проект: {self.__name} (Статус: {self.__status}, Команда: {len(self.__team)} чел.)"

    def __len__(self) -> int:
        """Возвращает размер команды"""
        return len(self.__team)

    def __contains__(self, employee: AbstractEmployee) -> bool:
        """Проверяет, есть ли сотрудник в проекте"""
        if not isinstance(employee, AbstractEmployee):
            return False

        for team_member in self.__team:
            if team_member == employee:
                return True
        return False

    # проверка команды
    def has_team(self) -> bool:
        """
        Проверяет, есть ли сотрудники в проекте

        Returns:
            True если есть сотрудники, иначе False
        """
        return len(self.__team) > 0

    def get_team_member_ids(self) -> List[int]:
        """
        Возвращает список ID всех сотрудников в проекте

        Returns:
            Список ID сотрудников
        """
        return [emp.id for emp in self.__team]
