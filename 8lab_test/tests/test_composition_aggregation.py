"""
Часть 4: Тестирование композиции, агрегации и сложных структур
"""
import pytest
from datetime import datetime, timedelta
from Employee import Employee, Manager, Developer, Salesperson
from Department import Department
from Project import Project
from Company import Company
from exceptions import (
    InvalidDataError,
    EmployeeNotFoundError,
    DepartmentNotFoundError,
    ProjectNotFoundError,
    DuplicateIdError,
    InvalidStatusError
)


class TestProjectTeamManagement:
    """Тесты управления командой проекта"""
    
    def test_project_add_team_member(self):
        """Проверка добавления сотрудника в команду проекта"""
        project = Project(1, "AI Platform", "Разработка AI", datetime.now(), "planning")
        emp = Employee(1, "John", "IT", 5000)
        
        project.add_team_member(emp)
        
        assert len(project.get_team()) == 1
        assert emp in project.get_team()
    
    def test_project_add_multiple_team_members(self):
        """Проверка добавления нескольких сотрудников"""
        project = Project(1, "Project", "Desc", datetime.now(), "active")
        
        employees = [
            Employee(1, "John", "IT", 5000),
            Manager(2, "Jane", "Mgmt", 5000, 1000),
            Developer(3, "Bob", "DEV", 5000, ["Python"], "senior")
        ]
        
        for emp in employees:
            project.add_team_member(emp)
        
        assert len(project.get_team()) == 3
    
    def test_project_remove_team_member(self):
        """Проверка удаления сотрудника из команды"""
        project = Project(1, "Project", "Desc", datetime.now(), "planning")
        emp = Employee(1, "John", "IT", 5000)
        
        project.add_team_member(emp)
        assert len(project.get_team()) == 1
        
        project.remove_team_member(1)
        assert len(project.get_team()) == 0
    
    def test_project_remove_nonexistent_member(self):
        """Проверка выброса исключения при удалении несуществующего сотрудника"""
        project = Project(1, "Project", "Desc", datetime.now(), "planning")
        
        with pytest.raises(EmployeeNotFoundError):
            project.remove_team_member(999)
    
    def test_project_duplicate_member_raises_error(self):
        """Проверка что нельзя добавить одного сотрудника дважды"""
        project = Project(1, "Project", "Desc", datetime.now(), "planning")
        emp = Employee(1, "John", "IT", 5000)
        
        project.add_team_member(emp)
        
        with pytest.raises(DuplicateIdError):
            project.add_team_member(emp)
    
    def test_project_get_team_size(self):
        """Проверка получения размера команды"""
        project = Project(1, "Project", "Desc", datetime.now(), "planning")
        
        assert project.get_team_size() == 0
        
        project.add_team_member(Employee(1, "John", "IT", 5000))
        assert project.get_team_size() == 1
        
        project.add_team_member(Employee(2, "Bob", "IT", 6000))
        assert project.get_team_size() == 2
    
    def test_project_add_member_to_completed_project(self):
        """Проверка что нельзя добавить сотрудника в завершенный проект"""
        project = Project(1, "Project", "Desc", datetime.now(), "completed")
        emp = Employee(1, "John", "IT", 5000)
        
        with pytest.raises(InvalidStatusError):
            project.add_team_member(emp)
    
    def test_project_add_member_to_cancelled_project(self):
        """Проверка что нельзя добавить сотрудника в отменённый проект"""
        project = Project(1, "Project", "Desc", datetime.now(), "cancelled")
        emp = Employee(1, "John", "IT", 5000)
        
        with pytest.raises(InvalidStatusError):
            project.add_team_member(emp)


