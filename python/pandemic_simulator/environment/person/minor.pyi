from typing import Optional, Sequence

from ..interfaces import (ContactTracer, LocationID, NoOP, PersonID,
                          PersonRoutine, PersonState, SimTime, SimTimeTuple)
from .base import BasePerson

class Minor(BasePerson):
    def __init__(
        self,
        person_id: PersonID,
        home: LocationID,
        school: Optional[LocationID] = ...,
        school_time: Optional[SimTimeTuple] = ...,
        regulation_compliance_prob: float = ...,
        init_state: Optional[PersonState] = ...,
    ) -> None: ...
    @property
    def school(self) -> Optional[LocationID]: ...
    @property
    def assigned_locations(self) -> Sequence[LocationID]: ...
    @property
    def at_school(self) -> bool: ...
    def set_outside_school_routines(
        self, routines: Sequence[PersonRoutine]
    ) -> None: ...
    def step(
        self, sim_time: SimTime, contact_tracer: Optional[ContactTracer] = ...
    ) -> Optional[NoOP]: ...
    def reset(self) -> None: ...
