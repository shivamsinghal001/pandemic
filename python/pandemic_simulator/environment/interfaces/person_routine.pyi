import enum
from abc import ABCMeta, abstractmethod
from typing import Optional, Sequence, Type, Union

from .ids import LocationID
from .location import Location
from .person import Person, PersonState
from .sim_time import SimTime, SimTimeInterval, SimTimeTuple

class SpecialEndLoc(enum.Enum):
    social: int

class RoutineTrigger(metaclass=ABCMeta):
    @abstractmethod
    def trigger(
        self, sim_time: SimTime, person_state: Optional[PersonState] = ...
    ) -> bool: ...

class SimTimeRoutineTrigger(RoutineTrigger, SimTimeInterval):
    def trigger(
        self, sim_time: SimTime, person_state: Optional[PersonState] = ...
    ) -> bool: ...

class PersonRoutine:
    start_loc: Optional[LocationID]
    end_loc: Union[LocationID, SpecialEndLoc]
    valid_time: SimTimeTuple
    start_trigger: RoutineTrigger
    start_hour_probability: float
    explorable_end_locs: Sequence[LocationID]
    explore_probability: float
    duration_of_stay_at_end_loc: int
    reset_when_done_trigger: RoutineTrigger
    def __init__(
        self,
        start_loc,
        end_loc,
        valid_time,
        start_trigger,
        start_hour_probability,
        explorable_end_locs,
        explore_probability,
        duration_of_stay_at_end_loc,
        reset_when_done_trigger,
    ) -> None: ...

class PersonRoutineWithStatus:
    routine: PersonRoutine
    due: bool
    started: bool
    duration: int
    done: bool
    end_loc_selected: Optional[LocationID]
    def sync(
        self, sim_time: SimTime, person_state: Optional[PersonState] = ...
    ) -> None: ...
    def reset(self) -> None: ...
    def __init__(
        self, routine, due, started, duration, done, end_loc_selected
    ) -> None: ...

class PersonRoutineAssignment(metaclass=ABCMeta):
    @property
    @abstractmethod
    def required_location_types(self) -> Sequence[Type[Location]]: ...
    @abstractmethod
    def assign_routines(self, persons: Sequence[Person]) -> None: ...
    def __call__(self, persons: Sequence[Person]) -> None: ...
