# refactored/examples.py
"""
Примеры использования рефакторенного кода
Демонстрация всех SOLID принципов в действии
"""

from refactored.validators import EmployeeValidator
from refactored.interfaces import ISalaryCalculable, ISkillManageable
from refactored.repository import InMemoryEmployeeRepository
from refactored.strategies.bonus_strategy import (
    FixedBonusStrategy, PercentageBonusStrategy, SeniorityBonusStrategy
)
from refactored.services import SalaryCalculator, DepartmentManager
from refactored.models.employee_refactored import (
    Employee, Developer, Manager, Salesperson
)


def example_1_srp_validators():
    """
    SRP - Single Responsibility Principle
    Валидаторы отделены от класса Employee
    """
    print("=" * 60)
    print("* ПРИМЕР 1: SRP (Single Responsibility)")
    print("=" * 60)
    
    # Валидация сначала (работает везде)
    try:
        EmployeeValidator.validate_id(123)      #     Работает
        EmployeeValidator.validate_salary(50000) #     Работает
        print("    Валидация прошла успешно")
    except Exception as e:
        print(f"  Ошибка: {e}")
    
    # Создание Employee с валидацией
    emp = Employee(1, "Alice", "IT", 50000)
    print(f"    Создан сотрудник: {emp}")
    print()


def example_2_ocp_strategies():
    """
    OCP - Open/Closed Principle
    Добавление новых стратегий БЕЗ изменения Manager
    """
    print("=" * 60)
    print("* ПРИМЕР 2: OCP (Open/Closed)")
    print("=" * 60)
    
    # Manager с разными стратегиями
    print("\n Фиксированный бонус:")
    manager1 = Manager(1, "Bob", "IT", 60000, FixedBonusStrategy(15000))
    print(f"   Базовая зарплата: 60000")
    print(f"   Бонус: {manager1.calculate_bonus()}")
    print(f"   Итого: {manager1.calculate_salary()}")
    
    print("\n Процентный бонус (20%):")
    manager2 = Manager(2, "Charlie", "IT", 60000, PercentageBonusStrategy(0.2))
    print(f"   Базовая зарплата: 60000")
    print(f"   Бонус: {manager2.calculate_bonus()}")
    print(f"   Итого: {manager2.calculate_salary()}")
    
    print("\n Бонус по уровню:")
    manager3 = Manager(3, "Diana", "IT", 60000, SeniorityBonusStrategy())
    manager3.level = "senior"  # Имитация уровня
    print(f"   Базовая зарплата: 60000")
    print(f"   Бонус: {manager3.calculate_bonus()}")
    print(f"   Итого: {manager3.calculate_salary()}")
    
    print("\n   Всё работает! БЕЗ изменения класса Manager!")
    print()


def example_3_lsp_polymorphism():
    """
    LSP - Liskov Substitution Principle
    Все сотрудники подставляются везде
    """
    print("=" * 60)
    print("* ПРИМЕР 3: LSP (Liskov Substitution)")
    print("=" * 60)
    
    # Список разных типов сотрудников
    employees = [
        Employee(1, "Alice", "IT", 50000),
        Developer(2, "Bob", "IT", 60000, "middle"),
        Manager(3, "Charlie", "IT", 70000, FixedBonusStrategy(10000)),
        Salesperson(4, "Diana", "Sales", 40000, 0.1)
    ]
    
    # Все подставляются везде (полиморфизм)
    print("Зарплаты сотрудников:")
    total = 0
    for emp in employees:
        salary = emp.calculate_salary()
        print(f"   {emp.name:15} -> {salary:>10.2f}")
        total += salary
    
    print(f"   {'':15} {'─' * 15}")
    print(f"   {'Итого':15} -> {total:>10.2f}")
    print()


def example_4_isp_interfaces():
    """
    ISP - Interface Segregation Principle
    Каждый класс реализует только нужные интерфейсы
    """
    print("=" * 60)
    print("* ПРИМЕР 4: ISP (Interface Segregation)")
    print("=" * 60)
    
    emp = Employee(1, "Alice", "IT", 50000)
    dev = Developer(2, "Bob", "IT", 60000, "senior")
    manager = Manager(3, "Charlie", "IT", 70000, FixedBonusStrategy(10000))
    
    # Проверка интерфейсов
    print("Employee реализует:")
    print(f"       ISalaryCalculable: {isinstance(emp, ISalaryCalculable)}")
    print(f"     ISkillManageable: {isinstance(emp, ISkillManageable)}")
    
    print("\nDeveloper реализует:")
    print(f"       ISalaryCalculable: {isinstance(dev, ISalaryCalculable)}")
    print(f"       ISkillManageable: {isinstance(dev, ISkillManageable)}")
    
    print("\nManager реализует:")
    print(f"       ISalaryCalculable: {isinstance(manager, ISalaryCalculable)}")
    print(f"     ISkillManageable: {isinstance(manager, ISkillManageable)}")
    
    # Используем только то, что реализовано
    print("\nИспользование:")
    dev.add_skill("Python")
    dev.add_skill("JavaScript")
    print(f"   Dev навыки: {dev.get_skills()}")
    print()


