from typing import List, Optional, Sequence

from _typeshed import Incomplete

from .interfaces import (ContactTracer, InfectionModel, Location,
                         PandemicRegulation, PandemicSimState, PandemicTesting,
                         Person, PersonRoutineAssignment, Registry,
                         SimTimeInterval)
from .simulator_config import PandemicSimConfig
from .simulator_opts import PandemicSimOpts

def make_locations(sim_config: PandemicSimConfig) -> List[Location]: ...

class PandemicSim:
    location_names: Incomplete
    person_types: Incomplete
    prev_loc_data: Incomplete
    def __init__(
        self,
        locations: Sequence[Location],
        persons: Sequence[Person],
        infection_model: Optional[InfectionModel] = ...,
        infection_model_delta: Optional[InfectionModel] = ...,
        pandemic_testing: Optional[PandemicTesting] = ...,
        contact_tracer: Optional[ContactTracer] = ...,
        new_time_slot_interval: SimTimeInterval = ...,
        infection_update_interval: SimTimeInterval = ...,
        person_routine_assignment: Optional[PersonRoutineAssignment] = ...,
        infection_threshold: int = ...,
        hospital_capacity: int = ...,
        delta_start_lo: int = ...,
        delta_start_hi: int = ...,
    ) -> None: ...
    @classmethod
    def from_config(
        cls, sim_config: PandemicSimConfig, sim_opts: PandemicSimOpts = ...
    ) -> PandemicSim: ...
    @property
    def registry(self) -> Registry: ...
    def step(self) -> None: ...
    def step_day(self, hours_in_a_day: int = ...) -> None: ...
    def impose_regulation(self, regulation: PandemicRegulation) -> None: ...
    @property
    def state(self) -> PandemicSimState: ...
    def reset(self) -> None: ...
