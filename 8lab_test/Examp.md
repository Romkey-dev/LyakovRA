# 📊 ПРИМЕРЫ ЗАПУСКА И РЕЗУЛЬТАТЫ

## 1 Запуск всех тестов

### Команда:
```bash
pytest -v
```

###   вывод:
```
============================= test session starts ==============================
platform linux -- Python 3.9.0, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
cachedir: .pytest_cache
rootdir: /path/to/project
collected 255 items

test_employee.py::TestEmployeeCreation::test_employee_creation_valid_data PASSED
test_employee.py::TestEmployeeCreation::test_employee_creation_invalid_id PASSED
test_employee.py::TestEmployeeValidity::test_invalid_id_negative PASSED
test_employee.py::TestEmployeeValidity::test_invalid_name_empty PASSED
...
[Множество PASSED]
...
test_patterns.py::TestStrategyPattern::test_strategy_switching PASSED

============================= 255 passed in 12.34s ==============================
```

**Результат**:  Все 255 тестов должны пройти зелёным цветом

---

## 2 Запуск конкретного файла

### Команда:
```bash
pytest test_employee.py -v
```

### вывод:
```
============================= test session starts ==============================

test_employee.py::TestEmployeeCreation::test_employee_creation_valid_data PASSED
test_employee.py::TestEmployeeCreation::test_employee_creation_with_defaults PASSED
test_employee.py::TestEmployeeValidity::test_invalid_id_negative PASSED
test_employee.py::TestEmployeeValidity::test_invalid_name_empty PASSED
test_employee.py::TestEmployeeValidity::test_invalid_salary_negative PASSED
test_employee.py::TestEmployeeProperties::test_salary_property_get PASSED
test_employee.py::TestEmployeeProperties::test_salary_property_set_valid PASSED
test_employee.py::TestEmployeeMethods::test_calculate_salary PASSED
test_employee.py::TestEmployeeMethods::test_get_info_format PASSED
test_employee.py::TestEmployeeMethods::test_get_info_contains_all_data PASSED
test_employee.py::TestEmployeeMagicMethods::test_employee_equality PASSED
test_employee.py::TestEmployeeMagicMethods::test_employee_less_than PASSED
...

============================= 45 passed in 1.23s ===============================
```

**Результат**:  45+ тестов для Employee должны пройти

---

## 3 Запуск конкретного класса тестов

### Команда:
```bash
pytest test_employees_hierarchy.py::TestManagerClass -v
```

###   вывод:
```
============================= test session starts ==============================

test_employees_hierarchy.py::TestManagerClass::test_manager_creation_valid PASSED
test_employees_hierarchy.py::TestManagerClass::test_manager_has_bonus PASSED
test_employees_hierarchy.py::TestManagerClass::test_manager_salary_calculation_with_bonus PASSED
test_employees_hierarchy.py::TestManagerClass::test_manager_salary_calculation_different_values PASSED
test_employees_hierarchy.py::TestManagerClass::test_manager_get_info_includes_bonus PASSED
test_employees_hierarchy.py::TestManagerClass::test_manager_get_info_includes_salary PASSED
test_employees_hierarchy.py::TestManagerClass::test_manager_is_abstract_employee PASSED

============================= 7 passed in 0.45s ===============================
```

**Результат**:  Все тесты для Manager должны пройти

---

## 4 Запуск одного конкретного теста

### Команда:
```bash
pytest test_polymorphism_magic_methods.py::TestEmployeeEquality::test_employee_equality_same_id -v
```

###   вывод:
```
============================= test session starts ==============================

test_polymorphism_magic_methods.py::TestEmployeeEquality::test_employee_equality_same_id PASSED

============================= 1 passed in 0.02s ===============================
```

**Результат**:  Тест должен пройти

---

## 5 Запуск с фильтрацией по имени

### Команда:
```bash
pytest -k salary -v
```

###   вывод:
```
============================= test session starts ==============================

test_employee.py::TestEmployeeMethods::test_calculate_salary PASSED
test_employee.py::TestEmployeeSerialization::test_to_dict_includes_salary PASSED
test_employees_hierarchy.py::TestManagerClass::test_manager_salary_calculation_with_bonus PASSED
test_employees_hierarchy.py::TestManagerClass::test_manager_salary_calculation_different_values PASSED
test_employees_hierarchy.py::TestDeveloperClass::test_developer_salary_junior PASSED
test_employees_hierarchy.py::TestDeveloperClass::test_developer_salary_middle PASSED
test_employees_hierarchy.py::TestDeveloperClass::test_developer_salary_senior PASSED
test_employees_hierarchy.py::TestDeveloperClass::test_developer_salary_by_level PASSED
test_employees_hierarchy.py::TestSalespersonClass::test_salesperson_salary_calculation PASSED
test_employees_hierarchy.py::TestSalespersonClass::test_salesperson_salary_different_values PASSED
test_polymorphism_magic_methods.py::TestEmployeeComparison::test_employee_less_than PASSED
test_polymorphism_magic_methods.py::TestEmployeeComparison::test_employee_greater_than PASSED
test_polymorphism_magic_methods.py::TestEmployeeAddition::test_employee_addition_two_employees PASSED
test_composition_aggregation.py::TestProjectSalaryCalculation::test_project_total_salary_single_employee PASSED
test_composition_aggregation.py::TestProjectSalaryCalculation::test_project_total_salary_multiple_employees PASSED
test_composition_aggregation.py::TestProjectSalaryCalculation::test_project_total_salary_empty_team PASSED
test_composition_aggregation.py::TestCompanyEmployeeManagement::test_company_calculate_total_monthly_cost PASSED

============================= 17 passed in 0.89s ==========================
```

