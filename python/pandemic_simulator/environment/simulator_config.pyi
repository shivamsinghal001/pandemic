from typing import Any, Dict, Optional, Sequence, Type

from .interfaces import BaseLocation, PersonRoutineAssignment

class LocationConfig:
    location_type: Type[BaseLocation]
    num: int
    num_assignees: int
    state_opts: Dict[str, Any]
    extra_opts: Dict[str, Any]
    def __post_init__(self) -> None: ...
    def __init__(
        self, location_type, num, num_assignees, state_opts, extra_opts
    ) -> None: ...

class PandemicSimConfig:
    num_persons: int
    delta_start_lo: int
    delta_start_hi: int
    location_configs: Sequence[LocationConfig]
    regulation_compliance_prob: float
    max_hospital_capacity: int
    person_routine_assignment: Optional[PersonRoutineAssignment]
    def __post_init__(self) -> None: ...
    def __init__(
        self,
        num_persons,
        delta_start_lo,
        delta_start_hi,
        location_configs,
        regulation_compliance_prob,
        person_routine_assignment,
    ) -> None: ...
