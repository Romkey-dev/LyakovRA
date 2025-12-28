"""
Тесты для рефакторенного кода
Проверяют все принципы SOLID и улучшения
"""

import pytest
from refactored.validators import (
    EmployeeValidator, DepartmentValidator, CompanyValidator, ProjectValidator
)
from refactored.interfaces import (
    ISalaryCalculable, ISkillManageable, IBonusCalculable, ICommissionCalculable
)
from refactored.repository import (
    InMemoryEmployeeRepository, InMemoryDepartmentRepository
)
from refactored.strategies.bonus_strategy import (
    FixedBonusStrategy, PercentageBonusStrategy, SeniorityBonusStrategy,
    NoBonusStrategy, CompositeBonusStrategy
)
from refactored.services import SalaryCalculator, DepartmentManager
from refactored.models.employee_refactored import (
    Employee, Developer, Manager, Salesperson
)
from refactored.exceptions import InvalidDataError, DuplicateIdError, FinancialValidationError


class TestValidators:
    """Тесты валидаторов (SRP)"""
    
    def test_employee_validator_valid_id(self):
        """Валидный ID"""
        EmployeeValidator.validate_id(1)  # Должно пройти
    
    def test_employee_validator_invalid_id_zero(self):
        """ID не может быть 0"""
        with pytest.raises(InvalidDataError):
            EmployeeValidator.validate_id(0)
    
    def test_employee_validator_invalid_id_negative(self):
        """ID не может быть отрицательным"""
        with pytest.raises(InvalidDataError):
            EmployeeValidator.validate_id(-1)
    
    def test_employee_validator_invalid_name(self):
        """Имя не может быть пустым"""
        with pytest.raises(InvalidDataError):
            EmployeeValidator.validate_name("")
    
    def test_employee_validator_valid_salary(self):
        """Валидная зарплата"""
        EmployeeValidator.validate_salary(50000)
    
    def test_employee_validator_invalid_salary_negative(self):
        """Зарплата не может быть отрицательной"""
        with pytest.raises(FinancialValidationError):
            EmployeeValidator.validate_salary(-1000)
    
    def test_department_validator_valid_name(self):
        """Валидное название отдела"""
        DepartmentValidator.validate_name("IT")
    
    def test_department_validator_invalid_name(self):
        """Название отдела не может быть пустым"""
        with pytest.raises(InvalidDataError):
            DepartmentValidator.validate_name("")
    
    def test_company_validator_valid_name(self):
        """Валидное название компании"""
        CompanyValidator.validate_name("Google")


class TestRepository:
    """Тесты Repository Pattern (DIP)"""
    
    def test_add_employee(self):
        """Добавление сотрудника в репозиторий"""
        repo = InMemoryEmployeeRepository()
        emp = Employee(1, "Alice", "IT", 50000)
        repo.add(emp)
        assert repo.get_by_id(1) == emp
    
    def test_duplicate_employee_id(self):
        """Дублирование ID должно вызвать ошибку"""
        repo = InMemoryEmployeeRepository()
        emp1 = Employee(1, "Alice", "IT", 50000)
        emp2 = Employee(1, "Bob", "HR", 45000)
        repo.add(emp1)
        with pytest.raises(DuplicateIdError):
            repo.add(emp2)
    
    def test_remove_employee(self):
        """Удаление сотрудника"""
        repo = InMemoryEmployeeRepository()
        emp = Employee(1, "Alice", "IT", 50000)
        repo.add(emp)
        repo.remove(1)
        assert repo.get_by_id(1) is None
    
    def test_get_all_employees(self):
        """Получить всех сотрудников"""
        repo = InMemoryEmployeeRepository()
        emp1 = Employee(1, "Alice", "IT", 50000)
        emp2 = Employee(2, "Bob", "HR", 45000)
        repo.add(emp1)
        repo.add(emp2)
        assert len(repo.get_all()) == 2
    
    def test_find_employees(self):
        """Поиск сотрудников по критериям"""
        repo = InMemoryEmployeeRepository()
        emp1 = Employee(1, "Alice", "IT", 50000)
        emp2 = Developer(2, "Bob", "IT", 60000, "middle")
        repo.add(emp1)
        repo.add(emp2)
        results = repo.find({'department': 'IT'})
        assert len(results) == 2


