"""
Часть 2: Тестирование наследования и иерархии классов сотрудников
"""
import pytest
from datetime import datetime
from Employee import Employee, Manager, Developer, Salesperson
from Abctract_emp import AbstractEmployee
from Department import Department
from Project import Project
from exceptions import (
    InvalidDataError, 
    FinancialValidationError, 
    DuplicateIdError,
    InvalidStatusError
)


class TestAbstractEmployeeInterface:
    """Тесты интерфейса AbstractEmployee"""
    
    def test_abstract_employee_cannot_be_instantiated(self):
        """Проверка что нельзя создать экземпляр AbstractEmployee"""
        with pytest.raises(TypeError):
            AbstractEmployee()


class TestManagerClass:
    """Тесты класса Manager"""
    
    def test_manager_creation_valid(self):
        """Проверка создания менеджера с валидными данными"""
        manager = Manager(1, "John", "Management", 5000, 1000)
        
        assert manager.id == 1
        assert manager.name == "John"
        assert manager.department == "Management"
        assert manager.base_salary == 5000
    
    def test_manager_has_bonus(self):
        """Проверка что менеджер имеет бонус"""
        manager = Manager(1, "John", "Management", 5000, 1000)
        assert manager.bonus == 1000
    
    def test_manager_salary_calculation_with_bonus(self):
        """Проверка расчета зарплаты менеджера с учетом бонуса"""
        manager = Manager(1, "John", "Management", 5000, 1000)
        salary = manager.calculate_salary()
        
        # Зарплата = базовая + бонус
        assert salary == 6000
    
    def test_manager_salary_calculation_different_values(self):
        """Проверка расчета зарплаты при разных значениях"""
        manager1 = Manager(1, "John", "Mgmt", 5000, 500)
        manager2 = Manager(2, "Jane", "Mgmt", 7000, 2000)
        
        assert manager1.calculate_salary() == 5500
        assert manager2.calculate_salary() == 9000
    
    def test_manager_get_info_includes_bonus(self):
        """Проверка что get_info включает информацию о бонусе"""
        manager = Manager(1, "John", "Management", 5000, 1000)
        info = manager.get_info()
        
        assert "1000" in info
        assert "бонус" in info.lower() or "Бонус" in info
    
    def test_manager_get_info_includes_salary(self):
        """Проверка что get_info включает итоговую зарплату"""
        manager = Manager(1, "John", "Management", 5000, 1000)
        info = manager.get_info()
        
        # Итоговая зарплата 6000
        assert "6000" in info
    
    def test_manager_is_abstract_employee(self):
        """Проверка что Manager является AbstractEmployee"""
        manager = Manager(1, "John", "Management", 5000, 1000)
        assert isinstance(manager, AbstractEmployee)


