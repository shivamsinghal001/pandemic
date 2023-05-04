from typing import Optional, Sequence

from ..interfaces import (LocationID, NoOP, PersonRoutine,
                          PersonRoutineWithStatus, RoutineTrigger)
from .base import BasePerson

def execute_routines(
    person: BasePerson, routines_with_status: Sequence[PersonRoutineWithStatus]
) -> Optional[NoOP]: ...
def triggered_routine(
    start_loc: Optional[LocationID],
    end_location_type: type,
    interval_in_days: int,
    explore_probability: float = ...,
) -> PersonRoutine: ...
def weekend_routine(
    start_loc: Optional[LocationID],
    end_location_type: type,
    explore_probability: float = ...,
    reset_when_done: RoutineTrigger = ...,
) -> PersonRoutine: ...
def mid_day_during_week_routine(
    start_loc: Optional[LocationID],
    end_location_type: type,
    explore_probability: float = ...,
) -> PersonRoutine: ...
def social_routine(start_loc: Optional[LocationID]) -> PersonRoutine: ...
