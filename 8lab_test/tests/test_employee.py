"""
Часть 1: Тестирование инкапсуляции и базового класса Employee
"""
import pytest
from Employee import Employee
from Abctract_emp import AbstractEmployee
from exceptions import InvalidDataError, FinancialValidationError, DuplicateIdError


class TestEmployeeCreation:
    """Тесты создания и инициализации сотрудника"""
    
    def test_employee_creation_valid_data(self):
        """Проверка корректной инициализации сотрудника с валидными данными"""
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Assert
        assert emp.id == 1
        assert emp.name == "Alice"
        assert emp.department == "IT"
        assert emp.base_salary == 5000
    
    def test_employee_creation_multiple(self):
        """Проверка создания нескольких сотрудников с разными данными"""
        # Arrange & Act
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(2, "Bob", "HR", 4500)
        emp3 = Employee(3, "Charlie", "Finance", 6000)
        
        # Assert
        assert emp1.id == 1
        assert emp2.id == 2
        assert emp3.id == 3
        assert emp1.name != emp2.name


class TestEmployeeValidation:
    """Тесты валидации данных при создании и изменении"""
    
    def test_employee_invalid_id_negative(self):
        """Проверка выброса исключения при отрицательном ID"""
        with pytest.raises(InvalidDataError):
            Employee(-1, "Alice", "IT", 5000)
    
    def test_employee_invalid_id_zero(self):
        """Проверка выброса исключения при ID равном нулю"""
        with pytest.raises(InvalidDataError):
            Employee(0, "Alice", "IT", 5000)
    
    def test_employee_invalid_id_not_int(self):
        """Проверка выброса исключения при ID не целого числа"""
        with pytest.raises(InvalidDataError):
            Employee("abc", "Alice", "IT", 5000)
    
    def test_employee_invalid_name_empty(self):
        """Проверка выброса исключения при пустом имени"""
        with pytest.raises(InvalidDataError):
            Employee(1, "", "IT", 5000)
    
    def test_employee_invalid_name_whitespace(self):
        """Проверка выброса исключения при имени состоящем только из пробелов"""
        with pytest.raises(InvalidDataError):
            Employee(1, "   ", "IT", 5000)
    
    def test_employee_invalid_name_not_string(self):
        """Проверка выброса исключения при имени не строкового типа"""
        with pytest.raises(InvalidDataError):
            Employee(1, 123, "IT", 5000)
    
    def test_employee_invalid_department_empty(self):
        """Проверка выброса исключения при пустом названии отдела"""
        with pytest.raises(InvalidDataError):
            Employee(1, "Alice", "", 5000)
    
    def test_employee_invalid_department_whitespace(self):
        """Проверка выброса исключения при отделе состоящем только из пробелов"""
        with pytest.raises(InvalidDataError):
            Employee(1, "Alice", "   ", 5000)
    
    def test_employee_invalid_salary_negative(self):
        """Проверка выброса исключения при отрицательной зарплате"""
        with pytest.raises(FinancialValidationError):
            Employee(1, "Alice", "IT", -5000)
    
    def test_employee_invalid_salary_zero(self):
        """Проверка выброса исключения при нулевой зарплате"""
        with pytest.raises(FinancialValidationError):
            Employee(1, "Alice", "IT", 0)
    
    def test_employee_invalid_salary_not_number(self):
        """Проверка выброса исключения при зарплате не числового типа"""
        with pytest.raises(FinancialValidationError):
            Employee(1, "Alice", "IT", "5000")