def example_5_dip_repository():
    """
    DIP - Dependency Inversion Principle
    Repository Pattern - легко менять реализацию
    """
    print("=" * 60)
    print("* ПРИМЕР 5: DIP (Dependency Inversion)")
    print("=" * 60)
    
    # Repository (in-memory)
    repo = InMemoryEmployeeRepository()
    dept = DepartmentManager("IT", repo)
    
    # Добавляем сотрудников
    dept.add_employee(Employee(1, "Alice", "IT", 50000))
    dept.add_employee(Developer(2, "Bob", "IT", 60000, "middle"))
    dept.add_employee(Manager(3, "Charlie", "IT", 70000, FixedBonusStrategy(10000)))
    
    print(f"В отделе {dept.get_employee_count()} сотрудников")
    print(f"ID сотрудников: {dept.get_employee_ids()}")
    
    # Получаем сотрудника
    emp = dept.get_employee(2)
    print(f"\nПолучен сотрудник: {emp}")
    
    # ТО ЖЕ, но с другим repository (можно в будущем):
    # db_repo = DatabaseEmployeeRepository(connection)
    # dept_db = DepartmentManager("IT", db_repo)
    # dept_db.add_employee(...)  # Работает так же!
    
    print("\n   Легко менять реализацию хранилища!")
    print()


def example_6_salary_calculator():
    """
    SRP - Services
    SalaryCalculator отвечает только за расчеты
    """
    print("=" * 60)
    print("* ПРИМЕР 6: SRP (Services)")
    print("=" * 60)
    
    employees = [
        Employee(1, "Alice", "IT", 50000),
        Developer(2, "Bob", "IT", 60000, "senior"),  # 120000
        Manager(3, "Charlie", "IT", 70000, FixedBonusStrategy(15000)),
        Salesperson(4, "Diana", "Sales", 40000, 0.1)
    ]
    
    # Расчеты через сервис
    total = SalaryCalculator.calculate_total_salary(employees)
    avg = SalaryCalculator.calculate_average_salary(employees)
    
    print(f"Общая зарплата: {total:.2f}")
    print(f"Средняя зарплата: {avg:.2f}")
    
    # Статистика
    stats = SalaryCalculator.get_salary_statistics(employees)
    print(f"\nСтатистика:")
    print(f"   Всего: {stats['total']:.2f}")
    print(f"   Среднее: {stats['average']:.2f}")
    print(f"   Минимум: {stats['min']:.2f}")
    print(f"   Максимум: {stats['max']:.2f}")
    print(f"   Сотрудников: {stats['count']}")
    print()


def example_7_complete_workflow():
    """
    Полный рабочий процесс
    Все SOLID принципы в действии
    """
    print("=" * 60)
    print("* ПРИМЕР 7: Полный рабочий процесс")
    print("=" * 60)
    
    # 1. Создаем репозиторий (DIP)
    repo = InMemoryEmployeeRepository()
    
    # 2. Создаем отдел (SRP - управление)
    dept = DepartmentManager("IT", repo)
    
    # 3. Добавляем сотрудников (валидация через SRP)
    dept.add_employee(Employee(1, "Alice", "IT", 50000))
    dev = Developer(2, "Bob", "IT", 60000, "senior")
    dev.add_skill("Python")
    dev.add_skill("JavaScript")
    dev.add_skill("Go")
    dept.add_employee(dev)
    
    manager = Manager(3, "Charlie", "IT", 70000, PercentageBonusStrategy(0.15))
    dept.add_employee(manager)
    
    sp = Salesperson(4, "Diana", "Sales", 40000, 0.1)
    sp.set_sales_amount(500000)  # $500k продаж
    dept.add_employee(sp)
    
    # 4. Получаем информацию
    print(f"Отдел: {dept.name}")
    print(f"Сотрудников: {dept.get_employee_count()}\n")
    
    # 5. Выводим информацию
    employees = dept.get_all_employees()
    for emp in employees:
        print(f"{emp.get_info()}\n")
    
    # 6. Считаем статистику (SRP - сервис)
    stats = SalaryCalculator.get_salary_statistics(employees)
    print("=" * 60)
    print(f"Статистика по зарплатам:")
    print(f"   Всего: {stats['total']:,.2f}")
    print(f"   Среднее: {stats['average']:,.2f}")
    print(f"   Min: {stats['min']:,.2f}")
    print(f"   Max: {stats['max']:,.2f}")
    print()


if __name__ == "__main__":
    print("\n")
    print("=" * 60)
    print("=" + " " * 58 + "=")
    print("=" + "  ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ SOLID ПРИНЦИПОВ".center(58) + "=")
    print("=" + " " * 58 + "=")
    print("=" * 60)
    print("\n")
    
    example_1_srp_validators()
    example_2_ocp_strategies()
    example_3_lsp_polymorphism()
    example_4_isp_interfaces()
    example_5_dip_repository()
    example_6_salary_calculator()
    example_7_complete_workflow()
    
    print("=" * 60)
    print("    Все примеры выполнены успешно!")
    print("=" * 60)