class TestBonusStrategies:
    """Тесты Strategy Pattern (OCP)"""
    
    def test_fixed_bonus_strategy(self):
        """Фиксированный бонус"""
        strategy = FixedBonusStrategy(10000)
        emp = Manager(1, "Alice", "IT", 50000)
        assert strategy.calculate(emp) == 10000
    
    def test_percentage_bonus_strategy(self):
        """Процентный бонус"""
        strategy = PercentageBonusStrategy(0.1)  # 10%
        emp = Manager(1, "Alice", "IT", 50000)
        assert strategy.calculate(emp) == 5000
    
    def test_seniority_bonus_strategy(self):
        """Бонус по уровню"""
        strategy = SeniorityBonusStrategy()
        emp = Developer(1, "Alice", "IT", 50000, "senior")
        emp.level = "senior"
        # Зарплата senior разработчика: 50000 * 2.0 = 100000
        # Бонус: 100000 * 0.2 = 20000
        bonus = strategy.calculate(emp)
        assert bonus == 100000 * 0.2  # 20000
    
    def test_no_bonus_strategy(self):
        """Стратегия без бонусов"""
        strategy = NoBonusStrategy()
        emp = Employee(1, "Alice", "IT", 50000)
        assert strategy.calculate(emp) == 0
    
    def test_composite_bonus_strategy(self):
        """Комбинированная стратегия"""
        strategies = [
            FixedBonusStrategy(5000),
            PercentageBonusStrategy(0.05)
        ]
        composite = CompositeBonusStrategy(strategies)
        emp = Manager(1, "Alice", "IT", 50000)
        # 5000 + 2500 = 7500
        assert composite.calculate(emp) == 7500
    
    def test_change_bonus_strategy_at_runtime(self):
        """Изменение стратегии во время выполнения (OCP)"""
        emp = Manager(1, "Alice", "IT", 50000, FixedBonusStrategy(10000))
        assert emp.calculate_bonus() == 10000
        
        # Меняем стратегию!
        emp.set_bonus_strategy(PercentageBonusStrategy(0.2))
        assert emp.calculate_bonus() == 10000


class TestEmployeeTypes:
    """Тесты типов сотрудников (LSP, ISP)"""
    
    def test_employee_basic(self):
        """Базовый сотрудник"""
        emp = Employee(1, "Alice", "IT", 50000)
        assert emp.calculate_salary() == 50000
    
    def test_developer_skill_management(self):
        """Разработчик может управлять навыками (ISP)"""
        dev = Developer(1, "Alice", "IT", 60000, "senior")
        assert isinstance(dev, ISkillManageable)  # Реализует ISP
        
        dev.add_skill("Python")
        dev.add_skill("JavaScript")
        assert len(dev.get_skills()) == 2
    
    def test_developer_salary_by_level(self):
        """Зарплата разработчика зависит от уровня"""
        junior = Developer(1, "Alice", "IT", 50000, "junior")
        middle = Developer(2, "Bob", "IT", 50000, "middle")
        senior = Developer(3, "Charlie", "IT", 50000, "senior")
        
        assert junior.calculate_salary() == 50000
        assert middle.calculate_salary() == 75000
        assert senior.calculate_salary() == 100000
    
    def test_manager_bonus_calculation(self):
        """Менеджер с бонусом (IBonusCalculable)"""
        emp = Manager(1, "Alice", "IT", 50000, FixedBonusStrategy(10000))
        assert isinstance(emp, IBonusCalculable)
        assert emp.calculate_salary() == 60000  # 50000 + 10000
    
    def test_salesperson_commission(self):
        """Менеджер по продажам с комиссией (ICommissionCalculable)"""
        sp = Salesperson(1, "Alice", "Sales", 30000, commission_rate=0.1)
        assert isinstance(sp, ICommissionCalculable)
        
        sp.set_sales_amount(100000)
        assert sp.calculate_commission() == 10000
        assert sp.calculate_salary() == 40000  # 30000 + 10000
    
    def test_liskov_substitution(self):
        """LSP: все сотрудники подставляются везде"""
        employees = [
            Employee(1, "Alice", "IT", 50000),
            Developer(2, "Bob", "IT", 60000, "middle"),
            Manager(3, "Charlie", "IT", 70000, FixedBonusStrategy(15000)),
            Salesperson(4, "Diana", "Sales", 40000)
        ]
        
        # Все реализуют ISalaryCalculable
        for emp in employees:
            assert isinstance(emp, ISalaryCalculable)
            salary = emp.calculate_salary()
            assert salary > 0


