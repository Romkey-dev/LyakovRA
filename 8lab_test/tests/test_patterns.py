"""
Часть 5: Тестирование паттернов проектирования
"""
import pytest
from datetime import datetime
from Employee import Employee, Manager, Developer, Salesperson
from Abctract_emp import AbstractEmployee
from Department import Department
from Project import Project
from Company import Company
from singleton import DatabaseConnection
from factory_method import EmployeeFactory, DeveloperFactory, ManagerFactory
from Builder import EmployeeBuilder
from decorator import BonusDecorator, TrainingDecorator
from observer import Observer, Observable, NotificationSystem, LoggingSystem
from Strategy import BonusStrategy, PerformanceBonusStrategy, SeniorityBonusStrategy, EmployeeWithStrategy


class TestSingletonPattern:
    """Тесты паттерна Singleton"""
    
    def test_singleton_same_instance(self):
        """Проверка что Singleton возвращает один и тот же экземпляр"""
        # Получаем два экземпляра
        db1 = DatabaseConnection.get_instance()
        db2 = DatabaseConnection.get_instance()
        
        # Проверяем что это один и тот же объект
        assert db1 is db2
    
    def test_singleton_same_id(self):
        """Проверка что ID объектов одинаковые"""
        db1 = DatabaseConnection.get_instance()
        db2 = DatabaseConnection.get_instance()
        
        assert id(db1) == id(db2)
    
    def test_singleton_connection_persistence(self):
        """Проверка что подключение сохраняется между вызовами"""
        db1 = DatabaseConnection.get_instance()
        conn1 = db1.get_connection()
        
        db2 = DatabaseConnection.get_instance()
        conn2 = db2.get_connection()
        
        # Одно и то же подключение
        assert conn1 is conn2
    
    def test_singleton_multiple_get_instance_calls(self):
        """Проверка что множественные вызовы get_instance возвращают один объект"""
        instances = [DatabaseConnection.get_instance() for _ in range(5)]
        
        # Все должны быть идентичны
        for i in range(1, len(instances)):
            assert instances[0] is instances[i]


class TestFactoryMethodPattern:
    """Тесты паттерна Factory Method"""
    
    def test_developer_factory_creates_developer(self):
        """Проверка что DeveloperFactory создает Developer"""
        factory = DeveloperFactory()
        
        dev = factory.create_employee(
            id=1,
            name="John",
            department="DEV",
            base_salary=5000,
            tech_stack=["Python"],
            seniority_level="senior"
        )
        
        assert isinstance(dev, Developer)
        assert dev.name == "John"
    
    def test_manager_factory_creates_manager(self):
        """Проверка что ManagerFactory создает Manager"""
        factory = ManagerFactory()
        
        mgr = factory.create_employee(
            id=1,
            name="Jane",
            department="Mgmt",
            base_salary=5000,
            bonus=1000
        )
        
        assert isinstance(mgr, Manager)
        assert mgr.name == "Jane"
    
    def test_factory_creates_correct_type(self):
        """Проверка что фабрика создает правильный тип объекта"""
        dev_factory = DeveloperFactory()
        mgr_factory = ManagerFactory()
        
        dev = dev_factory.create_employee(
            id=1, name="Alice", department="DEV",
            base_salary=5000, tech_stack=[], seniority_level="junior"
        )
        
        mgr = mgr_factory.create_employee(
            id=2, name="Bob", department="Mgmt",
            base_salary=7000, bonus=1500
        )
        
        assert type(dev).__name__ == "Developer"
        assert type(mgr).__name__ == "Manager"
    
    def test_factory_encapsulation(self):
        """Проверка инкапсуляции логики создания объектов"""
        factory = DeveloperFactory()
        
        # Фабрика скрывает детали создания
        dev = factory.create_employee(
            id=1, name="Charlie", department="DEV",
            base_salary=5000, tech_stack=["Java"], seniority_level="middle"
        )
        
        # Мы получаем готовый объект с правильными параметрами
        assert dev.calculate_salary() == 7500  # middle multiplier


