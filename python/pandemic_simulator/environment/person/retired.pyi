from typing import Optional, Sequence

from ..interfaces import (ContactTracer, LocationID, NoOP, PersonID,
                          PersonRoutine, PersonState, SimTime)
from .base import BasePerson

class Retired(BasePerson):
    def __init__(
        self,
        person_id: PersonID,
        home: LocationID,
        regulation_compliance_prob: float = ...,
        init_state: Optional[PersonState] = ...,
    ) -> None: ...
    def set_routines(self, routines: Sequence[PersonRoutine]) -> None: ...
    def step(
        self, sim_time: SimTime, contact_tracer: Optional[ContactTracer] = ...
    ) -> Optional[NoOP]: ...
    def reset(self) -> None: ...
