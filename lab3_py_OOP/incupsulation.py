from abs import ABC, abstractmethod

class AbsrEmployee(ABC):
    @abstractmethod
    def calculate_salary(self) -> float:
        pass

    def get_info(self) -> str:
        pass


class Employee(AbsrEmployee):
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
        return f"{self.__str__()}, salary: {self.calculate_salary()}"

    class Manager(Employee):
        def __init__(self, id_empl, name, department, base_salary, bonus):
            super().__init__(self, id_empl, name, department, base_salary)
            self.__bonus = bonus

        @property
        def bonus(self):
            return self.__bonus

        @bonus.setter
        def bonus(self, value):
            if value < 0 or not isinstance(value, (int, float)):
                raise ValueError("Должно быть числом и не отрицательным")
            self.__bonus = value

        def calculate_salary(self) -> float:
            return self.base_salary + self.__bonus

        def get_info(self) -> str:
            return f"{super().__str__()}, Бонус: {self.__bonus}, Итоговая зарплата: {self.calculate_salary()}"


    class Developer(Employee):
        def __init__(self, id_empl, name, department, base_salary, teck_stack = None,seniority_level="junior"):
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

    # Тестирование
    if __name__ == "__main__":
        print("=== Тестирование иерархии классов ===")

        # Обычный сотрудник
        emp = Employee(1, "Иван Иванов", "Администрация", 40000.0)
        print("Обычный сотрудник:")
        print(emp.get_info())
        print()

        # Менеджер
        manager = Manager(2, "Анна Петрова", "Менеджмент", 60000.0, 15000.0)
        print("Менеджер:")
        print(manager.get_info())
        print()

        # Разработчик
        dev = Developer(3, "Пётр Сидоров", "IT", 50000.0, ["Python", "Django"], "middle")
        dev.add_skill("PostgreSQL")
        print("Разработчик:")
        print(dev.get_info())
        print()

        # Продавец
        sales = Salesperson(4, "Мария Козлова", "Продажи", 30000.0, 0.1, 50000.0)
        sales.update_sales(25000.0)
        print("Продавец:")
        print(sales.get_info())