class TestBuilderPattern:
    """Тесты паттерна Builder"""
    
    def test_builder_creates_employee(self):
        """Проверка создания сотрудника через Builder"""
        emp = (EmployeeBuilder()
               .set_id(1)
               .set_name("Alice")
               .set_department("IT")
               .set_base_salary(5000)
               .build())
        
        assert emp.id == 1
        assert emp.name == "Alice"
        assert isinstance(emp, Employee)
    
    def test_builder_creates_developer(self):
        """Проверка создания Developer через Builder"""
        dev = (EmployeeBuilder()
               .set_id(1)
               .set_name("Bob")
               .set_department("DEV")
               .set_base_salary(5000)
               .set_employee_type("Developer")
               .add_skill("Python")
               .add_skill("Java")
               .build())
        
        assert isinstance(dev, Developer)
        assert "Python" in dev.tech_stack
        assert "Java" in dev.tech_stack
    
    def test_builder_creates_manager(self):
        """Проверка создания Manager через Builder"""
        mgr = (EmployeeBuilder()
               .set_id(1)
               .set_name("Charlie")
               .set_department("Mgmt")
               .set_base_salary(5000)
               .set_employee_type("Manager")
               .set_bonus(1000)
               .build())
        
        assert isinstance(mgr, Manager)
        assert mgr.bonus == 1000
    
    def test_builder_fluent_interface(self):
        """Проверка fluent интерфейса Builder"""
        # Builder должен возвращать self для цепочки вызовов
        builder = EmployeeBuilder()
        
        result = builder.set_id(1).set_name("Alice").set_department("IT")
        
        # Все методы должны возвращать builder для цепочки
        assert isinstance(result, EmployeeBuilder)
    
    def test_builder_with_multiple_skills(self):
        """Проверка добавления нескольких навыков через Builder"""
        dev = (EmployeeBuilder()
               .set_id(1)
               .set_name("Developer")
               .set_department("DEV")
               .set_base_salary(5000)
               .set_employee_type("Developer")
               .add_skill("Python")
               .add_skill("JavaScript")
               .add_skill("SQL")
               .build())
        
        assert len(dev.tech_stack) == 3
        assert all(skill in dev.tech_stack for skill in ["Python", "JavaScript", "SQL"])


class TestDecoratorPattern:
    """Тесты паттерна Decorator"""
    
    def test_bonus_decorator_adds_bonus(self):
        """Проверка что BonusDecorator добавляет бонус к зарплате"""
        emp = Employee(1, "Alice", "IT", 5000)
        decorated = BonusDecorator(emp, 500)
        
        assert decorated.calculate_salary() == 5500
    
    def test_bonus_decorator_stacking(self):
        """Проверка многоуровневого добавления бонусов"""
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Добавляем два бонуса
        decorated = BonusDecorator(BonusDecorator(emp, 500), 300)
        
        assert decorated.calculate_salary() == 5800
    
    def test_training_decorator_adds_info(self):
        """Проверка что TrainingDecorator добавляет информацию об обучении"""
        emp = Employee(1, "Alice", "IT", 5000)
        decorated = TrainingDecorator(emp, "Python Advanced")
        
        info = decorated.get_info()
        
        assert "Python Advanced" in info
    
    def test_decorator_combination(self):
        """Проверка комбинирования разных декораторов"""
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Применяем бонус и обучение
        decorated = TrainingDecorator(
            BonusDecorator(emp, 1000),
            "DevOps Course"
        )
        
        assert decorated.calculate_salary() == 6000
        assert "DevOps Course" in decorated.get_info()
    
    def test_decorator_preserves_original(self):
        """Проверка что декоратор не изменяет оригинальный объект"""
        emp = Employee(1, "Alice", "IT", 5000)
        
        decorated = BonusDecorator(emp, 500)
        
        # Оригинальная зарплата не должна измениться
        assert emp.calculate_salary() == 5000
        
        # Декорированная зарплата должна измениться
        assert decorated.calculate_salary() == 5500


class TestObserverPattern:
    """Тесты паттерна Observer"""
    
    def test_observer_notification(self):
        """Проверка что наблюдатель получает уведомления"""
        observable = Observable()
        notification_system = NotificationSystem()
        
        # Добавляем наблюдателя
        observable.add_observer(notification_system)
        
        # Отправляем уведомление
        observable.notify_observers("Test message")
        
        # Проверяем что notification_system присутствует
        assert notification_system in observable._observers
    
    def test_multiple_observers(self):
        """Проверка работы с несколькими наблюдателями"""
        observable = Observable()
        
        notification = NotificationSystem()
        logging = LoggingSystem()
        
        observable.add_observer(notification)
        observable.add_observer(logging)
        
        assert len(observable._observers) == 2
    
    def test_observer_removal(self):
        """Проверка удаления наблюдателя"""
        observable = Observable()
        observer = NotificationSystem()
        
        observable.add_observer(observer)
        assert len(observable._observers) == 1
        
        observable.remove_observer(observer)
        assert len(observable._observers) == 0
    
    def test_observer_is_abstract(self):
        """Проверка что Observer является абстрактным"""
        # Нельзя создать экземпляр Observer напрямую
        with pytest.raises(TypeError):
            Observer()
    
    def test_notification_system_implements_observer(self):
        """Проверка что NotificationSystem реализует Observer"""
        notification = NotificationSystem()
        assert isinstance(notification, Observer)
    
    def test_logging_system_implements_observer(self):
        """Проверка что LoggingSystem реализует Observer"""
        logging = LoggingSystem()
        assert isinstance(logging, Observer)