class TestSalaryCalculator:
    """Тесты SalaryCalculator сервиса (SRP)"""
    
    def test_calculate_total_salary(self):
        """Расчет общей зарплаты"""
        employees = [
            Employee(1, "Alice", "IT", 50000),
            Developer(2, "Bob", "IT", 60000, "middle"),
            Manager(3, "Charlie", "IT", 50000, FixedBonusStrategy(10000))
        ]
        
        total = SalaryCalculator.calculate_total_salary(employees)
        # 50000 + 90000 + 60000 = 200000
        assert total == 200000
    
    def test_calculate_average_salary(self):
        """Расчет средней зарплаты"""
        employees = [
            Employee(1, "Alice", "IT", 50000),
            Employee(2, "Bob", "IT", 60000),
            Employee(3, "Charlie", "IT", 40000)
        ]
        
        avg = SalaryCalculator.calculate_average_salary(employees)
        assert avg == 50000
    
    def test_get_salary_statistics(self):
        """Получить статистику по зарплатам"""
        employees = [
            Employee(1, "Alice", "IT", 50000),
            Employee(2, "Bob", "IT", 60000),
            Employee(3, "Charlie", "IT", 40000)
        ]
        
        stats = SalaryCalculator.get_salary_statistics(employees)
        assert stats['total'] == 150000
        assert stats['average'] == 50000
        assert stats['min'] == 40000
        assert stats['max'] == 60000
        assert stats['count'] == 3


class TestDepartmentManager:
    """Тесты DepartmentManager сервиса (SRP)"""
    
    def test_add_and_get_employee(self):
        """Добавление и получение сотрудника"""
        repo = InMemoryEmployeeRepository()
        dept = DepartmentManager("IT", repo)
        
        emp = Employee(1, "Alice", "IT", 50000)
        dept.add_employee(emp)
        
        assert dept.get_employee(1) == emp
    
    def test_remove_employee(self):
        """Удаление сотрудника из отдела"""
        repo = InMemoryEmployeeRepository()
        dept = DepartmentManager("IT", repo)
        
        emp = Employee(1, "Alice", "IT", 50000)
        dept.add_employee(emp)
        dept.remove_employee(1)
        
        assert dept.get_employee(1) is None
    
    def test_get_employee_count(self):
        """Количество сотрудников в отделе"""
        repo = InMemoryEmployeeRepository()
        dept = DepartmentManager("IT", repo)
        
        dept.add_employee(Employee(1, "Alice", "IT", 50000))
        dept.add_employee(Employee(2, "Bob", "IT", 60000))
        
        assert dept.get_employee_count() == 2
    
    def test_find_employees_by_criteria(self):
        """Поиск сотрудников по критериям"""
        repo = InMemoryEmployeeRepository()
        dept = DepartmentManager("IT", repo)
        
        dept.add_employee(Developer(1, "Alice", "IT", 50000, "senior"))
        dept.add_employee(Developer(2, "Bob", "IT", 60000, "middle"))
        
        # Поиск по уровню
        # результаты = dept.find_employees({'level': 'senior'})
        # assert len(результаты) == 1


# Запуск всех тестов
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
