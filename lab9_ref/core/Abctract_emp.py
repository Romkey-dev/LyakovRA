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
