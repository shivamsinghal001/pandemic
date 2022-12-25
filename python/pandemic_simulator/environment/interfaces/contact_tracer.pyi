import abc
import numpy as np
from .ids import PersonID
from abc import ABC, abstractmethod
from orderedset import OrderedSet
from typing import Mapping

class ContactTracer(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def new_time_slot(self) -> None: ...
    @abstractmethod
    def reset(self) -> None: ...
    @abstractmethod
    def add_contacts(self, contacts: OrderedSet) -> None: ...
    @abstractmethod
    def get_contacts(self, person_id: PersonID) -> Mapping[PersonID, np.ndarray]: ...