class TestEmployeeProperties:
    """Тесты свойств (properties) сотрудника"""
    
    def test_employee_id_property_getter(self):
        """Проверка получения ID через property"""
        emp = Employee(1, "Alice", "IT", 5000)
        assert emp.id == 1
    
    def test_employee_name_property_getter(self):
        """Проверка получения имени через property"""
        emp = Employee(1, "Alice", "IT", 5000)
        assert emp.name == "Alice"
    
    def test_employee_department_property_getter(self):
        """Проверка получения отдела через property"""
        emp = Employee(1, "Alice", "IT", 5000)
        assert emp.department == "IT"
    
    def test_employee_base_salary_property_getter(self):
        """Проверка получения базовой зарплаты через property"""
        emp = Employee(1, "Alice", "IT", 5000)
        assert emp.base_salary == 5000
    
    def test_employee_id_property_setter_valid(self):
        """Проверка установки ID через setter с валидными данными"""
        emp = Employee(1, "Alice", "IT", 5000)
        emp.id = 2
        assert emp.id == 2
    
    def test_employee_id_property_setter_invalid(self):
        """Проверка выброса исключения при установке невалидного ID"""
        emp = Employee(1, "Alice", "IT", 5000)
        with pytest.raises(InvalidDataError):
            emp.id = -1
    
    def test_employee_name_property_setter_valid(self):
        """Проверка установки имени через setter с валидными данными"""
        emp = Employee(1, "Alice", "IT", 5000)
        emp.name = "Bob"
        assert emp.name == "Bob"
    
    def test_employee_name_property_setter_invalid(self):
        """Проверка выброса исключения при установке пустого имени"""
        emp = Employee(1, "Alice", "IT", 5000)
        with pytest.raises(InvalidDataError):
            emp.name = ""
    
    def test_employee_department_property_setter_valid(self):
        """Проверка установки отдела через setter с валидными данными"""
        emp = Employee(1, "Alice", "IT", 5000)
        emp.department = "HR"
        assert emp.department == "HR"
    
    def test_employee_department_property_setter_invalid(self):
        """Проверка выброса исключения при установке пустого отдела"""
        emp = Employee(1, "Alice", "IT", 5000)
        with pytest.raises(InvalidDataError):
            emp.department = ""
    
    def test_employee_base_salary_property_setter_valid(self):
        """Проверка установки зарплаты через setter с валидными данными"""
        emp = Employee(1, "Alice", "IT", 5000)
        emp.base_salary = 6000
        assert emp.base_salary == 6000
    
    def test_employee_base_salary_property_setter_invalid(self):
        """Проверка выброса исключения при установке отрицательной зарплаты"""
        emp = Employee(1, "Alice", "IT", 5000)
        with pytest.raises(FinancialValidationError):
            emp.base_salary = -1000
    
    def test_employee_base_salary_with_float(self):
        """Проверка использования float для зарплаты"""
        emp = Employee(1, "Alice", "IT", 5000.5)
        assert emp.base_salary == 5000.5


class TestEmployeeStringRepresentation:
    """Тесты строкового представления сотрудника"""
    
    def test_employee_str_representation(self):
        """Проверка строкового представления объекта"""
        emp = Employee(1, "Alice", "IT", 5000)
        result = str(emp)
        
        expected = "Сотрудник [id: 1, имя: Alice, отдел: IT, базовая зарплата: 5000]"
        assert result == expected
    
    def test_employee_str_contains_id(self):
        """Проверка наличия ID в строковом представлении"""
        emp = Employee(42, "Alice", "IT", 5000)
        assert "42" in str(emp)
    
    def test_employee_str_contains_name(self):
        """Проверка наличия имени в строковом представлении"""
        emp = Employee(1, "TestName", "IT", 5000)
        assert "TestName" in str(emp)
    
    def test_employee_str_contains_department(self):
        """Проверка наличия отдела в строковом представлении"""
        emp = Employee(1, "Alice", "TestDept", 5000)
        assert "TestDept" in str(emp)
    
    def test_employee_str_contains_salary(self):
        """Проверка наличия зарплаты в строковом представлении"""
        emp = Employee(1, "Alice", "IT", 7500)
        assert "7500" in str(emp)


