import json
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


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
        self.__id = id_empl
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary

    def get_all(self):
        return (self.__id, self.__name, self.__department, self.__base_salary)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID должен быть положительным целым числом")
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Имя не должно быть пустой строкой")
        self.__name = value

    @property
    def department(self):
        return self.__department

    @department.setter
    def department(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Отдел не должен быть пустой строкой")
        self.__department = value

    @property
    def base_salary(self):
        return self.__base_salary

    @base_salary.setter
    def base_salary(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Зарплата должна быть положительным числом")
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
                raise ValueError(f"Отсутствует обязательное поле: {field}")

        return cls(
            id_empl=data['id'],
            name=data['name'],
            department=data['department'],
            base_salary=data['base_salary']
        )


class Manager(Employee):
    def __init__(self, id_empl, name, department, base_salary, bonus):
        super().__init__(id_empl, name, department, base_salary)
        self.__bonus = bonus

    @property
    def bonus(self):
        return self.__bonus

    @bonus.setter
    def bonus(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Бонус должен быть неотрицательным числом")
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
            raise ValueError("Отсутствует обязательное поле: bonus")

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
        self.__tech_stack = tech_stack if tech_stack is not None else []
        self.__seniority_level = seniority_level

    @property
    def tech_stack(self):
        return self.__tech_stack.copy()

    @property
    def seniority_level(self):
        return self.__seniority_level

    @seniority_level.setter
    def seniority_level(self, value):
        valid_levels = ["junior", "middle", "senior"]
        if value not in valid_levels:
            raise ValueError(f"Уровень должен быть одним из: {valid_levels}")
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
            raise ValueError("Навык не должен быть пустой строкой")
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
        self.__commission_rate = commission_rate
        self.__sales_volume = sales_volume

    @property
    def commission_rate(self):
        return self.__commission_rate

    @commission_rate.setter
    def commission_rate(self, value):
        if not isinstance(value, (int, float)) or value < 0 or value > 1:
            raise ValueError("Процент комиссии должен быть между 0 и 1")
        self.__commission_rate = value

    @property
    def sales_volume(self):
        return self.__sales_volume

    def calculate_salary(self) -> float:
        return self.base_salary + (self.__sales_volume * self.__commission_rate)

    def update_sales(self, new_sales: float) -> None:
        if not isinstance(new_sales, (int, float)) or new_sales < 0:
            raise ValueError("Объем продаж должен быть неотрицательным числом")
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
            raise ValueError("Отсутствует обязательное поле: commission_rate")

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
            raise ValueError(f"Неизвестный тип сотрудника: {emp_type}. "
                             f"Доступные типы: {available}")
        required = EmployeeFactory._required_params[emp_type]
        missing = [param for param in required if param not in kwargs]
        if missing:
            raise ValueError(f"Не хватает обязательных параметров: {missing}")

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
            raise ValueError("Словарь должен содержать поле 'type'")

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
            raise ValueError(f"Неизвестный тип сотрудника: {emp_type}")


class Department:
    """Класс для отделов компании"""

    def __init__(self, name: str):
        """
        Args:
            name: Название отдела
        """
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Название отдела не должно быть пустой строкой")
        self.__name = name
        self.__employees: List[AbstractEmployee] = []

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        """Устанавливает название отдела"""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Название отдела не должно быть пустой строкой")
        self.__name = value

    def add_employee(self, employee: AbstractEmployee) -> None:
        """
        Добавляет сотрудника

        Args:
            employee: Объект сотрудника для добавления

        ValueError: Если сотрудник уже есть в отделе
        """
        if not isinstance(employee, AbstractEmployee):
            raise ValueError("Можно добавить только объект типа AbstractEmployee")

        for emp in self.__employees:
            if emp.id == employee.id:
                raise ValueError(f"Сотрудник с ID {employee.id} уже есть в отделе")

        self.__employees.append(employee)

    def remove_employee(self, employee_id: int) -> None:
        """
        Удаляет сотрудника по ID

        Args:
            employee_id: ID сотрудника для удаления

        ValueError: Если сотрудник с таким ID не найден
        """
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise ValueError("ID должен быть положительным целым числом")

        for i, emp in enumerate(self.__employees):
            if emp.id == employee_id:
                del self.__employees[i]
                return

        raise ValueError(f"Сотрудник с ID {employee_id} не найден в отделе")

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
            raise ValueError("ID должен быть положительным целым числом")

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
            raise ValueError("Файл должен содержать поле 'name'")
        if 'employees' not in data:
            raise ValueError("Файл должен содержать поле 'employees'")

        department = cls(data['name'])

        for emp_data in data['employees']:
            try:
                employee = EmployeeFactory.from_dict(emp_data)
                department.add_employee(employee)
            except (ValueError, KeyError) as e:
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


# тест
if __name__ == "__main__":
    print("=== ДЕМОНСТРАЦИЯ ===")

    # 1. Создание отдела и добавление сотрудников
    dept = Department("IT отдел")
    dept.add_employee(Employee(1, "Иван", "ИТ", 40000))
    dept.add_employee(Manager(2, "Анна", "Упр", 60000, 15000))
    dept.add_employee(Developer(3, "Пётр", "Разр", 50000, ["Python", "Django"], "senior"))
    dept.add_employee(Salesperson(4, "Мария", "Прод", 30000, 0.1, 50000))
    print(f"1. Создан отдел: {dept}")

    # 2. Общая зп
    print(f"2. Общая зарплата: {dept.calculate_total_salary():.2f}")

    # 3. Перегруженные операторы
    emp1, emp2 = dept[0], dept[1]
    print(f"3.1 emp1 == emp2: {emp1 == emp2}")
    print(f"3.2 emp1 < emp2: {emp1 < emp2}")
    print(f"3.3 emp1 + emp2: {emp1 + emp2:.2f}")
    print(f"3.4 sum(dept): {sum(dept):.2f}")
    print(f"3.5 emp1 in dept: {emp1 in dept}")
    print(f"3.6 dept[2]: {dept[2].name}")

    # 4. Итерация
    print("4.1 Итерация по отделу:")
    for emp in dept:
        print(f"   - {emp.name}: {emp.calculate_salary():.2f}")

    dev = dept[2]
    if isinstance(dev, Developer):
        print("4.2 Стек технологий разработчика:")
        for tech in dev.tech_stack:
            print(f"   - {tech}")

    # 5. Сериализация
    dept.save_to_file("it_department.json")
    loaded = Department.load_from_file("it_department.json")
    print(f"5. Загружен отдел: {loaded.name}")

    # 6. Сортировка
    print("6.1 По зарплате (по убыванию):")
    for emp in sorted(dept, reverse=True):
        print(f"   {emp.name}: {emp.calculate_salary():.2f}")

    print("6.2 По имени:")
    for emp in sorted(dept, key=lambda x: x.name):
        print(f"   {emp.name}")

    # 7. Поиск по ID
    found = dept.find_employee_by_id(3)
    print(f"7. Найден сотрудник с ID 3: {found.name if found else 'Не найден'}")