class TestStrategyPattern:
    """Тесты паттерна Strategy"""
    
    def test_performance_bonus_strategy(self):
        """Проверка стратегии бонуса за производительность"""
        emp = Employee(1, "Alice", "IT", 5000)
        
        strategy = PerformanceBonusStrategy()
        bonus = strategy.calculate_bonus(emp)
        
        # 10% от базовой зарплаты
        assert bonus == 500
    
    def test_seniority_bonus_strategy_junior(self):
        """Проверка стратегии бонуса за уровень junior"""
        emp = Developer(1, "Alice", "DEV", 5000, ["Python"], "junior")
        
        strategy = SeniorityBonusStrategy()
        bonus = strategy.calculate_bonus(emp)
        
        # 5% для junior
        assert bonus == 250
    
    def test_seniority_bonus_strategy_middle(self):
        """Проверка стратегии бонуса за уровень middle"""
        emp = Developer(1, "Alice", "DEV", 5000, ["Python"], "middle")
        
        strategy = SeniorityBonusStrategy()
        bonus = strategy.calculate_bonus(emp)
        
        # 10% для middle
        assert bonus == 500
    
    def test_seniority_bonus_strategy_senior(self):
        """Проверка стратегии бонуса за уровень senior"""
        emp = Developer(1, "Alice", "DEV", 5000, ["Python"], "senior")
        
        strategy = SeniorityBonusStrategy()
        bonus = strategy.calculate_bonus(emp)
        
        # 20% для senior
        assert bonus == 1000
    
    def test_employee_with_strategy(self):
        """Проверка работы Employee с Strategy"""
        emp = Employee(1, "Alice", "IT", 5000)
        emp_with_strategy = EmployeeWithStrategy(emp, PerformanceBonusStrategy())
        
        # базовая зарплата + бонус
        assert emp_with_strategy.calculate_total_salary() == 5500
    
    def test_strategy_switching(self):
        """Проверка переключения между стратегиями"""
        emp = Developer(1, "Alice", "DEV", 5000, ["Python"], "senior")
        emp_with_strategy = EmployeeWithStrategy(emp, PerformanceBonusStrategy())
        
        salary1 = emp_with_strategy.calculate_total_salary()
        
        # Меняем стратегию
        emp_with_strategy.set_bonus_strategy(SeniorityBonusStrategy())
        salary2 = emp_with_strategy.calculate_total_salary()
        
        # Зарплаты должны быть разными
        assert salary1 != salary2
    
    def test_strategy_is_abstract(self):
        """Проверка что BonusStrategy является абстрактным"""
        with pytest.raises(TypeError):
            BonusStrategy()


class TestPatternIntegration:
    """Интеграционные тесты сочетания паттернов"""
    
    def test_builder_factory_integration(self):
        """Проверка взаимодействия Builder и Factory паттернов"""
        # Builder для создания сложного объекта
        dev = (EmployeeBuilder()
               .set_id(1)
               .set_name("Alice")
               .set_department("DEV")
               .set_base_salary(5000)
               .set_employee_type("Developer")
               .add_skill("Python")
               .build())
        
        # Factory могла бы использоваться для создания сотрудников
        factory = DeveloperFactory()
        dev2 = factory.create_employee(
            id=2, name="Bob", department="DEV",
            base_salary=5000, tech_stack=["Python"],
            seniority_level="junior"
        )
        
        assert isinstance(dev, Developer)
        assert isinstance(dev2, Developer)
    
    def test_decorator_strategy_integration(self):
        """Проверка взаимодействия Decorator и Strategy"""
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Добавляем бонус через Decorator
        decorated = BonusDecorator(emp, 500)
        
        # Применяем Strategy к декорированному объекту
        emp_with_strategy = EmployeeWithStrategy(decorated, PerformanceBonusStrategy())
        
        # базовая + бонус + стратегия = 5000 + 500 + (5500 * 0.1) = 6050
        assert emp_with_strategy.calculate_total_salary() == 6050
    
    def test_singleton_with_company(self):
        """Проверка использования Singleton при работе с Company"""
        company1 = Company("TechCorp")
        db1 = DatabaseConnection.get_instance()
        
        company2 = Company("TechCorp")
        db2 = DatabaseConnection.get_instance()
        
        # Одна и та же БД для обеих компаний
        assert db1 is db2
    
    def test_full_pattern_workflow(self):
        """Комплексный тест использования множественных паттернов"""
        # 1. Singleton для БД
        db = DatabaseConnection.get_instance()
        
        # 2. Builder для создания сотрудника
        emp = (EmployeeBuilder()
               .set_id(1)
               .set_name("Alice")
               .set_department("DEV")
               .set_base_salary(5000)
               .set_employee_type("Developer")
               .add_skill("Python")
               .build())
        
        # 3. Decorator для добавления функциональности
        decorated = BonusDecorator(emp, 500)
        
        # 4. Strategy для гибкого расчета
        emp_with_strategy = EmployeeWithStrategy(decorated, SeniorityBonusStrategy())
        
        # 5. Observer для уведомлений
        observable = Observable()
        observer = NotificationSystem()
        observable.add_observer(observer)
        
        # Проверяем все слои
        assert isinstance(db, DatabaseConnection)
        assert isinstance(emp, Developer)
        assert decorated.calculate_salary() == 5500
        assert emp_with_strategy.calculate_total_salary() > 5500
        assert observer in observable._observers
