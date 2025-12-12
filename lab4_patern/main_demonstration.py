import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def print_header(text):
    """Печатает заголовок раздела"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_subheader(text):
    """Печатает подзаголовок"""
    print(f"\n {text}")
    print("-" * 50)


def main():
    """Основная функция демонстрации"""
    print("\n" + "=" * 80)
    print(" ЛАБОРАТОРНАЯ РАБОТА №4: ДЕМОНСТРАЦИЯ ПАТТЕРНОВ ПРОЕКТИРОВАНИЯ")
    print("=" * 80)

    try:
        # 1 SINGLETON
      
        print_header("1. SINGLETON: Единое подключение к базе данных")

        try:
            from Paterns.creational.singleton import DatabaseConnection
            from data_base.connection import db_singleton, get_db

            print("Создаем два 'разных' экземпляра DatabaseConnection:")
            db1 = DatabaseConnection()
            db2 = DatabaseConnection.get_instance()

            print(f"   db1 id: {id(db1)}")
            print(f"   db2 id: {id(db2)}")
            print(f"   db1 is db2: {db1 is db2}")

            if db1 is db2:
                print("  Паттерн Singleton работает: создан только один экземпляр!")

            # Получаем подключение к БД
            connection = db1.get_connection()
            print(f"\nПолучено подключение к БД: {connection}")

            # Используем практическую обертку из data_base
            print("\nИспользование практической обертки из data_base:")
            db_practical = get_db()
            print(f"   Практический экземпляр: {db_practical}")

        except ImportError as e:
            print(f" Ошибка импорта Singleton: {e}")
            print("   Убедитесь, что файлы находятся в правильных директориях")
        except Exception as e:
            print(f"  Ошибка при демонстрации Singleton: {e}")


        # 2 FACTORY METHOD - создание сотрудников
        print_header("2 FACTORY METHOD: Создание объектов сотрудников")

        try:
            # Пытаемся импортировать фабрику из паттернов
            from Paterns.creational.factory_method import (
                EmployeeFactory, DeveloperFactory, ManagerFactory
            )

            print("Создаем фабрики для разных типов сотрудников:")
            dev_factory = DeveloperFactory()
            manager_factory = ManagerFactory()

            print("\nСоздание разработчика через DeveloperFactory:")
            developer = dev_factory.create_employee(
                id=101,
                name="Алексей Петров",
                department="Разработка",
                base_salary=5000,
                tech_stack=["Python", "Django", "PostgreSQL"],
                seniority_level="senior"
            )
            print(f"   Создан: {developer.name}")
            print(f"   Должность: Разработчик")
            print(f"   Навыки: {', '.join(developer.tech_stack)}")

            print("\nСоздание менеджера через ManagerFactory:")
            manager = manager_factory.create_employee(
                id=201,
                name="Мария Иванова",
                department="Менеджмент",
                base_salary=7000,
                bonus=1500
            )
            print(f"   Создан: {manager.name}")
            print(f"   Должность: Менеджер")
            print(f"   Бонус: {manager.bonus}")

        except ImportError:
            # Пробуем альтернативный импорт
            try:
                from core_OOP.Employee import Employee, Manager, Developer
                print("Используем прямое создание объектов (без Factory Method):")

                developer = Developer(
                    id_empl=101,
                    name="Алексей Петров",
                    department="Разработка",
                    base_salary=5000,
                    tech_stack=["Python", "Django"],
                    seniority_level="middle"
                )
                print(f"   Создан разработчик: {developer.name}")

            except ImportError as e:
                print(f"    Не удалось импортировать классы сотрудников: {e}")
        except Exception as e:
            print(f"  Ошибка при демонстрации Factory Method: {e}")

      
        # 3 BUILDER  - пошаговое создание сложных объектов
        print_header("3 BUILDER: Пошаговое создание сотрудников")

        try:
            from Paterns.creational.builder import EmployeeBuilder

            print("Пошаговое создание сотрудника через Builder:")

            # Используем fluent-интерфейс
            employee = (EmployeeBuilder()
                        .set_id(301)
                        .set_name("Сергей Смирнов")
                        .set_department("Тестирование")
                        .set_base_salary(4500)
                        .set_employee_type("Developer")
                        .add_skill("Python")
                        .add_skill("Pytest")
                        .add_skill("Selenium")
                        .build())

            print(f"   Создан: {employee.name}")
            print(f"   Отдел: {employee.department}")
            print(f"   Зарплата: {employee.base_salary}")

            print("\nСоздание менеджера через Builder:")
            manager = (EmployeeBuilder()
                       .set_id(302)
                       .set_name("Ольга Кузнецова")
                       .set_department("Управление проектами")
                       .set_base_salary(8000)
                       .set_employee_type("Manager")
                       .set_bonus(2000)
                       .build())

            print(f"   Создан: {manager.name}")
            print(f"   Бонус: {manager.bonus}")

        except ImportError as e:
            print(f"    Не удалось импортировать Builder: {e}")
        except Exception as e:
            print(f"  Ошибка при демонстрации Builder: {e}")

      
        # 4 STRATEGY - различные алгоритмы расчета бонусов
        print_header("4 STRATEGY: Гибкий расчет бонусов")

        try:
            from Paterns.behavioral.strategy import (
                BonusStrategy,
                PerformanceBonusStrategy,
                SeniorityBonusStrategy,
                EmployeeWithStrategy
            )

            # Создаем тестового сотрудника
            from core_OOP.Employee import Developer

            test_developer = Developer(
                id_empl=401,
                name="Дмитрий Васильев",
                department="Разработка",
                base_salary=6000,
                tech_stack=["Python", "FastAPI"],
                seniority_level="senior"
            )

            print(f"Базовый сотрудник: {test_developer.name}")
            print(f"Базовая зарплата: {test_developer.calculate_salary()}")

            # Создаем обертку со стратегией
            employee_with_strategy = EmployeeWithStrategy(test_developer)

            # Применяем разные стратегии
            print("\nПрименение разных стратегий расчета бонусов:")

            print("1. Стратегия на основе производительности:")
            employee_with_strategy.set_bonus_strategy(PerformanceBonusStrategy())
            salary_with_performance = employee_with_strategy.calculate_total_salary()
            print(f"   Итоговая зарплата: {salary_with_performance:.2f}")

            print("\n2. Стратегия на основе стажа/уровня:")
            employee_with_strategy.set_bonus_strategy(SeniorityBonusStrategy())
            salary_with_seniority = employee_with_strategy.calculate_total_salary()
            print(f"   Итоговая зарплата: {salary_with_seniority:.2f}")

            print(f"\n Разница между стратегиями: {abs(salary_with_performance - salary_with_seniority):.2f}")

        except ImportError as e:
            print(f"    Не удалось импортировать Strategy: {e}")
        except Exception as e:
            print(f"  Ошибка при демонстрации Strategy: {e}")

      
        # 5 DECORATOR  - динамическое добавление функциональности
        print_header("5 DECORATOR: Динамическое расширение возможностей")

        try:
            from Paterns.structural.decorator import (
                EmployeeDecorator,
                BonusDecorator,
                TrainingDecorator
            )
            from core_OOP.Employee import Employee

            # Создаем базового сотрудника
            base_employee = Employee(
                id_empl=501,
                name="Игорь Николаев",
                department="Поддержка",
                base_salary=4000
            )

            print(f"Базовый сотрудник: {base_employee.name}")
            print(f"Базовая зарплата: {base_employee.calculate_salary()}")

            # Динамически добавляем функциональность через декораторы
            print("\nДинамическое добавление функциональности:")

            print("1. Добавляем бонусный декоратор:")
            employee_with_bonus = BonusDecorator(base_employee, 500)
            print(f"   Зарплата с бонусом: {employee_with_bonus.calculate_salary()}")

            print("\n2. Добавляем декоратор обучения:")
            employee_with_training = TrainingDecorator(employee_with_bonus, "Курс по DevOps")
            print(f"   Информация: {employee_with_training.get_info()}")

            print("\n3. Комбинируем несколько декораторов:")
            super_employee = TrainingDecorator(
                BonusDecorator(base_employee, 1000),
                "Продвинутый Python"
            )
            print(f"   Итоговая зарплата: {super_employee.calculate_salary()}")
            print(f"   Полная информация: {super_employee.get_info()}")

        except ImportError as e:
            print(f"    Не удалось импортировать Decorator: {e}")
        except Exception as e:
            print(f"  Ошибка при демонстрации Decorator: {e}")


        # 6 OBSERVER  - система уведомлений
        print_header("6 OBSERVER: Система уведомлений об изменениях")

        try:
            from Paterns.behavioral.observer import (
                Observable,
                Observer,
                NotificationSystem,
                LoggingSystem
            )

            print("Создаем систему уведомлений и логирования:")

            # Создаем наблюдателей
            notification_system = NotificationSystem()
            logging_system = LoggingSystem()

            print("1. Созданы наблюдатели:")
            print(f"   - {notification_system.__class__.__name__}")
            print(f"   - {logging_system.__class__.__name__}")

            # Демонстрация работы наблюдателя
            print("\n2. Демонстрация работы Observer:")

            # Используем ObservableEmployee если он существует
            try:
                from Paterns.behavioral.observer import ObservableEmployee
                from core_OOP.Employee import Employee as BaseEmployee

                # Создаем наблюдаемого сотрудника
                observable_emp = ObservableEmployee(
                    id_empl=601,
                    name="Анна Семенова",
                    department="Аналитика",
                    base_salary=5500
                )

                # Добавляем наблюдателей
                observable_emp.add_observer(notification_system)
                observable_emp.add_observer(logging_system)

                print(f"   Создан наблюдаемый сотрудник: {observable_emp.name}")
                print(f"   Текущая зарплата: {observable_emp.base_salary}")

                print("\n3. Изменяем зарплату (должны прийти уведомления):")
                observable_emp.set_salary(6000)

            except ImportError:
                print("ObservableEmployee не найден, используем базовую демонстрацию")

                # Простая демонстрация
                class SimpleObservable(Observable):
                    def change_data(self, new_data):
                        self.notify_observers(f"Данные изменены на: {new_data}")

                simple_obs = SimpleObservable()
                simple_obs.add_observer(notification_system)
                simple_obs.add_observer(logging_system)

                print("\n   Тестовая отправка уведомления:")
                simple_obs.change_data("Новые настройки системы")

        except ImportError as e:
            print(f" Не удалось импортировать Observer: {e}")
        except Exception as e:
            print(f"Ошибка при демонстрации Observer: {e}")

      

        print_header("7 ИНТЕГРАЦИЯ: Взаимодействие всех паттернов")

        try:
            print("Демонстрация совместной работы паттернов:")
            print("\nСценарий: Полный цикл работы с сотрудником")

            # 1 Создаем через Builder
            print("\n1. СОЗДАНИЕ через BUILDER:")
            from Paterns.creational.builder import EmployeeBuilder
            new_employee = (EmployeeBuilder()
                            .set_id(701)
                            .set_name("Кирилл Волков")
                            .set_department("Data Science")
                            .set_base_salary(6500)
                            .set_employee_type("Developer")
                            .add_skill("Python")
                            .add_skill("Machine Learning")
                            .add_skill("SQL")
                            .build())
            print(f"   Создан: {new_employee.name}")

            # 2 Добавляем функциональность через Decorator
            print("\n2. РАСШИРЕНИЕ через DECORATOR:")
            from Paterns.structural.decorator import BonusDecorator, TrainingDecorator
            enhanced_employee = TrainingDecorator(
                BonusDecorator(new_employee, 800),
                "Курс по нейросетям"
            )
            print(f"   Общая зарплата: {enhanced_employee.calculate_salary()}")

            # 3 Применяем Strategy для расчета
            print("\n3. РАСЧЕТ через STRATEGY:")
            from Paterns.behavioral.strategy import (
                EmployeeWithStrategy,
                PerformanceBonusStrategy
            )
            strategic_employee = EmployeeWithStrategy(enhanced_employee)
            strategic_employee.set_bonus_strategy(PerformanceBonusStrategy())
            final_salary = strategic_employee.calculate_total_salary()
            print(f"   Итоговая зарплата со стратегией: {final_salary:.2f}")

            # 4 Сохраняем в БД через Singleton
            print("\n4. СОХРАНЕНИЕ через SINGLETON:")
            try:
                from data_base.connection import save_employee

                employee_data = {
                    'id': new_employee.id,
                    'name': new_employee.name,
                    'department': new_employee.department,
                    'base_salary': new_employee.base_salary,
                    'employee_type': new_employee.__class__.__name__,
                    'tech_stack': new_employee.tech_stack if hasattr(new_employee, 'tech_stack') else []
                }

                save_employee(employee_data)
                print(f"   Сотрудник сохранен в БД с ID: {new_employee.id}")

            except ImportError as e:
                print(f"       Не удалось сохранить в БД: {e}")

            print("\n  Полный цикл работы завершен успешно!")

        except Exception as e:
            print(f"    Ошибка при интеграции паттернов: {e}")


        # 8 ИСКЛЮЧЕНИЯ
        print_header("8 ОБРАБОТКА ИСКЛЮЧЕНИЙ")

        try:
            from core_OOP.exceptions import (
                EmployeeNotFoundError,
                DepartmentNotFoundError,
                DuplicateIdError
            )

            print("Демонстрация кастомных исключений:")

            exceptions_to_demo = [
                ("Сотрудник не найден", EmployeeNotFoundError(999)),
                ("Отдел не найден", DepartmentNotFoundError("Несуществующий отдел")),
                ("Дубликат ID", DuplicateIdError("Сотрудник", 123))
            ]

            for description, exception in exceptions_to_demo:
                print(f"\n - {description}:")
                print(f"  Тип: {type(exception).__name__}")
                print(f"  Сообщение: {exception}")

        except ImportError as e:
            print(f"    Не удалось импортировать исключения: {e}")
        except Exception as e:
            print(f"  Ошибка при демонстрации исключений: {e}")


        # ИТОГИ
        print_header("ИТОГИ ДЕМОНСТРАЦИИ")

        print(" Сводка по реализованным паттернам:")
        print("""
        1.   Singleton     - Единое подключение к БД
        2.   Factory Method- Создание объектов сотрудников
        3.   Builder       - Пошаговое создание сложных объектов
        4.   Strategy      - Гибкие алгоритмы расчета бонусов
        5.   Decorator     - Динамическое расширение функциональности
        6.   Observer      - Система уведомлений об изменениях
        7.   Integration   - Совместная работа паттернов
        8.   Exceptions    - Кастомная обработка ошибок
        """)

        print(" Преимущества реализованной архитектуры:")
        print(" - Гибкость и расширяемость системы")
        print(" - Чистая и поддерживаемая кодовая база")
        print(" - Повторное использование компонентов")
        print(" - Легкость тестирования")

        print("\n" + "=" * 80)
        print(" ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
        print("=" * 80)


    except Exception as e:
        print(f"\n\n  Критическая ошибка в демонстрации: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