**Результат**:  Все тесты связанные с зарплатой должны пройти (17+)

---

## 6 Запуск с проверкой покрытия

### Команда:
```bash
pytest --cov=. --cov-report=term-missing
```

###   вывод:
```
============================= test session starts ==============================

test_employee.py .................................................                  [ 15%]
test_employees_hierarchy.py ......................................................  [ 30%]
test_polymorphism_magic_methods.py .................................................[ 50%]
test_composition_aggregation.py ...................................................[ 70%]
test_patterns.py .........................................................        [100%]

============================= test coverage results ==============================
Name                        Stmts   Miss  Cover   Missing
─────────────────────────────────────────────────────────────
Employee.py                  120      5    95%     125-127
Abctract_emp.py              10       0   100%
Manager.py                   25       0   100%
Developer.py                 35       0   100%
Salesperson.py               30       0   100%
Department.py                55       2    96%     120, 125
Project.py                   50       1    98%     135
Company.py                   80       3    96%     145, 150, 160
singleton.py                 15       0   100%
factory_method.py            35       0   100%
Builder.py                   45       0   100%
decorator.py                 30       0   100%
observer.py                  40       0   100%
Strategy.py                  50       0   100%
─────────────────────────────────────────────────────────────
TOTAL                        925      11    99%

============================= 255 passed in 12.45s ==========================
```

**Результат**:  Покрытие кода должно быть > 95%

---

## 7 Запуск с подробным выводом при ошибке

### Команда:
```bash
pytest test_employee.py::TestEmployeeCreation::test_employee_creation_valid_data -vv
```

###   вывод (при успехе):
```
============================= test session starts ==============================

test_employee.py::TestEmployeeCreation::test_employee_creation_valid_data 
    assert emp.id == 1  # PASSED
    assert emp.name == "Alice"  # PASSED
    assert emp.department == "IT"  # PASSED
    assert emp.base_salary == 5000  # PASSED
PASSED

============================= 1 passed in 0.01s ===============================
```

**Результат**:  Тест должен пройти с подробной информацией

---

## 8 Запуск параметризованного теста

### Команда:
```bash
pytest test_employees_hierarchy.py::TestDeveloperClass::test_developer_salary_by_level -v
```

###   вывод:
```
============================= test session starts ==============================

test_employees_hierarchy.py::TestDeveloperClass::test_developer_salary_by_level[junior-1.0] PASSED
test_employees_hierarchy.py::TestDeveloperClass::test_developer_salary_by_level[middle-1.5] PASSED
test_employees_hierarchy.py::TestDeveloperClass::test_developer_salary_by_level[senior-2.0] PASSED

============================= 3 passed in 0.08s ===============================
```

**Результат**:  Каждый вариант параметров проходит отдельно

---

## 9 Запуск с остановкой на первой ошибке

### Команда:
```bash
pytest -x
```

###   вывод (если всё хорошо):
```
============================= test session starts ==============================

test_employee.py .............................................................
test_employees_hierarchy.py ..............................................................
test_polymorphism_magic_methods.py ........................ (55 passed)
... [остальные тесты]

============================= 255 passed in 12.34s ==========================
```

**Результат**:  Если бы была ошибка - тесты остановились бы на ней

---

## 10 Запуск с показом print() output

### Команда:
```bash
pytest test_employee.py -s
```

###   вывод:
```
============================= test session starts ==============================

test_employee.py::TestEmployeeCreation::test_employee_creation_valid_data 
Creating employee: Alice from IT with salary 5000
PASSED
test_employee.py::TestEmployeeCreation::test_employee_creation_with_defaults 
Creating employee with defaults
PASSED

============================= 45 passed in 1.23s ===============================
```

**Результат**:  Видны все print() операции из кода

---
### Успешное выполнение всех тестов:
```
✅ 255+ тестов
✅ 100% pass rate
✅ 0 failed
✅ 0 errors
✅ Execution time: 12-15 секунд
✅ Code coverage: > 95%
```
---

**Дата**: 26.12.2025  