"""
OCP - Open/Closed Principle
Strategy Pattern для различных стратегий расчета бонусов
Открыто для расширения (добавления новых стратегий)
Закрыто для изменения (не нужно менять Manager)
"""

from abc import ABC, abstractmethod


class BonusStrategy(ABC):
    """Базовая стратегия расчета бонусов"""
    
    @abstractmethod
    def calculate(self, employee) -> float:
        """Рассчитать бонус для сотрудника
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            float: Размер бонуса
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Получить название стратегии"""
        pass


class FixedBonusStrategy(BonusStrategy):
    """Фиксированный бонус"""
    
    def __init__(self, bonus_amount: float):
        """
        Args:
            bonus_amount: Размер фиксированного бонуса
        """
        self.bonus_amount = bonus_amount
    
    def calculate(self, employee) -> float:
        """Возвращает фиксированный бонус"""
        return self.bonus_amount
    
    def get_name(self) -> str:
        return f"Фиксированный бонус ({self.bonus_amount})"


class PercentageBonusStrategy(BonusStrategy):
    """Бонус в процентах от базовой зарплаты"""
    
    def __init__(self, percentage: float):
        """
        Args:
            percentage: Процент от базовой зарплаты (0.1 = 10%)
        """
        if not (0 <= percentage <= 1):
            raise ValueError("Процент должен быть от 0 до 1")
        self.percentage = percentage
    
    def calculate(self, employee) -> float:
        """Возвращает процент от базовой зарплаты"""
        return employee.base_salary * self.percentage
    
    def get_name(self) -> str:
        return f"Процентный бонус ({self.percentage * 100}%)"


class SeniorityBonusStrategy(BonusStrategy):
    """Бонус в зависимости от уровня (junior/middle/senior)"""
    
    def __init__(self):
        self.multipliers = {
            "junior": 0.05,    # 5%
            "middle": 0.10,    # 10%
            "senior": 0.20,    # 20%
        }
    
    def calculate(self, employee) -> float:
        """Возвращает бонус в зависимости от уровня"""
        level = getattr(employee, 'level', 'junior')
        multiplier = self.multipliers.get(level, 0.05)
        return employee.base_salary * multiplier
    
    def get_name(self) -> str:
        return "Бонус по уровню (junior/middle/senior)"


class ProjectBonusStrategy(BonusStrategy):
    """Бонус за завершенные проекты"""
    
    def __init__(self, bonus_per_project: float = 5000):
        """
        Args:
            bonus_per_project: Бонус за один проект
        """
        self.bonus_per_project = bonus_per_project
    
    def calculate(self, employee) -> float:
        """Возвращает бонус за проекты"""
        # Количество завершенных проектов
        projects_count = getattr(employee, 'projects_count', 0)
        return projects_count * self.bonus_per_project
    
    def get_name(self) -> str:
        return f"Бонус за проекты ({self.bonus_per_project} за проект)"


class PerformanceBonusStrategy(BonusStrategy):
    """Бонус в зависимости от процента выполнения целей"""
    
    def __init__(self, base_bonus: float = 10000):
        """
        Args:
            base_bonus: Базовый размер бонуса
        """
        self.base_bonus = base_bonus
    
    def calculate(self, employee) -> float:
        """Возвращает бонус в зависимости от производительности"""
        # Процент выполнения целей (0-1)
        achievement = getattr(employee, 'achievement', 0.8)
        
        # Если цель выполнена более чем на 100%, получит дополнительный бонус
        if achievement >= 1.0:
            return self.base_bonus * (1 + (achievement - 1.0) * 0.5)
        elif achievement >= 0.5:
            return self.base_bonus * achievement
        else:
            return 0  # Нет бонуса если выполнено менее 50%
    
    def get_name(self) -> str:
        return f"Бонус по производительности (базовый {self.base_bonus})"


class CompositeBonusStrategy(BonusStrategy):
    """Комбинированная стратегия (сумма нескольких стратегий)"""
    
    def __init__(self, strategies: list):
        """
        Args:
            strategies: Список стратегий для суммирования
        """
        self.strategies = strategies
    
    def calculate(self, employee) -> float:
        """Суммирует результаты всех стратегий"""
        total = 0.0
        for strategy in self.strategies:
            total += strategy.calculate(employee)
        return total
    
    def get_name(self) -> str:
        names = [s.get_name() for s in self.strategies]
        return f"Комбинированный бонус: {' + '.join(names)}"


class NoBonusStrategy(BonusStrategy):
    """Стратегия без бонусов (для базовых сотрудников)"""
    
    def calculate(self, employee) -> float:
        """Возвращает 0"""
        return 0.0
    
    def get_name(self) -> str:
        return "Без бонусов"
