from typing import Optional, Sequence

from ..interfaces import (ContactTracer, LocationID, NoOP, PersonID,
                          PersonRoutine, PersonState, SimTime, SimTimeTuple)
from .base import BasePerson

class Worker(BasePerson):
    def __init__(
        self,
        person_id: PersonID,
        home: LocationID,
        work: LocationID,
        work_time: Optional[SimTimeTuple] = ...,
        regulation_compliance_prob: float = ...,
        init_state: Optional[PersonState] = ...,
    ) -> None: ...
    @property
    def work(self) -> LocationID: ...
    @property
    def assigned_locations(self) -> Sequence[LocationID]: ...
    @property
    def at_work(self) -> bool: ...
    def set_during_work_routines(self, routines: Sequence[PersonRoutine]) -> None: ...
    def set_outside_work_routines(self, routines: Sequence[PersonRoutine]) -> None: ...
    def step(
        self, sim_time: SimTime, contact_tracer: Optional[ContactTracer] = ...
    ) -> Optional[NoOP]: ...
    def reset(self) -> None: ...
