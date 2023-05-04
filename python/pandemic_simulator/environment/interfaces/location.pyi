import abc
from abc import ABC, abstractmethod
from typing import ClassVar, Type

from .ids import LocationID, PersonID
from .location_rules import LocationRule
from .sim_time import SimTime

class LocationError(Exception): ...

class LocationSummary:
    entry_count: float
    visitor_count: float
    def __init__(self, entry_count, visitor_count) -> None: ...

class Location(ABC, metaclass=abc.ABCMeta):
    location_rule_type: Type
    state_type: ClassVar[Type[_State]]
    @property
    @abstractmethod
    def id(self) -> LocationID: ...
    @property
    @abstractmethod
    def state(self) -> _State: ...
    @property
    @abstractmethod
    def init_state(self) -> _State: ...
    @abstractmethod
    def sync(self, sim_time: SimTime) -> None: ...
    @abstractmethod
    def update_rules(self, new_rule: LocationRule) -> None: ...
    @abstractmethod
    def is_entry_allowed(self, person_id: PersonID) -> bool: ...
    @abstractmethod
    def assign_person(self, person_id: PersonID) -> None: ...
    @abstractmethod
    def add_person_to_location(self, person_id: PersonID) -> None: ...
    @abstractmethod
    def remove_person_from_location(self, person_id: PersonID) -> None: ...
    @abstractmethod
    def reset(self) -> None: ...
