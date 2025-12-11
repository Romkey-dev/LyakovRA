from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    """Наблюдатель"""
    
    @abstractmethod
    def update(self, message: str):
        pass


class Observable:
    """Наблюдаемый объект"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def add_observer(self, observer: Observer):
        self._observers.append(observer)
    
    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify_observers(self, message: str):
        for observer in self._observers:
            observer.update(message)


class NotificationSystem(Observer):
    """Система уведомлений"""
    
    def update(self, message: str):
        print(f"🔔 Уведомление: {message}")


class LoggingSystem(Observer):
    """Система логирования"""
    
    def update(self, message: str):
        print(f"📝 Лог: {message}")
