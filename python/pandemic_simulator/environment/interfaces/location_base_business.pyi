from abc import ABCMeta
from typing import ClassVar, Tuple, Type

from .ids import PersonID
from .location_base import BaseLocation
from .location_rules import LocationRule
from .sim_time import SimTime, SimTimeTuple

class BusinessBaseLocation(BaseLocation[_BusinessState], metaclass=ABCMeta):
    location_rule_type: Type
    def sync(self, sim_time: SimTime) -> None: ...
    def update_rules(self, new_rule: LocationRule) -> None: ...
    def get_worker_work_time(self) -> SimTimeTuple: ...

class EssentialBusinessBaseLocation(
    BusinessBaseLocation[_BusinessState], metaclass=ABCMeta
): ...

class NonEssentialBusinessBaseLocation(
    BusinessBaseLocation[_NonEssentialBusinessState], metaclass=ABCMeta
):
    location_rule_type: Type
    def sync(self, sim_time: SimTime) -> None: ...
    def update_rules(self, new_rule: LocationRule) -> None: ...

class AgeRestrictedBusinessBaseLocation(
    NonEssentialBusinessBaseLocation[_NonEssentialBusinessState], metaclass=ABCMeta
):
    age_limits: ClassVar[Tuple[int, int]]
    def is_entry_allowed(self, person_id: PersonID) -> bool: ...
