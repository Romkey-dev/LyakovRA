import json
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime


class AbstractEmployee(ABC):
    @abstractmethod
    def calculate_salary(self) -> float:
        pass

    @abstractmethod
    def get_info(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Конвертирует объект в словарь """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> 'AbstractEmployee':
        """Создает объект из словаря"""
        pass

    # перезагрузка сотрудников
    def __eq__(self, other) -> bool:
        """ сотрудников по ID"""
        if not isinstance(other, AbstractEmployee):
            return False
        return self.id == other.id

    def __lt__(self, other) -> bool:
        """Сравнение по зп"""
        if not isinstance(other, AbstractEmployee):
            return NotImplemented
        return self.calculate_salary() < other.calculate_salary()

    def __add__(self, other) -> float:
        """Сложение двух сотрудников возвращает сумму их зарплат"""
        if isinstance(other, AbstractEmployee):
            return self.calculate_salary() + other.calculate_salary()
        elif isinstance(other, (int, float)):
            return self.calculate_salary() + other
        else:
            return NotImplemented

    def __radd__(self, other) -> float:
        """ суммирование в списке через sum()"""
        if isinstance(other, (int, float)):
            return other + self.calculate_salary()
        return NotImplemented


class Employee(AbstractEmployee):
    def __init__(self, id_empl, name, department, base_salary):
        self.__validate_id(id_empl)
        self.__validate_name(name)
        self.__validate_department(department)
        self.__validate_salary(base_salary)

        self.__id = id_empl
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary

    def __validate_id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise InvalidDataError("ID должен быть положительным целым числом")

    def __validate_name(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise InvalidDataError("Имя не должно быть пустой строкой")

    def __validate_department(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise InvalidDataError("Отдел не должен быть пустой строкой")

    def __validate_salary(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise FinancialValidationError("Зарплата должна быть положительным числом")

    def get_all(self):
        return (self.__id, self.__name, self.__department, self.__base_salary)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__validate_id(value)
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__validate_name(value)
        self.__name = value

    @property
    def department(self):
        return self.__department

    @department.setter
    def department(self, value):
        self.__validate_department(value)
        self.__department = value

    @property
    def base_salary(self):
        return self.__base_salary

    @base_salary.setter
    def base_salary(self, value):
        self.__validate_salary(value)
        self.__base_salary = value

    def __str__(self):
        return f"Сотрудник [id: {self.__id}, имя: {self.__name}, отдел: {self.__department}, базовая зарплата: {self.__base_salary}]"

    def calculate_salary(self) -> float:
        return self.__base_salary

    def get_info(self) -> str:
        return f"{self.__str__()}, Рассчитанная зарплата: {self.calculate_salary()}"

    def to_dict(self) -> dict:
        """Конвертирует сотрудника в словарь"""
        return {
            'type': self.__class__.__name__,
            'id': self.__id,
            'name': self.__name,
            'department': self.__department,
            'base_salary': self.__base_salary
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Employee':
        """Создает сотрудника из словаря"""
        required_fields = ['id', 'name', 'department', 'base_salary']
        for field in required_fields:
            if field not in data:
                raise InvalidDataError(f"Отсутствует обязательное поле: {field}")

        return cls(
            id_empl=data['id'],
            name=data['name'],
            department=data['department'],
            base_salary=data['base_salary']
        )


class Manager(Employee):
    def __init__(self, id_empl, name, department, base_salary, bonus):
        super().__init__(id_empl, name, department, base_salary)
        self.__validate_bonus(bonus)
        self.__bonus = bonus

    def __validate_bonus(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise FinancialValidationError("Бонус должен быть неотрицательным числом")

    @property
    def bonus(self):
        return self.__bonus

    @bonus.setter
    def bonus(self, value):
        self.__validate_bonus(value)
        self.__bonus = value

    def calculate_salary(self) -> float:
        return self.base_salary + self.__bonus

    def get_info(self) -> str:
        return f"{super().__str__()}, Бонус: {self.__bonus}, Итоговая зарплата: {self.calculate_salary()}"

    def to_dict(self) -> dict:
        """Конвертирует менеджера в словарь"""
        data = super().to_dict()
        data['bonus'] = self.__bonus
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Manager':
        """Создает менеджера из словаря"""
        if 'bonus' not in data:
            raise InvalidDataError("Отсутствует обязательное поле: bonus")

        return cls(
            id_empl=data['id'],
            name=data['name'],
            department=data['department'],
            base_salary=data['base_salary'],
            bonus=data['bonus']
        )


class Developer(Employee):
    def __init__(self, id_empl, name, department, base_salary, tech_stack=None, seniority_level="junior"):
        super().__init__(id_empl, name, department, base_salary)
        self.__validate_tech_stack(tech_stack)
        self.__validate_seniority_level(seniority_level)
        self.__tech_stack = tech_stack if tech_stack is not None else []
        self.__seniority_level = seniority_level

    def __validate_tech_stack(self, value):
        if value is not None and not isinstance(value, list):
            raise InvalidDataError("tech_stack должен быть списком")

    def __validate_seniority_level(self, value):
        valid_levels = ["junior", "middle", "senior"]
        if value not in valid_levels:
            raise InvalidDataError(f"Уровень должен быть одним из: {valid_levels}")

    @property
    def tech_stack(self):
        return self.__tech_stack.copy()

    @property
    def seniority_level(self):
        return self.__seniority_level

    @seniority_level.setter
    def seniority_level(self, value):
        self.__validate_seniority_level(value)
        self.__seniority_level = value

    def calculate_salary(self) -> float:
        coefficients = {
            "junior": 1.0,
            "middle": 1.5,
            "senior": 2.0
        }
        return self.base_salary * coefficients[self.__seniority_level]

    def add_skill(self, new_skill: str) -> None:
        if not isinstance(new_skill, str) or new_skill.strip() == "":
            raise InvalidDataError("Навык не должен быть пустой строкой")
        if new_skill not in self.__tech_stack:
            self.__tech_stack.append(new_skill)

    def get_info(self) -> str:
        return f"{super().__str__()}, Уровень: {self.__seniority_level}, Технологии: {', '.join(self.__tech_stack)}, Итоговая зарплата: {self.calculate_salary()}"

    def to_dict(self) -> dict:
        """Конвертирует разработчика в словарь"""
        data = super().to_dict()
        data.update({
            'tech_stack': self.__tech_stack,
            'seniority_level': self.__seniority_level
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Developer':
        """Создает разработчика из словаря"""
        tech_stack = data.get('tech_stack', [])
        seniority_level = data.get('seniority_level', 'junior')

        return cls(
            id_empl=data['id'],
            name=data['name'],
            department=data['department'],
            base_salary=data['base_salary'],
            tech_stack=tech_stack,
            seniority_level=seniority_level
        )


class Salesperson(Employee):
    def __init__(self, id_empl, name, department, base_salary, commission_rate, sales_volume=0.0):
        super().__init__(id_empl, name, department, base_salary)
        self.__validate_commission_rate(commission_rate)
        self.__validate_sales_volume(sales_volume)
        self.__commission_rate = commission_rate
        self.__sales_volume = sales_volume

    def __validate_commission_rate(self, value):
        if not isinstance(value, (int, float)) or value < 0 or value > 1:
            raise FinancialValidationError("Процент комиссии должен быть между 0 и 1")

    def __validate_sales_volume(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise FinancialValidationError("Объем продаж должен быть неотрицательным числом")

    @property
    def commission_rate(self):
        return self.__commission_rate

    @commission_rate.setter
    def commission_rate(self, value):
        self.__validate_commission_rate(value)
        self.__commission_rate = value

    @property
    def sales_volume(self):
        return self.__sales_volume

    def calculate_salary(self) -> float:
        return self.base_salary + (self.__sales_volume * self.__commission_rate)

    def update_sales(self, new_sales: float) -> None:
        if not isinstance(new_sales, (int, float)) or new_sales < 0:
            raise FinancialValidationError("Объем продаж должен быть неотрицательным числом")
        self.__sales_volume += new_sales

    def get_info(self) -> str:
        return f"{super().__str__()}, Комиссия: {self.__commission_rate:.1%}, Объем продаж: {self.__sales_volume}, Итоговая зарплата: {self.calculate_salary()}"

    def to_dict(self) -> dict:
        """Конвертирует продавца в словарь"""
        data = super().to_dict()
        data.update({
            'commission_rate': self.__commission_rate,
            'sales_volume': self.__sales_volume
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Salesperson':
        """Создает продавца из словаря"""
        if 'commission_rate' not in data:
            raise InvalidDataError("Отсутствует обязательное поле: commission_rate")

        sales_volume = data.get('sales_volume', 0.0)

        return cls(
            id_empl=data['id'],
            name=data['name'],
            department=data['department'],
            base_salary=data['base_salary'],
            commission_rate=data['commission_rate'],
            sales_volume=sales_volume
        )


class EmployeeFactory:
    """класс для создания объектов сотрудников разных типов"""

    _employee_classes = {
        'employee': Employee,
        'manager': Manager,
        'developer': Developer,
        'salesperson': Salesperson
    }

    _required_params = {
        'employee': ['id_empl', 'name', 'department', 'base_salary'],
        'manager': ['id_empl', 'name', 'department', 'base_salary', 'bonus'],
        'developer': ['id_empl', 'name', 'department', 'base_salary'],
        'salesperson': ['id_empl', 'name', 'department', 'base_salary', 'commission_rate']
    }

    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        """
        Создает и возвращает объект сотрудника

        Args:
            emp_type: Тип сотрудника ("employee", "manager", "developer", "salesperson")
            **kwargs: Аргументы для конструктора

        Returns:
             сотрудник заданного типа

        ValueError: Если передан неизвестный тип сотрудника или недостаточно аргументов
        """
        emp_type = emp_type.lower()

        if emp_type not in EmployeeFactory._employee_classes:
            available = ', '.join(EmployeeFactory._employee_classes.keys())
            raise InvalidDataError(f"Неизвестный тип сотрудника: {emp_type}. "
                                   f"Доступные типы: {available}")
        required = EmployeeFactory._required_params[emp_type]
        missing = [param for param in required if param not in kwargs]
        if missing:
            raise InvalidDataError(f"Не хватает обязательных параметров: {missing}")

        employee_class = EmployeeFactory._employee_classes[emp_type]
        return employee_class(**kwargs)

    @staticmethod
    def from_dict(data: dict) -> AbstractEmployee:
        """
        Создает сотрудника из словаря

        Args:
            data: Словарь с данными сотрудника

        Returns:
            Объект сотрудника соответствующего типа

        ValueError: Если тип сотрудника неизвестен или данные некорректны
        """
        if 'type' not in data:
            raise InvalidDataError("Словарь должен содержать поле 'type'")

        emp_type = data['type'].lower()

        if emp_type == 'employee':
            return Employee.from_dict(data)
        elif emp_type == 'manager':
            return Manager.from_dict(data)
        elif emp_type == 'developer':
            return Developer.from_dict(data)
        elif emp_type == 'salesperson':
            return Salesperson.from_dict(data)
        else:
            raise InvalidDataError(f"Неизвестный тип сотрудника: {emp_type}")


class Department:
    """Класс для отделов компании"""

    def __init__(self, name: str):
        """
        Args:
            name: Название отдела
        """
        if not isinstance(name, str) or name.strip() == "":
            raise InvalidDataError("Название отдела не должно быть пустой строкой")
        self.__name = name
        self.__employees: List[AbstractEmployee] = []

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        """Устанавливает название отдела"""
        if not isinstance(value, str) or value.strip() == "":
            raise InvalidDataError("Название отдела не должно быть пустой строкой")
        self.__name = value

    def add_employee(self, employee: AbstractEmployee) -> None:
        """
        Добавляет сотрудника

        Args:
            employee: Объект сотрудника для добавления

        ValueError: Если сотрудник уже есть в отделе
        """
        if not isinstance(employee, AbstractEmployee):
            raise InvalidDataError("Можно добавить только объект типа AbstractEmployee")

        # Проверка уникальности ID
        for emp in self.__employees:
            if emp.id == employee.id:
                raise DuplicateIdError(f"Сотрудник с ID {employee.id} уже есть в отделе")

        self.__employees.append(employee)

    def remove_employee(self, employee_id: int) -> None:
        """
        Удаляет сотрудника по ID

        Args:
            employee_id: ID сотрудника для удаления

        ValueError: Если сотрудник с таким ID не найден
        """
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise InvalidDataError("ID должен быть положительным целым числом")

        for i, emp in enumerate(self.__employees):
            if emp.id == employee_id:
                del self.__employees[i]
                return

        raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден в отделе")

    def get_employees(self) -> List[AbstractEmployee]:
        """
        Возвращает список всех сотрудников

        Returns:
            Копию списка сотрудников
        """
        return self.__employees.copy()

    def calculate_total_salary(self) -> float:
        """
        Вычисляет общую ЗП всех сотрудников

        Return:
            Сумма зарплат всех сотрудников
        """
        total = 0.0
        for employee in self.__employees:
            total += employee.calculate_salary()
        return total

    def get_employee_count(self) -> dict[str, int]:
        """
        Возвращает статистику по типам сотрудников

        Returns:
            Словарь {тип_сотрудника: количество}
        """
        counts = {
            "Employee": 0,
            "Manager": 0,
            "Developer": 0,
            "Salesperson": 0
        }

        for employee in self.__employees:
            class_name = employee.__class__.__name__
            if class_name in counts:
                counts[class_name] += 1
            else:
                counts[class_name] = 1

        # Удаляем нулевые знач
        return {k: v for k, v in counts.items() if v > 0}

    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """
        Ищет сотрудника по ID

        Args:
            employee_id: ID сотрудника для поиска

        Returns:
            Найденный сотрудник или None, если не найден
        """
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise InvalidDataError("ID должен быть положительным целым числом")

        for employee in self.__employees:
            if employee.id == employee_id:
                return employee

        return None

    def to_dict(self) -> dict:
        """Конвертирует отдел в словарь"""
        return {
            'name': self.__name,
            'employees': [emp.to_dict() for emp in self.__employees]
        }

    def save_to_file(self, filename: str) -> None:
        """
        Сохраняет всех сотрудников отдела в JSON файл.

        Args:
            filename: Имя файла для сохранения
:
        Error: Если не удалось сохранить файл
        """
        try:
            data = self.to_dict()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except (IOError, OSError) as e:
            raise IOError(f"Не удалось сохранить файл {filename}: {e}")

    @classmethod
    def load_from_file(cls, filename: str) -> 'Department':
        """
        Загружает отдел из JSON

        Args:
            filename: Имя файла для загрузки

        Returns:
            Загруженный отдел

        Error: Если не удалось загрузить файл
        ValueError: Если данные в файле некорректны
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (IOError, OSError, json.JSONDecodeError) as e:
            raise IOError(f"Не удалось загрузить файл {filename}: {e}")

        if 'name' not in data:
            raise InvalidDataError("Файл должен содержать поле 'name'")
        if 'employees' not in data:
            raise InvalidDataError("Файл должен содержать поле 'employees'")

        department = cls(data['name'])

        for emp_data in data['employees']:
            try:
                employee = EmployeeFactory.from_dict(emp_data)
                department.add_employee(employee)
            except (InvalidDataError, DuplicateIdError) as e:
                print(f"Предупреждение: не удалось загрузить сотрудника: {e}")
                continue

        return department

    # Перегрузка операторов
    def __len__(self) -> int:
        """Возвращает количество сотрудников в отделе"""
        return len(self.__employees)

    def __getitem__(self, key) -> AbstractEmployee:
        """
        Доступ к сотруднику по индексу

        Args:
            key: Индекс сотрудника или срез

        Returns:
            Сотрудник или список сотрудников

        IndError: Если индекс вне диапазона
        TypeError: Если ключ не int или slice
        """
        if isinstance(key, int):
            if key < 0:
                key = len(self.__employees) + key
            if 0 <= key < len(self.__employees):
                return self.__employees[key]
            raise IndexError(f"Индекс {key} вне диапазона [0, {len(self.__employees) - 1}]")
        elif isinstance(key, slice):
            return self.__employees[key]
        else:
            raise TypeError(f"Индекс должен быть int или slice, а не {type(key).__name__}")

    def __contains__(self, employee: AbstractEmployee) -> bool:
        """
        Проверка принадлежности сотрудника отделу

        Args:
            employee: Сотрудник для проверки

        Returns:
            True если сотрудник в отделе, иначе False
        """
        if not isinstance(employee, AbstractEmployee):
            return False

        for emp in self.__employees:
            if emp == employee:
                return True
        return False

    def __str__(self) -> str:
        """Строковое представление отдела"""
        return f"Отдел: {self.__name}, Сотрудников: {len(self)}"

    def __iter__(self):
        """Итератор по сотрудникам отдела"""
        return iter(self.__employees)

    def __repr__(self) -> str:
        """Официальное строковое представление"""
        return f"Department(name='{self.__name}', employees={len(self.__employees)})"

    # связи
    def has_employees(self) -> bool:
        """
        Проверяет, есть ли сотрудники в отделе

        Returns:
            True если есть сотрудники, иначе False
        """
        return len(self.__employees) > 0

    def get_employee_ids(self) -> List[int]:
        """
        Возвращает список ID всех сотрудников отдела

        Returns:
            Список ID сотрудников
        """
        return [emp.id for emp in self.__employees]


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


# ИСКЛЮЧЕНИЯ
class EmployeeNotFoundError(Exception):
    """сотрудник не найден"""
    pass

class DepartmentNotFoundError(Exception):
    """отдел не найден"""
    pass

class ProjectNotFoundError(Exception):
    """проект не найден"""
    pass

class InvalidStatusError(Exception):
    """неверный статус"""
    pass

class DuplicateIdError(Exception):
    """ дублирование ID"""
    pass

class InvalidDataError(Exception):
    """неверные данные"""
    pass

class FinancialValidationError(Exception):
    """ошибка валидации финансовых показателей"""
    pass


# тест
if __name__ == "__main__":
    print("=== ДЕМОНСТРАЦИЯ ===")

    try:
        print("\n1. Отчёт")

        # Создание компании
        company = Company("TechInnovations")

        # Создание сотрудников разных типов
        manager = Manager(1, "Alice Johnson", "DEV", 7000, 2000)
        developer = Developer(2, "Bob Smith", "DEV", 5000, ["Python", "SQL"], "senior")
        salesperson = Salesperson(3, "Charlie Brown", "SAL", 4000, 0.15, 50000)

        # Создание отделов
        dev_department = Department("Development")
        sales_department = Department("Sales")

        # Добавление отделов в компанию
        company.add_department(dev_department)
        company.add_department(sales_department)

        # Добавление сотрудников в отделы
        dev_department.add_employee(manager)
        dev_department.add_employee(developer)
        sales_department.add_employee(salesperson)

        print(f"   Компания создана: {company}")
        print(f"   Отделы: {[dept.name for dept in company.get_departments()]}")
        print(f"   Сотрудников: {len(company)}")
        print(f"   - Manager: {manager.name}, зарплата: {manager.calculate_salary():.2f}")
        print(f"   - Developer: {developer.name}, зарплата: {developer.calculate_salary():.2f}")
        print(f"   - Salesperson: {salesperson.name}, зарплата: {salesperson.calculate_salary():.2f}")

        # Создание проектов
        ai_project = Project(101, "AI Platform", "Разработка AI системы", datetime(2024, 12, 31), "active")
        web_project = Project(102, "Web Portal", "Создание веб-портала", datetime(2024, 9, 30), "planning")

        # Добавление проектов в компанию
        company.add_project(ai_project)
        company.add_project(web_project)

        # Формирование команд проектов
        ai_project.add_team_member(developer)
        ai_project.add_team_member(manager)
        web_project.add_team_member(developer)

        print(f"\n   Проектов создано: {len(company.get_projects())}")
        print(f"   - AI Platform: {ai_project.get_team_size()} участников")
        print(f"   - Web Portal: {web_project.get_team_size()} участников")


        print("\n2. РАБОТА С КОМПОЗИЦИЕЙ И АГРЕГАЦИЕЙ")

        #  разница в жизненном цикле объектов
        print("   Жизненный цикл объектов:")
        print(f"   - Сотрудник {developer.name} принадлежит отделу Development: {developer in dev_department}")
        print(f"   - Сотрудник {developer.name} работает над проектом AI Platform: {developer in ai_project}")
        print(f"   - Сотрудник {manager.name} работает над проектом AI Platform: {manager in ai_project}")

        #  управления связями
        print("\n   Управление связями:")
        print("   Создаем нового сотрудника для демонстрации переноса")
        test_employee = Employee(4, "Test Employee", "SAL", 3500)
        sales_department.add_employee(test_employee)
        print(f"   Добавлен {test_employee.name} в отдел Sales")

        # Пробуем перенести должно вызвать ошибку
        print("   Пробуем перенести сотрудника между отделами")
        try:
            company.transfer_employee(4, "Sales", "Development")
            print(f"   {test_employee.name} успешно перенесен в Development")
        except Exception as e:
            print(f"   Ошибка переноса: {e}")


        print("\n3. ВАЛИДАЦИЯ И ОБРАБОТКА ОШИБОК")


        print("   Попытка добавить дубликат ID:")
        try:
            dev_department.add_employee(Employee(1, "Duplicate Employee", "DEV", 3000))
            print("   Ошибка: должен был быть выброшен DuplicateIdError!")
        except DuplicateIdError as e:
            print(f"   *** Ожидаемая ошибка: {e}")
        except Exception as e:
            print(f"   Неожиданная ошибка: {type(e).__name__}: {e}")


        print("\n   Попытка невалидного изменения статуса:")
        try:
            ai_project.change_status("неправильный_статус")
            print("   Ошибка: должен был быть выброшен InvalidStatusError!")
        except InvalidStatusError as e:
            print(f"   *** Ожидаемая ошибка: {e}")
        except Exception as e:
            print(f"   Неожиданная ошибка: {type(e).__name__}: {e}")

        print("\n   Попытка удаления занятого отдела:")
        try:
            company.remove_department("Development")
            print("   Ошибка: должен был быть выброшен RuntimeError!")
        except RuntimeError as e:
            print(f"   *** Ожидаемая ошибка: {e}")
        except Exception as e:
            print(f"   Неожиданная ошибка: {type(e).__name__}: {e}")


        print("\n4. СЕРИАЛИЗАЦИЯ И ЭКСПОРТ")


        print("   Сохранение данных в JSON:")
        dev_department.save_to_file("development_department.json")
        print("   *** Отдел Development сохранен в development_department.json")

 
        print("   Загрузка данных из JSON:")
        loaded_department = Department.load_from_file("development_department.json")
        print(f"   *** Отдел загружен: {loaded_department.name}, сотрудников: {len(loaded_department)}")


        print("\n5. АНАЛИЗ ДАННЫХ")


        print("   Статистика по компании:")
        print(f"   {company.get_company_info()}")


        print("\n   Финансовые показатели:")
        total_cost = company.calculate_total_monthly_cost()
        print(f"   Общие месячные затраты: {total_cost:.2f}")


        print("\n   Затраты по отделам:")
        for dept in company.get_departments():
            dept_cost = dept.calculate_total_salary()
            percentage = (dept_cost / total_cost * 100) if total_cost > 0 else 0
            print(f"   - {dept.name}: {dept_cost:.2f} ({percentage:.1f}%)")


        print("\n   Статистика сотрудников Development:")
        dev_stats = dev_department.get_employee_count()
        for emp_type, count in dev_stats.items():
            print(f"   - {emp_type}: {count}")


        print("\n   Поиск сущностей:")


        found_employee = company.find_employee_by_id(2)
        if found_employee:
            print(f"   *** Найден сотрудник ID 2: {found_employee.name}")


        print("\n   Проекты по статусам:")
        for status in ["planning", "active", "completed", "cancelled"]:
            projects = company.get_projects_by_status(status)
            if projects:
                print(f"   - {status}: {len(projects)} проект(ов)")

        
        # Перегрузка
        print("\n   Перегрузка операторов:")
        if len(dev_department) >= 2:
            emp1 = dev_department[0]
            emp2 = dev_department[1]
            print(f"   - Сравнение: {emp1.name} < {emp2.name} = {emp1 < emp2}")
            print(f"   - Сумма зарплат: {emp1.name} + {emp2.name} = {emp1 + emp2:.2f}")
            print(f"   - Сумма всех зарплат отдела: {sum(dev_department):.2f}")

        print("\n=== конец ===")


    except Exception as e:
        print(f"\n!!! ПРОИЗОШЛА ОШИБКА: {type(e).__name__}: {e}")
        print("Демонстрация прервана.")
