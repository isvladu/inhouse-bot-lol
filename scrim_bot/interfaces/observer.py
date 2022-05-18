from __future__ import annotations
from abc import ABC, abstractmethod


class Subject(ABC):
    """
    Subject interface that declares a set of method for managing subscribers.
    """
    
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attaches an observer to the subject.
        """
        pass
        
    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Detaches an observer from the subject.
        """
        pass
        
    @abstractmethod
    def notify(self) -> None:
        """
        Notifies all observers about an event.
        """
        pass
    
class Observer(ABC):
    """
    Observer interface that declared an update method, used by subjects.
    """
    
    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Receive an update from the subject.
        """
        pass