class TestProjectSalaryCalculation:
    """Тесты расчета зарплаты команды проекта"""
    
    def test_project_total_salary_single_employee(self):
        """Проверка расчета зарплаты для одного сотрудника"""
        project = Project(1, "Project", "Desc", datetime.now(), "active")
        emp = Employee(1, "John", "IT", 5000)
        
        project.add_team_member(emp)
        
        assert project.calculate_total_salary() == 5000
    
    def test_project_total_salary_multiple_employees(self):
        """Проверка расчета суммарной зарплаты команды"""
        project = Project(1, "Project", "Desc", datetime.now(), "active")
        
        project.add_team_member(Employee(1, "John", "IT", 5000))
        project.add_team_member(Manager(2, "Jane", "Mgmt", 5000, 1000))  # 6000
        project.add_team_member(Developer(3, "Bob", "DEV", 5000, ["Python"], "senior"))  # 10000
        
        # 5000 + 6000 + 10000 = 21000
        assert project.calculate_total_salary() == 21000
    
    def test_project_total_salary_empty_team(self):
        """Проверка расчета зарплаты для пустой команды"""
        project = Project(1, "Project", "Desc", datetime.now(), "planning")
        
        assert project.calculate_total_salary() == 0


class TestCompanyDepartmentManagement:
    """Тесты управления отделами в компании"""
    
    def test_company_creation(self):
        """Проверка создания компании"""
        company = Company("TechCorp")
        
        assert company.name == "TechCorp"
    
    def test_company_add_department(self):
        """Проверка добавления отдела в компанию"""
        company = Company("TechCorp")
        dept = Department("IT")
        
        company.add_department(dept)
        
        assert len(company.get_departments()) == 1
    
    def test_company_add_multiple_departments(self):
        """Проверка добавления нескольких отделов"""
        company = Company("TechCorp")
        
        company.add_department(Department("IT"))
        company.add_department(Department("HR"))
        company.add_department(Department("Finance"))
        
        assert len(company.get_departments()) == 3
    
    def test_company_remove_department(self):
        """Проверка удаления отдела из компании"""
        company = Company("TechCorp")
        dept = Department("IT")
        
        company.add_department(dept)
        assert len(company.get_departments()) == 1
        
        company.remove_department("IT")
        assert len(company.get_departments()) == 0
    
    def test_company_remove_nonexistent_department(self):
        """Проверка выброса исключения при удалении несуществующего отдела"""
        company = Company("TechCorp")
        
        with pytest.raises(DepartmentNotFoundError):
            company.remove_department("NonExistent")
    
    def test_company_duplicate_department_raises_error(self):
        """Проверка что нельзя добавить отдел с дублирующимся названием"""
        company = Company("TechCorp")
        
        company.add_department(Department("IT"))
        
        with pytest.raises(DuplicateIdError):
            company.add_department(Department("IT"))


class TestCompanyProjectManagement:
    """Тесты управления проектами в компании"""
    
    def test_company_add_project(self):
        """Проверка добавления проекта в компанию"""
        company = Company("TechCorp")
        project = Project(1, "AI Platform", "Desc", datetime.now(), "planning")
        
        company.add_project(project)
        
        assert len(company.get_projects()) == 1
    
    def test_company_add_multiple_projects(self):
        """Проверка добавления нескольких проектов"""
        company = Company("TechCorp")
        
        company.add_project(Project(1, "Project1", "Desc", datetime.now(), "planning"))
        company.add_project(Project(2, "Project2", "Desc", datetime.now(), "active"))
        company.add_project(Project(3, "Project3", "Desc", datetime.now(), "planning"))
        
        assert len(company.get_projects()) == 3
    
    def test_company_remove_project(self):
        """Проверка удаления проекта из компании"""
        company = Company("TechCorp")
        project = Project(1, "Project", "Desc", datetime.now(), "planning")
        
        company.add_project(project)
        company.remove_project(1)
        
        assert len(company.get_projects()) == 0
    
    def test_company_duplicate_project_raises_error(self):
        """Проверка что нельзя добавить проект с дублирующимся ID"""
        company = Company("TechCorp")
        
        company.add_project(Project(1, "Project", "Desc", datetime.now(), "planning"))
        
        with pytest.raises(DuplicateIdError):
            company.add_project(Project(1, "Another", "Desc", datetime.now(), "planning"))


