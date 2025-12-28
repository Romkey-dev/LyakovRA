"""
Часть 3: Тестирование полиморфизма и магических методов
"""
import pytest
from datetime import datetime
from Employee import Employee, Manager, Developer, Salesperson
from Abctract_emp import AbstractEmployee
from Department import Department
from Project import Project
from exceptions import InvalidDataError, FinancialValidationError


class TestEmployeeEquality:
    """Тесты оператора равенства для сотрудников"""
    
    def test_employee_equality_same_id(self):
        """Проверка равенства сотрудников с одинаковым ID"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(1, "Jane", "HR", 4000)
        
        assert emp1 == emp2
    
    def test_employee_inequality_different_id(self):
        """Проверка неравенства сотрудников с разными ID"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 5000)
        
        assert emp1 != emp2
    
    def test_employee_equality_with_different_types(self):
        """Проверка что равенство работает для разных типов сотрудников"""
        emp = Employee(1, "John", "IT", 5000)
        manager = Manager(1, "Jane", "Mgmt", 7000, 1000)
        
        assert emp == manager
    
    def test_employee_equality_is_not_same_as_identity(self):
        """Проверка что == проверяет ID, а не идентичность объектов"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(1, "John", "IT", 5000)
        
        assert emp1 == emp2
        assert emp1 is not emp2


class TestEmployeeComparison:
    """Тесты операторов сравнения для сотрудников"""
    
    def test_employee_less_than(self):
        """Проверка оператора < по зарплате"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 6000)
        
        assert emp1 < emp2
        assert not emp2 < emp1
    
    def test_employee_greater_than(self):
        """Проверка оператора > по зарплате"""
        emp1 = Employee(1, "John", "IT", 6000)
        emp2 = Employee(2, "Bob", "IT", 5000)
        
        assert emp1 > emp2
        assert not emp2 > emp1
    
    def test_employee_less_than_equal(self):
        """Проверка оператора <= по зарплате"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 5000)
        emp3 = Employee(3, "Jane", "IT", 6000)
        
        assert emp1 <= emp2
        assert emp1 <= emp3
    
    def test_employee_greater_than_equal(self):
        """Проверка оператора >= по зарплате"""
        emp1 = Employee(1, "John", "IT", 6000)
        emp2 = Employee(2, "Bob", "IT", 6000)
        emp3 = Employee(3, "Jane", "IT", 5000)
        
        assert emp1 >= emp2
        assert emp1 >= emp3
    
    def test_employee_comparison_polymorphic(self):
        """Проверка сравнения разных типов сотрудников по рассчитанной зарплате"""
        emp = Employee(1, "John", "IT", 5000)
        manager = Manager(2, "Jane", "Mgmt", 5000, 500)  # 5500 total
        dev = Developer(3, "Bob", "DEV", 5000, ["Python"], "senior")  # 10000 total
        
        assert emp < manager
        assert manager < dev
        assert emp < dev


class TestEmployeeAddition:
    """Тесты операторов сложения"""
    
    def test_employee_addition_two_employees(self):
        """Проверка сложения двух сотрудников"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 6000)
        
        result = emp1 + emp2
        assert result == 11000
    
    def test_employee_addition_multiple_employees(self):
        """Проверка сложения нескольких сотрудников"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 6000)
        emp3 = Employee(3, "Jane", "IT", 7000)
        
        result = emp1 + emp2 + emp3
        assert result == 18000
    
    def test_employee_addition_with_number(self):
        """Проверка сложения сотрудника с числом"""
        emp = Employee(1, "John", "IT", 5000)
        
        result = emp + 1000
        assert result == 6000
    
    def test_employee_reverse_addition_with_number(self):
        """Проверка обратного сложения (число + сотрудник)"""
        emp = Employee(1, "John", "IT", 5000)
        
        result = 1000 + emp
        assert result == 6000
    
    def test_employee_addition_polymorphic(self):
        """Проверка сложения разных типов сотрудников"""
        emp = Employee(1, "John", "IT", 5000)
        manager = Manager(2, "Jane", "Mgmt", 5000, 1000)  # 6000 total
        dev = Developer(3, "Bob", "DEV", 5000, ["Python"], "middle")  # 7500 total
        
        # 5000 + 6000 = 11000
        result1 = emp + manager
        assert result1 == 11000
        
        # 6000 + 7500 = 13500
        result2 = manager + dev
        assert result2 == 13500
    
    def test_employee_sum_in_list(self):
        """Проверка суммирования через sum() для списка сотрудников"""
        employees = [
            Employee(1, "John", "IT", 5000),
            Employee(2, "Bob", "IT", 6000),
            Employee(3, "Jane", "IT", 7000)
        ]
        
        total = sum([emp.calculate_salary() for emp in employees])
        assert total == 18000
    
    def test_employee_radd_for_sum(self):
        """Проверка __radd__ для корректной работы с sum()"""
        employees = [
            Employee(1, "John", "IT", 5000),
            Manager(2, "Jane", "Mgmt", 5000, 1000),
            Developer(3, "Bob", "DEV", 5000, ["Python"], "senior")
        ]
        
        # 5000 + 6000 + 10000 = 21000
        total = sum([emp.calculate_salary() for emp in employees])
        assert total == 21000


class TestDepartmentMagicMethods:
    """Тесты магических методов класса Department"""
    
    def test_department_len(self):
        """Проверка __len__ - получение количества сотрудников"""
        dept = Department("IT")
        
        assert len(dept) == 0
        
        dept.add_employee(Employee(1, "John", "IT", 5000))
        assert len(dept) == 1
        
        dept.add_employee(Employee(2, "Bob", "IT", 6000))
        assert len(dept) == 2
    
    def test_department_getitem_by_index(self):
        """Проверка __getitem__ - доступ по индексу"""
        dept = Department("IT")
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 6000)
        
        dept.add_employee(emp1)
        dept.add_employee(emp2)
        
        assert dept[0] == emp1
        assert dept[1] == emp2
    
    def test_department_getitem_negative_index(self):
        """Проверка __getitem__ с отрицательным индексом"""
        dept = Department("IT")
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 6000)
        
        dept.add_employee(emp1)
        dept.add_employee(emp2)
        
        assert dept[-1] == emp2
        assert dept[-2] == emp1
    
    def test_department_getitem_slice(self):
        """Проверка __getitem__ со срезом"""
        dept = Department("IT")
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 6000)
        emp3 = Employee(3, "Jane", "IT", 7000)
        
        dept.add_employee(emp1)
        dept.add_employee(emp2)
        dept.add_employee(emp3)
        
        slice_result = dept[0:2]
        assert len(slice_result) == 2
        assert emp1 in slice_result
        assert emp2 in slice_result
    
    def test_department_getitem_out_of_range(self):
        """Проверка __getitem__ с индексом вне диапазона"""
        dept = Department("IT")
        dept.add_employee(Employee(1, "John", "IT", 5000))
        
        with pytest.raises(IndexError):
            dept[10]
    
    def test_department_contains(self):
        """Проверка __contains__ - оператор in"""
        dept = Department("IT")
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 6000)
        emp3 = Employee(3, "Jane", "IT", 7000)
        
        dept.add_employee(emp1)
        dept.add_employee(emp2)
        
        assert emp1 in dept
        assert emp2 in dept
        assert emp3 not in dept
    
    def test_department_str(self):
        """Проверка __str__ - строковое представление"""
        dept = Department("IT")
        dept.add_employee(Employee(1, "John", "IT", 5000))
        dept.add_employee(Employee(2, "Bob", "IT", 6000))
        
        str_repr = str(dept)
        
        assert "IT" in str_repr
        assert "2" in str_repr  # количество сотрудников
    
    def test_department_iter(self):
        """Проверка __iter__ - итерация по отделу"""
        dept = Department("IT")
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 6000)
        emp3 = Employee(3, "Jane", "IT", 7000)
        
        dept.add_employee(emp1)
        dept.add_employee(emp2)
        dept.add_employee(emp3)
        
        # Проверяем итерацию
        count = 0
        for employee in dept:
            count += 1
            assert isinstance(employee, AbstractEmployee)
        
        assert count == 3
    
    def test_department_iteration_in_loop(self):
        """Проверка использования итерации в цикле for"""
        dept = Department("IT")
        employees = [
            Employee(1, "John", "IT", 5000),
            Employee(2, "Bob", "IT", 6000),
            Employee(3, "Jane", "IT", 7000)
        ]
        
        for emp in employees:
            dept.add_employee(emp)
        
        # Собираем ID через итерацию
        ids = [emp.id for emp in dept]
        assert ids == [1, 2, 3]
    
    def test_department_repr(self):
        """Проверка __repr__ - официальное представление"""
        dept = Department("IT")
        dept.add_employee(Employee(1, "John", "IT", 5000))
        
        repr_str = repr(dept)
        
        assert "Department" in repr_str
        assert "IT" in repr_str


class TestProjectMagicMethods:
    """Тесты магических методов класса Project"""
    
    def test_project_len(self):
        """Проверка __len__ для проекта"""
        project = Project(1, "Project", "Desc", datetime.now(), "planning")
        
        assert len(project) == 0
        
        project.add_team_member(Employee(1, "John", "IT", 5000))
        assert len(project) == 1
    
    def test_project_contains(self):
        """Проверка __contains__ для проекта"""
        project = Project(1, "Project", "Desc", datetime.now(), "planning")
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 6000)
        
        project.add_team_member(emp1)
        
        assert emp1 in project
        assert emp2 not in project
    
    def test_project_str(self):
        """Проверка __str__ для проекта"""
        project = Project(1, "AI Project", "Desc", datetime.now(), "active")
        project.add_team_member(Employee(1, "John", "IT", 5000))
        
        str_repr = str(project)
        
        assert "AI Project" in str_repr
        assert "active" in str_repr
        assert "1" in str_repr  # размер команды


class TestEmployeeToDict:
    """Тесты сериализации в словарь"""
    
    def test_employee_to_dict_structure(self):
        """Проверка структуры словаря при сериализации"""
        emp = Employee(1, "John", "IT", 5000)
        data = emp.to_dict()
        
        assert 'type' in data
        assert 'id' in data
        assert 'name' in data
        assert 'department' in data
        assert 'base_salary' in data
    
    def test_employee_to_dict_values(self):
        """Проверка значений в словаре"""
        emp = Employee(1, "John", "IT", 5000)
        data = emp.to_dict()
        
        assert data['id'] == 1
        assert data['name'] == "John"
        assert data['department'] == "IT"
        assert data['base_salary'] == 5000
        assert data['type'] == "Employee"
    
    def test_manager_to_dict(self):
        """Проверка сериализации Manager"""
        manager = Manager(1, "John", "Mgmt", 5000, 1000)
        data = manager.to_dict()
        
        assert data['type'] == "Manager"
        assert data['bonus'] == 1000
    
    def test_developer_to_dict(self):
        """Проверка сериализации Developer"""
        dev = Developer(1, "John", "DEV", 5000, ["Python", "Java"], "senior")
        data = dev.to_dict()
        
        assert data['type'] == "Developer"
        assert 'Python' in data['tech_stack']
        assert 'Java' in data['tech_stack']
        assert data['seniority_level'] == "senior"
    
    def test_salesperson_to_dict(self):
        """Проверка сериализации Salesperson"""
        sales = Salesperson(1, "John", "Sales", 4000, 0.15, 50000)
        data = sales.to_dict()
        
        assert data['type'] == "Salesperson"
        assert data['commission_rate'] == 0.15
        assert data['sales_volume'] == 50000


class TestEmployeeFromDict:
    """Тесты десериализации из словаря"""
    
    def test_employee_from_dict_roundtrip(self):
        """Проверка полного цикла сериализации и десериализации"""
        original = Employee(1, "John", "IT", 5000)
        
        # Serialize
        data = original.to_dict()
        
        # Deserialize
        restored = Employee.from_dict(data)
        
        # Verify
        assert restored.id == original.id
        assert restored.name == original.name
        assert restored.department == original.department
        assert restored.base_salary == original.base_salary
    
    def test_from_dict_missing_required_field(self):
        """Проверка выброса исключения при отсутствии поля"""
        data = {'id': 1, 'name': 'John'}  # missing department and base_salary
        
        with pytest.raises(InvalidDataError):
            Employee.from_dict(data)
    
    def test_from_dict_invalid_id_type(self):
        """Проверка выброса исключения при неверном типе ID"""
        data = {
            'id': 'abc',  # должно быть int
            'name': 'John',
            'department': 'IT',
            'base_salary': 5000
        }
        
        with pytest.raises(InvalidDataError):
            Employee.from_dict(data)


class TestDepartmentSerialization:
    """Тесты сериализации отдела"""
    
    def test_department_to_dict(self):
        """Проверка сериализации отдела в словарь"""
        dept = Department("IT")
        dept.add_employee(Employee(1, "John", "IT", 5000))
        
        data = dept.to_dict()
        
        assert data['name'] == "IT"
        assert 'employees' in data
        assert len(data['employees']) == 1
    
    def test_department_to_dict_multiple_employees(self):
        """Проверка сериализации отдела с несколькими сотрудниками"""
        dept = Department("IT")
        dept.add_employee(Employee(1, "John", "IT", 5000))
        dept.add_employee(Manager(2, "Jane", "Mgmt", 5000, 1000))
        
        data = dept.to_dict()
        
        assert len(data['employees']) == 2


class TestPolymorphicBehavior:
    """Тесты полиморфного поведения"""
    
    def test_polymorphic_collection_iteration(self):
        """Проверка итерации по коллекции разных типов с полиморфизмом"""
        dept = Department("Mixed")
        dept.add_employee(Employee(1, "John", "IT", 5000))
        dept.add_employee(Manager(2, "Jane", "Mgmt", 5000, 1000))
        dept.add_employee(Developer(3, "Bob", "DEV", 5000, ["Python"], "senior"))
        
        salaries = []
        for emp in dept:
            salaries.append(emp.calculate_salary())
        
        # 5000 + 6000 + 10000 = 21000
        assert sum(salaries) == 21000
    
    def test_polymorphic_sorting_by_salary(self):
        """Проверка сортировки разных типов сотрудников по зарплате"""
        employees = [
            Developer(3, "Bob", "DEV", 5000, ["Python"], "senior"),  # 10000
            Manager(2, "Jane", "Mgmt", 5000, 1000),  # 6000
            Employee(1, "John", "IT", 5000),  # 5000
        ]
        
        # Сортировка по зарплате
        sorted_employees = sorted(employees, key=lambda e: e.calculate_salary())
        
        assert sorted_employees[0].calculate_salary() == 5000
        assert sorted_employees[1].calculate_salary() == 6000
        assert sorted_employees[2].calculate_salary() == 10000
    
    def test_polymorphic_get_info_all_types(self):
        """Проверка что каждый тип возвращает разную информацию"""
        emp = Employee(1, "John", "IT", 5000)
        manager = Manager(2, "Jane", "Mgmt", 5000, 1000)
        dev = Developer(3, "Bob", "DEV", 5000, ["Python"], "senior")
        sales = Salesperson(4, "Alice", "Sales", 4000, 0.15, 50000)
        
        infos = [emp.get_info(), manager.get_info(), dev.get_info(), sales.get_info()]
        
        # Все должны быть разными
        assert len(set(infos)) == 4