class TestEmployeeCalculateSalary:
    """Тесты расчета зарплаты"""
    
    def test_employee_calculate_salary_base(self):
        """Проверка что зарплата обычного сотрудника равна базовой зарплате"""
        emp = Employee(1, "Alice", "IT", 5000)
        salary = emp.calculate_salary()
        assert salary == 5000
    
    def test_employee_calculate_salary_different_values(self):
        """Проверка расчета зарплаты для разных значений"""
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(2, "Bob", "HR", 4500)
        emp3 = Employee(3, "Charlie", "Finance", 6000)
        
        assert emp1.calculate_salary() == 5000
        assert emp2.calculate_salary() == 4500
        assert emp3.calculate_salary() == 6000
    
    def test_employee_calculate_salary_after_modification(self):
        """Проверка расчета зарплаты после изменения базовой зарплаты"""
        emp = Employee(1, "Alice", "IT", 5000)
        emp.base_salary = 6000
        assert emp.calculate_salary() == 6000


class TestEmployeeGetInfo:
    """Тесты получения информации о сотруднике"""
    
    def test_employee_get_info(self):
        """Проверка получения полной информации о сотруднике"""
        emp = Employee(1, "Alice", "IT", 5000)
        info = emp.get_info()
        
        # Проверяем что информация содержит необходимые поля
        assert "Alice" in info
        assert "IT" in info
        assert "5000" in info
    
    def test_employee_get_info_includes_str(self):
        """Проверка что get_info включает результат __str__"""
        emp = Employee(1, "Alice", "IT", 5000)
        info = emp.get_info()
        str_repr = str(emp)
        
        assert str_repr in info
    
    def test_employee_get_info_includes_salary(self):
        """Проверка что get_info включает рассчитанную зарплату"""
        emp = Employee(1, "Alice", "IT", 5000)
        info = emp.get_info()
        salary = emp.calculate_salary()
        
        assert str(salary) in info


class TestEmployeeSerialization:
    """Тесты сериализации и десериализации"""
    
    def test_employee_to_dict(self):
        """Проверка конвертации сотрудника в словарь"""
        emp = Employee(1, "Alice", "IT", 5000)
        data = emp.to_dict()
        
        assert data['id'] == 1
        assert data['name'] == "Alice"
        assert data['department'] == "IT"
        assert data['base_salary'] == 5000
        assert data['type'] == "Employee"
    
    def test_employee_to_dict_all_fields(self):
        """Проверка наличия всех полей в словаре"""
        emp = Employee(1, "Alice", "IT", 5000)
        data = emp.to_dict()
        
        required_fields = ['type', 'id', 'name', 'department', 'base_salary']
        for field in required_fields:
            assert field in data
    
    def test_employee_from_dict(self):
        """Проверка создания сотрудника из словаря"""
        data = {
            'id': 1,
            'name': "Alice",
            'department': "IT",
            'base_salary': 5000
        }
        emp = Employee.from_dict(data)
        
        assert emp.id == 1
        assert emp.name == "Alice"
        assert emp.department == "IT"
        assert emp.base_salary == 5000
    
    def test_employee_from_dict_missing_field(self):
        """Проверка выброса исключения при отсутствии обязательного поля"""
        data = {
            'id': 1,
            'name': "Alice",
            # missing department and base_salary
        }
        with pytest.raises(InvalidDataError):
            Employee.from_dict(data)
    
    def test_employee_from_dict_invalid_id_type(self):
        """Проверка выброса исключения при неверном типе ID"""
        data = {
            'id': "abc",  # should be int
            'name': "Alice",
            'department': "IT",
            'base_salary': 5000
        }
        with pytest.raises(InvalidDataError):
            Employee.from_dict(data)
    
    def test_employee_serialization_roundtrip(self):
        """Проверка полного цикла сериализации и десериализации"""
        original = Employee(1, "Alice", "IT", 5000)
        
        # Serialize
        data = original.to_dict()
        
        # Deserialize
        restored = Employee.from_dict(data)
        
        # Verify
        assert restored.id == original.id
        assert restored.name == original.name
        assert restored.department == original.department
        assert restored.base_salary == original.base_salary


