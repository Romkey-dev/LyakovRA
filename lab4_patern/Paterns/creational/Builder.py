class EmployeeBuilder:
    """Для пошагового создания сотрудников"""
    
    def __init__(self):
        self.id = None
        self.name = None
        self.department = None
        self.base_salary = None
        self.employee_type = "Employee"
        self.bonus = 0
        self.tech_stack = []
        self.seniority_level = "junior"
    
    def set_id(self, id):
        self.id = id
        return self
    
    def set_name(self, name):
        self.name = name
        return self
    
    def set_department(self, department):
        self.department = department
        return self
    
    def set_base_salary(self, salary):
        self.base_salary = salary
        return self
    
    def set_employee_type(self, emp_type):
        self.employee_type = emp_type
        return self
    
    def set_bonus(self, bonus):
        self.bonus = bonus
        return self
    
    def add_skill(self, skill):
        self.tech_stack.append(skill)
        return self
    
    def build(self):
        # Возвращаем соответствующий объект
        from core_OOP.Employee import Employee, Manager, Developer
        
        if self.employee_type == "Manager":
            return Manager(
                id_empl=self.id,
                name=self.name,
                department=self.department,
                base_salary=self.base_salary,
                bonus=self.bonus
            )
        elif self.employee_type == "Developer":
            return Developer(
                id_empl=self.id,
                name=self.name,
                department=self.department,
                base_salary=self.base_salary,
                tech_stack=self.tech_stack,
                seniority_level=self.seniority_level
            )
        else:
            return Employee(
                id_empl=self.id,
                name=self.name,
                department=self.department,
                base_salary=self.base_salary
            )
    
    print(f"Создан через Builder: {developer.name}")
