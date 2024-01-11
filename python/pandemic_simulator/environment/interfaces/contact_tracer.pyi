import abc
from abc import ABC, abstractmethod
from typing import Mapping

import numpy as np
from ordered_set import OrderedSet

from .ids import PersonID

class ContactTracer(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def new_time_slot(self) -> None: ...
    @abstractmethod
    def reset(self) -> None: ...
    @abstractmethod
    def add_contacts(self, contacts: OrderedSet) -> None: ...
    @abstractmethod
    def get_contacts(self, person_id: PersonID) -> Mapping[PersonID, np.ndarray]: ...