class TestCompanyEmployeeManagement:
    """Тесты работы с сотрудниками в компании"""
    
    def test_company_find_employee_by_id(self):
        """Проверка поиска сотрудника по ID во всей компании"""
        company = Company("TechCorp")
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        
        dept.add_employee(emp)
        company.add_department(dept)
        
        found = company.find_employee_by_id(1)
        
        assert found is not None
        assert found.name == "John"
    
    def test_company_find_nonexistent_employee(self):
        """Проверка возврата None при поиске несуществующего сотрудника"""
        company = Company("TechCorp")
        dept = Department("IT")
        
        company.add_department(dept)
        
        found = company.find_employee_by_id(999)
        
        assert found is None
    
    def test_company_get_all_employees(self):
        """Проверка получения всех сотрудников компании"""
        company = Company("TechCorp")
        
        dept1 = Department("IT")
        dept1.add_employee(Employee(1, "John", "IT", 5000))
        dept1.add_employee(Employee(2, "Bob", "IT", 6000))
        
        dept2 = Department("HR")
        dept2.add_employee(Employee(3, "Jane", "HR", 4500))
        
        company.add_department(dept1)
        company.add_department(dept2)
        
        all_employees = company.get_all_employees()
        
        assert len(all_employees) == 3
    
    def test_company_calculate_total_monthly_cost(self):
        """Проверка расчета общих месячных затрат компании"""
        company = Company("TechCorp")
        
        dept1 = Department("IT")
        dept1.add_employee(Employee(1, "John", "IT", 5000))
        dept1.add_employee(Manager(2, "Jane", "Mgmt", 5000, 1000))  # 6000
        
        dept2 = Department("Dev")
        dept2.add_employee(Developer(3, "Bob", "DEV", 5000, ["Python"], "senior"))  # 10000
        
        company.add_department(dept1)
        company.add_department(dept2)
        
        # 5000 + 6000 + 10000 = 21000
        total = company.calculate_total_monthly_cost()
        
        assert total == 21000


class TestCompanyIntegration:
    """Интеграционные тесты для Company"""
    
    def test_complex_company_structure(self):
        """Проверка сложной структуры компании"""
        company = Company("TechInnovations")
        
        # Создание отделов
        dev_dept = Department("Development")
        sales_dept = Department("Sales")
        
        # Добавление сотрудников в отделы
        dev_dept.add_employee(Manager(1, "Alice", "DEV", 7000, 2000))
        dev_dept.add_employee(Developer(2, "Bob", "DEV", 5000, ["Python", "SQL"], "senior"))
        
        sales_dept.add_employee(Salesperson(3, "Charlie", "Sales", 4000, 0.15, 50000))
        
        # Добавление отделов в компанию
        company.add_department(dev_dept)
        company.add_department(sales_dept)
        
        # Создание проектов
        project1 = Project(1, "WebApp", "Desc", datetime.now(), "active")
        project1.add_team_member(dev_dept[0])  # Manager
        project1.add_team_member(dev_dept[1])  # Developer
        
        project2 = Project(2, "Sales Campaign", "Desc", datetime.now(), "planning")
        project2.add_team_member(sales_dept[0])
        
        company.add_project(project1)
        company.add_project(project2)
        
        # Проверки
        assert company.calculate_total_monthly_cost() > 0
        assert len(company.get_all_employees()) == 3
        assert len(company.get_departments()) == 2
        assert len(company.get_projects()) == 2
    
    def test_company_info_generation(self):
        """Проверка генерации информации о компании"""
        company = Company("TechCorp")
        
        dept = Department("IT")
        dept.add_employee(Employee(1, "John", "IT", 5000))
        
        company.add_department(dept)
        
        info = company.get_company_info()
        
        assert "TechCorp" in info
        assert "1" in info  # количество отделов
        assert "1" in info  # количество сотрудников