class TestDeveloperClass:
    """Тесты класса Developer"""
    
    def test_developer_creation_valid(self):
        """Проверка создания разработчика с валидными данными"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python", "Java"], "junior")
        
        assert dev.id == 1
        assert dev.name == "Alice"
        assert dev.department == "DEV"
        assert dev.base_salary == 5000
    
    def test_developer_has_tech_stack(self):
        """Проверка что разработчик имеет стек технологий"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python", "Java"], "junior")
        assert dev.tech_stack == ["Python", "Java"]
    
    def test_developer_has_seniority_level(self):
        """Проверка что разработчик имеет уровень квалификации"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "senior")
        assert dev.seniority_level == "senior"
    
    def test_developer_salary_junior(self):
        """Проверка расчета зарплаты junior разработчика"""
        # Предполагаем что junior = базовая зарплата
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "junior")
        salary = dev.calculate_salary()
        
        assert salary == 5000
    
    def test_developer_salary_middle(self):
        """Проверка расчета зарплаты middle разработчика"""
        # Предполагаем коэффициент 1.5x для middle
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "middle")
        salary = dev.calculate_salary()
        
        assert salary == 7500  # 5000 * 1.5
    
    def test_developer_salary_senior(self):
        """Проверка расчета зарплаты senior разработчика"""
        # Предполагаем коэффициент 2.0x для senior
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "senior")
        salary = dev.calculate_salary()
        
        assert salary == 10000  # 5000 * 2.0
    
    @pytest.mark.parametrize("level,expected_multiplier", [
        ("junior", 1.0),
        ("middle", 1.5),
        ("senior", 2.0)
    ])
    def test_developer_salary_by_level(self, level, expected_multiplier):
        """Параметризованный тест расчета зарплаты по уровню"""
        base_salary = 5000
        dev = Developer(1, "Alice", "DEV", base_salary, ["Python"], level)
        
        expected_salary = base_salary * expected_multiplier
        assert dev.calculate_salary() == expected_salary
    
    def test_developer_add_skill(self):
        """Проверка добавления навыка"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "junior")
        
        dev.add_skill("Java")
        assert "Java" in dev.tech_stack
        assert len(dev.tech_stack) == 2
    
    def test_developer_add_multiple_skills(self):
        """Проверка добавления нескольких навыков"""
        dev = Developer(1, "Alice", "DEV", 5000, [], "junior")
        
        dev.add_skill("Python")
        dev.add_skill("Java")
        dev.add_skill("SQL")
        
        assert len(dev.tech_stack) == 3
        assert "Python" in dev.tech_stack
        assert "Java" in dev.tech_stack
        assert "SQL" in dev.tech_stack
    
    def test_developer_get_info_includes_tech_stack(self):
        """Проверка что get_info включает технологии"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python", "Java"], "senior")
        info = dev.get_info()
        
        assert "Python" in info
        assert "Java" in info
    
    def test_developer_get_info_includes_level(self):
        """Проверка что get_info включает уровень"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "senior")
        info = dev.get_info()
        
        assert "senior" in info.lower() or "Senior" in info
    
    def test_developer_is_abstract_employee(self):
        """Проверка что Developer является AbstractEmployee"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "junior")
        assert isinstance(dev, AbstractEmployee)


class TestSalespersonClass:
    """Тесты класса Salesperson"""
    
    def test_salesperson_creation_valid(self):
        """Проверка создания продавца с валидными данными"""
        sales = Salesperson(1, "Bob", "Sales", 4000, 0.15, 50000)
        
        assert sales.id == 1
        assert sales.name == "Bob"
        assert sales.department == "Sales"
        assert sales.base_salary == 4000
    
    def test_salesperson_has_commission_rate(self):
        """Проверка что продавец имеет процент комиссии"""
        sales = Salesperson(1, "Bob", "Sales", 4000, 0.15, 50000)
        assert sales.commission_rate == 0.15
    
    def test_salesperson_has_sales_volume(self):
        """Проверка что продавец имеет объем продаж"""
        sales = Salesperson(1, "Bob", "Sales", 4000, 0.15, 50000)
        assert sales.sales_volume == 50000
    
    def test_salesperson_salary_calculation(self):
        """Проверка расчета зарплаты продавца с комиссией"""
        # Зарплата = базовая + (объем_продаж * процент_комиссии)
        sales = Salesperson(1, "Bob", "Sales", 4000, 0.15, 50000)
        salary = sales.calculate_salary()
        
        # 4000 + (50000 * 0.15) = 4000 + 7500 = 11500
        assert salary == 11500
    
    def test_salesperson_salary_different_values(self):
        """Проверка расчета зарплаты при разных значениях"""
        sales1 = Salesperson(1, "Bob", "Sales", 4000, 0.10, 100000)
        sales2 = Salesperson(2, "Jane", "Sales", 5000, 0.20, 50000)
        
        # 4000 + (100000 * 0.10) = 14000
        assert sales1.calculate_salary() == 14000
        
        # 5000 + (50000 * 0.20) = 15000
        assert sales2.calculate_salary() == 15000
    
    def test_salesperson_update_sales(self):
        """Проверка обновления объема продаж"""
        sales = Salesperson(1, "Bob", "Sales", 4000, 0.15, 50000)
        
        sales.sales_volume = 60000
        salary = sales.calculate_salary()
        
        # 4000 + (60000 * 0.15) = 4000 + 9000 = 13000
        assert salary == 13000
    
    def test_salesperson_get_info_includes_commission(self):
        """Проверка что get_info включает информацию о комиссии"""
        sales = Salesperson(1, "Bob", "Sales", 4000, 0.15, 50000)
        info = sales.get_info()
        
        assert "0.15" in info or "15%" in info
    
    def test_salesperson_get_info_includes_sales_volume(self):
        """Проверка что get_info включает объем продаж"""
        sales = Salesperson(1, "Bob", "Sales", 4000, 0.15, 50000)
        info = sales.get_info()
        
        assert "50000" in info
    
    def test_salesperson_is_abstract_employee(self):
        """Проверка что Salesperson является AbstractEmployee"""
        sales = Salesperson(1, "Bob", "Sales", 4000, 0.15, 50000)
        assert isinstance(sales, AbstractEmployee)


class TestEmployeeHierarchy:
    """Тесты иерархии и полиморфизма сотрудников"""
    
    def test_polymorphic_calculate_salary(self):
        """Проверка полиморфного поведения calculate_salary"""
        employees = [
            Employee(1, "Alice", "IT", 5000),
            Manager(2, "John", "Mgmt", 5000, 1000),
            Developer(3, "Bob", "DEV", 5000, ["Python"], "senior"),
            Salesperson(4, "Jane", "Sales", 4000, 0.15, 50000)
        ]
        
        # Проверяем что каждый тип рассчитывает зарплату по-своему
        assert employees[0].calculate_salary() == 5000
        assert employees[1].calculate_salary() == 6000
        assert employees[2].calculate_salary() == 10000
        assert employees[3].calculate_salary() == 11500
    
    def test_polymorphic_get_info(self):
        """Проверка полиморфного поведения get_info"""
        emp = Employee(1, "Alice", "IT", 5000)
        manager = Manager(1, "John", "Mgmt", 5000, 1000)
        dev = Developer(1, "Bob", "DEV", 5000, ["Python"], "senior")
        
        # Каждый тип возвращает разную информацию
        emp_info = emp.get_info()
        mgr_info = manager.get_info()
        dev_info = dev.get_info()
        
        assert emp_info != mgr_info
        assert mgr_info != dev_info
        assert emp_info != dev_info
    
    def test_employees_in_collection(self):
        """Проверка работы с коллекцией разных типов сотрудников"""
        employees = [
            Employee(1, "Alice", "IT", 5000),
            Manager(2, "John", "Mgmt", 5000, 1000),
            Developer(3, "Bob", "DEV", 5000, ["Python"], "senior")
        ]
        
        # Проверяем что все они AbstractEmployee
        for emp in employees:
            assert isinstance(emp, AbstractEmployee)


class TestDepartmentWithEmployees:
    """Тесты Department с разными типами сотрудников"""
    
    def test_department_add_employee(self):
        """Проверка добавления сотрудника в отдел"""
        dept = Department("IT")
        emp = Employee(1, "Alice", "IT", 5000)
        
        dept.add_employee(emp)
        assert len(dept) == 1
    
    def test_department_add_different_employee_types(self):
        """Проверка добавления разных типов сотрудников"""
        dept = Department("Mixed")
        emp = Employee(1, "Alice", "IT", 5000)
        manager = Manager(2, "John", "Mgmt", 5000, 1000)
        dev = Developer(3, "Bob", "DEV", 5000, ["Python"], "junior")
        
        dept.add_employee(emp)
        dept.add_employee(manager)
        dept.add_employee(dev)
        
        assert len(dept) == 3
    
    def test_department_remove_employee(self):
        """Проверка удаления сотрудника из отдела"""
        dept = Department("IT")
        emp = Employee(1, "Alice", "IT", 5000)
        
        dept.add_employee(emp)
        assert len(dept) == 1
        
        dept.remove_employee(1)
        assert len(dept) == 0
    
    def test_department_calculate_total_salary(self):
        """Проверка расчета суммарной зарплаты отдела"""
        dept = Department("Mixed")
        dept.add_employee(Employee(1, "Alice", "IT", 5000))
        dept.add_employee(Manager(2, "John", "Mgmt", 5000, 1000))
        dept.add_employee(Developer(3, "Bob", "DEV", 5000, ["Python"], "senior"))
        
        # 5000 + 6000 + 10000 = 21000
        total = dept.calculate_total_salary()
        assert total == 21000
    
    def test_department_get_employee_count(self):
        """Проверка получения статистики по типам сотрудников"""
        dept = Department("Mixed")
        dept.add_employee(Employee(1, "Alice", "IT", 5000))
        dept.add_employee(Manager(2, "John", "Mgmt", 5000, 1000))
        dept.add_employee(Developer(3, "Bob", "DEV", 5000, ["Python"], "junior"))
        
        counts = dept.get_employee_count()
        
        assert counts.get("Employee", 0) == 1
        assert counts.get("Manager", 0) == 1
        assert counts.get("Developer", 0) == 1


class TestProjectWithEmployees:
    """Тесты Project с разными типами сотрудников"""
    
    def test_project_add_employee(self):
        """Проверка добавления сотрудника в проект"""
        project = Project(1, "AI Platform", "Разработка AI", datetime.now(), "planning")
        emp = Employee(1, "Alice", "IT", 5000)
        
        project.add_team_member(emp)
        assert len(project) == 1
    
    def test_project_add_different_employee_types(self):
        """Проверка добавления разных типов сотрудников в проект"""
        project = Project(1, "Project", "Description", datetime.now(), "active")
        
        project.add_team_member(Manager(1, "John", "Mgmt", 5000, 1000))
        project.add_team_member(Developer(2, "Bob", "DEV", 5000, ["Python"], "senior"))
        project.add_team_member(Salesperson(3, "Jane", "Sales", 4000, 0.15, 50000))
        
        assert len(project) == 3
    
    def test_project_calculate_total_salary(self):
        """Проверка расчета суммарной зарплаты команды проекта"""
        project = Project(1, "Project", "Desc", datetime.now(), "active")
        
        project.add_team_member(Manager(1, "John", "Mgmt", 5000, 1000))
        project.add_team_member(Developer(2, "Bob", "DEV", 5000, ["Python"], "middle"))
        
        # 6000 + 7500 = 13500
        total = project.calculate_total_salary()
        assert total == 13500


class TestEmployeeValidationByType:
    """Тесты валидации для разных типов сотрудников"""
    
    def test_manager_invalid_bonus_negative(self):
        """Проверка выброса исключения при отрицательном бонусе"""
        with pytest.raises(FinancialValidationError):
            Manager(1, "John", "Mgmt", 5000, -1000)
    
    def test_developer_empty_tech_stack(self):
        """Проверка создания разработчика с пустым стеком технологий"""
        dev = Developer(1, "Alice", "DEV", 5000, [], "junior")
        assert dev.tech_stack == []
    
    def test_salesperson_invalid_commission_rate(self):
        """Проверка выброса исключения при неверном проценте комиссии"""
        with pytest.raises(FinancialValidationError):
            Salesperson(1, "Bob", "Sales", 4000, -0.15, 50000)
    
    def test_salesperson_invalid_sales_volume(self):
        """Проверка выброса исключения при отрицательном объеме продаж"""
        with pytest.raises(FinancialValidationError):
            Salesperson(1, "Bob", "Sales", 4000, 0.15, -50000)