class TestEmployeeMagicMethods:
    """Тесты перегруженных операторов и магических методов"""
    
    def test_employee_equality_same_id(self):
        """Проверка равенства сотрудников с одинаковым ID"""
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(1, "Bob", "HR", 6000)
        
        assert emp1 == emp2
    
    def test_employee_inequality_different_id(self):
        """Проверка неравенства сотрудников с разными ID"""
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 5000)
        
        assert emp1 != emp2
    
    def test_employee_less_than_comparison(self):
        """Проверка оператора < для сравнения по зарплате"""
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 6000)
        
        assert emp1 < emp2
    
    def test_employee_greater_than_comparison(self):
        """Проверка оператора > для сравнения по зарплате"""
        emp1 = Employee(1, "Alice", "IT", 6000)
        emp2 = Employee(2, "Bob", "IT", 5000)
        
        assert emp1 > emp2
    
    def test_employee_addition_two_employees(self):
        """Проверка сложения двух сотрудников (возвращает сумму зарплат)"""
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 6000)
        
        result = emp1 + emp2
        assert result == 11000
    
    def test_employee_addition_with_number(self):
        """Проверка сложения сотрудника и числа"""
        emp = Employee(1, "Alice", "IT", 5000)
        
        result = emp + 1000
        assert result == 6000
    
    def test_employee_radd_with_number(self):
        """Проверка обратного сложения (число + сотрудник)"""
        emp = Employee(1, "Alice", "IT", 5000)
        
        result = 1000 + emp
        assert result == 6000
    
    def test_employee_sum_in_list(self):
        """Проверка суммирования зарплат в списке через sum()"""
        employees = [
            Employee(1, "Alice", "IT", 5000),
            Employee(2, "Bob", "IT", 6000),
            Employee(3, "Charlie", "IT", 7000)
        ]
        
        total = sum([emp.calculate_salary() for emp in employees])
        assert total == 18000


class TestEmployeeIntegration:
    """Интеграционные тесты"""
    
    def test_employee_full_workflow(self):
        """Проверка полного рабочего процесса с сотрудником"""
        # Создание
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Проверка инициализации
        assert emp.id == 1
        assert emp.name == "Alice"
        
        # Модификация
        emp.name = "Alicia"
        emp.base_salary = 6000
        
        # Проверка модификации
        assert emp.name == "Alicia"
        assert emp.calculate_salary() == 6000
        
        # Сериализация
        data = emp.to_dict()
        assert data['name'] == "Alicia"
        
        # Десериализация
        new_emp = Employee.from_dict(data)
        assert new_emp.name == "Alicia"
        assert new_emp.calculate_salary() == 6000
    
    def test_employee_get_all_method(self):
        """Проверка метода get_all возвращающего все параметры"""
        emp = Employee(5, "Bob", "HR", 4500)
        all_data = emp.get_all()
        
        assert all_data == (5, "Bob", "HR", 4500)
    
    def test_employee_multiple_operations(self):
        """Проверка выполнения множества операций подряд"""
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Множественные операции
        emp.base_salary = 6000
        assert emp.calculate_salary() == 6000
        
        emp.department = "Finance"
        assert emp.department == "Finance"
        
        emp.name = "Alicia"
        assert emp.name == "Alicia"
        
        # Проверка консистентности
        assert emp.id == 1
        assert emp.calculate_salary() == 6000


class TestEmployeeIsAbstractEmployee:
    """Проверка что Employee наследует AbstractEmployee"""
    
    def test_employee_is_instance_of_abstract_employee(self):
        """Проверка что Employee это подкласс AbstractEmployee"""
        emp = Employee(1, "Alice", "IT", 5000)
        assert isinstance(emp, AbstractEmployee)
    
    def test_employee_implements_required_methods(self):
        """Проверка что Employee реализует все требуемые методы"""
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Проверяем наличие методов
        assert hasattr(emp, 'calculate_salary')
        assert hasattr(emp, 'get_info')
        assert hasattr(emp, 'to_dict')
        assert hasattr(emp, 'from_dict')
        
        # Проверяем что методы работают
        assert callable(emp.calculate_salary)
        assert callable(emp.get_info)
        assert callable(emp.to_dict)
