from abc import ABC, abstractmethod

class EmployeeDecorator(ABC):
    """Базовый декоратор для сотрудников"""
    
    def __init__(self, employee):
        self._employee = employee
    
    @abstractmethod
    def get_info(self) -> str:
        pass
    
    def __getattr__(self, name):
        # Делегируем вызовы к исходному сотруднику
        return getattr(self._employee, name)


class BonusDecorator(EmployeeDecorator):
    """Декоратор для добавления бонуса"""
    
    def __init__(self, employee, bonus_amount):
        super().__init__(employee)
        self.bonus_amount = bonus_amount
    
    def calculate_salary(self) -> float:
        return self._employee.calculate_salary() + self.bonus_amount
    
    def get_info(self) -> str:
        return f"{self._employee.get_info()} + Бонус: {self.bonus_amount}"


class TrainingDecorator(EmployeeDecorator):
    """Декоратор для отметки о прохождении обучения"""
    
    def __init__(self, employee, training_name):
        super().__init__(employee)
        self.training_name = training_name
    
    def get_info(self) -> str:
        return f"{self._employee.get_info()} | Обучение: {self.training_name}"