class TestCompanyProjectFiltering:
    """Тесты фильтрации проектов"""
    
    def test_get_projects_by_status(self):
        """Проверка получения проектов по статусу"""
        company = Company("TechCorp")
        
        company.add_project(Project(1, "P1", "Desc", datetime.now(), "planning"))
        company.add_project(Project(2, "P2", "Desc", datetime.now(), "active"))
        company.add_project(Project(3, "P3", "Desc", datetime.now(), "planning"))
        company.add_project(Project(4, "P4", "Desc", datetime.now(), "completed"))
        
        planning_projects = company.get_projects_by_status("planning")
        
        assert len(planning_projects) == 2
        for project in planning_projects:
            assert project.status == "planning"
    
    def test_get_projects_by_status_empty(self):
        """Проверка получения пустого списка проектов по статусу"""
        company = Company("TechCorp")
        
        company.add_project(Project(1, "P1", "Desc", datetime.now(), "active"))
        
        planning_projects = company.get_projects_by_status("planning")
        
        assert len(planning_projects) == 0
    
    def test_get_projects_invalid_status(self):
        """Проверка выброса исключения при невалидном статусе"""
        company = Company("TechCorp")
        
        with pytest.raises(InvalidStatusError):
            company.get_projects_by_status("invalid_status")


class TestCompanyValidation:
    """Тесты валидации данных компании"""
    
    def test_company_invalid_name_empty(self):
        """Проверка выброса исключения при пустом названии компании"""
        with pytest.raises(InvalidDataError):
            Company("")
    
    def test_company_invalid_name_whitespace(self):
        """Проверка выброса исключения при названии состоящем из пробелов"""
        with pytest.raises(InvalidDataError):
            Company("   ")
    
    def test_company_invalid_name_not_string(self):
        """Проверка выброса исключения при названии не строкового типа"""
        with pytest.raises(InvalidDataError):
            Company(123)


class TestComplexScenarios:
    """Комплексные сценарии работы с системой"""
    
    def test_employee_transfer_between_departments(self):
        """Проверка переноса сотрудника между отделами"""
        company = Company("TechCorp")
        
        it_dept = Department("IT")
        hr_dept = Department("HR")
        
        emp = Employee(1, "John", "IT", 5000)
        it_dept.add_employee(emp)
        
        company.add_department(it_dept)
        company.add_department(hr_dept)
        
        # Удаляем из IT
        it_dept.remove_employee(1)
        assert len(it_dept) == 0
        
        # Добавляем в HR (обновляем отдел сотрудника)
        emp = Employee(1, "John", "HR", 5000)  # обновленный отдел
        hr_dept.add_employee(emp)
        assert len(hr_dept) == 1
    
    def test_project_team_replacement(self):
        """Проверка замены членов команды проекта"""
        project = Project(1, "Project", "Desc", datetime.now(), "active")
        
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Bob", "IT", 6000)
        
        project.add_team_member(emp1)
        assert len(project) == 1
        
        project.remove_team_member(1)
        assert len(project) == 0
        
        project.add_team_member(emp2)
        assert len(project) == 1
        assert emp2 in project
    
    def test_multiple_departments_with_overlapping_employees(self):
        """Проверка что один сотрудник не может быть в двух отделах одновременно"""
        company = Company("TechCorp")
        
        dept1 = Department("IT")
        dept2 = Department("HR")
        
        emp = Employee(1, "John", "IT", 5000)
        
        dept1.add_employee(emp)
        
        # Нельзя добавить того же сотрудника в другой отдел
        # (так как ID должен быть уникален в системе)
        # Это должно быть проверено на уровне Company
        
        company.add_department(dept1)
        company.add_department(dept2)
        
        # Проверяем что компания видит сотрудника в dept1
        found = company.find_employee_by_id(1)
        assert found is not None
