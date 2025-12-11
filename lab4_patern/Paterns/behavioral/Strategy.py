from abc import ABC, abstractmethod

class BonusStrategy(ABC):
    """Стратегия расчета бонуса"""
    
    @abstractmethod
    def calculate_bonus(self, employee) -> float:
        pass


class PerformanceBonusStrategy(BonusStrategy):
    """Бонус на основе производительности"""
    
    def calculate_bonus(self, employee) -> float:
        # 10%
        return employee.base_salary * 0.10


class SeniorityBonusStrategy(BonusStrategy):
    """Бонус на основе стажа/уровня"""
    
    def calculate_bonus(self, employee) -> float:
        if hasattr(employee, 'seniority_level'):
            levels = {"junior": 0.05, "middle": 0.10, "senior": 0.20}
            return employee.base_salary * levels.get(employee.seniority_level, 0)
        return 0


class EmployeeWithStrategy:
    """Сотрудник с поддержкой стратегии бонусов"""
    
    def __init__(self, employee, bonus_strategy: BonusStrategy = None):
        self.employee = employee
        self.bonus_strategy = bonus_strategy
    
    def set_bonus_strategy(self, strategy: BonusStrategy):
        self.bonus_strategy = strategy
    
    def calculate_total_salary(self) -> float:
        base = self.employee.calculate_salary()
        if self.bonus_strategy:
            return base + self.bonus_strategy.calculate_bonus(self.employee)
        return base
