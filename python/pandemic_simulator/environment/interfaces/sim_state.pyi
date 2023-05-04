from typing import Dict, Mapping, Tuple, Type

from .ids import LocationID, PersonID
from .infection_model import InfectionSummary
from .location import LocationSummary
from .location_states import LocationState
from .pandemic_testing import GlobalTestingState
from .person import PersonState
from .sim_time import SimTime

class PandemicSimState:
    id_to_person_state: Dict[PersonID, PersonState]
    id_to_location_state: Dict[LocationID, LocationState]
    location_type_infection_summary: Dict[Type, int]
    global_infection_summary: Dict[InfectionSummary, int]
    global_infection_summary_alpha: Dict[InfectionSummary, int]
    global_infection_summary_delta: Dict[InfectionSummary, int]
    global_testing_state: GlobalTestingState
    global_testing_state_alpha: GlobalTestingState
    global_testing_state_delta: GlobalTestingState
    global_location_summary: Mapping[Tuple[str, str], LocationSummary]
    infection_above_threshold: bool
    regulation_stage: int
    regulation_stage_sum: int
    sim_time: SimTime
    def __init__(
        self,
        id_to_person_state,
        id_to_location_state,
        location_type_infection_summary,
        global_infection_summary,
        global_infection_summary_alpha,
        global_infection_summary_delta,
        global_testing_state,
        global_testing_state_alpha,
        global_testing_state_delta,
        global_location_summary,
        infection_above_threshold,
        regulation_stage,
        regulation_stage_sum,
        sim_time,
    ) -> None: ...
