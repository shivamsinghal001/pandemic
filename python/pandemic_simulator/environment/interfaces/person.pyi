import abc
from abc import ABC, abstractmethod
from typing import List, Optional, Sequence, Tuple

from .contact_tracer import ContactTracer
from .ids import LocationID, PersonID
from .infection_model import IndividualInfectionState, InfectionSummary, Risk
from .pandemic_testing_result import PandemicTestResult
from .pandemic_types import NoOP
from .regulation import PandemicRegulation
from .sim_time import SimTime

class PersonState:
    current_location: LocationID
    risk: Risk
    infection_state: Optional[IndividualInfectionState]
    infection_spread_multiplier: float
    infection_state_delta: Optional[IndividualInfectionState]
    infection_spread_multiplier_delta: float
    quarantine: bool
    quarantine_if_contact_positive: bool
    quarantine_if_household_quarantined: bool
    sick_at_home: bool
    avoid_gathering_size: int
    test_result: PandemicTestResult
    test_result_alpha: PandemicTestResult
    test_result_delta: PandemicTestResult
    avoid_location_types: List[type]
    not_infection_probability: float
    not_infection_probability_delta: float
    not_infection_probability_history: List[Tuple[LocationID, float]]
    not_infection_probability_delta_history: List[Tuple[LocationID, float]]
    def __init__(
        self,
        current_location,
        risk,
        infection_state,
        infection_spread_multiplier,
        infection_state_delta,
        infection_spread_multiplier_delta,
    ) -> None: ...

def get_infection_summary(person_state: PersonState) -> InfectionSummary: ...

class Person(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def step(
        self, sim_time: SimTime, contact_tracer: Optional[ContactTracer] = ...
    ) -> Optional[NoOP]: ...
    @abstractmethod
    def receive_regulation(self, regulation: PandemicRegulation) -> None: ...
    @abstractmethod
    def enter_location(self, location_id: LocationID) -> bool: ...
    @property
    @abstractmethod
    def id(self) -> PersonID: ...
    @property
    @abstractmethod
    def home(self) -> LocationID: ...
    @property
    @abstractmethod
    def assigned_locations(self) -> Sequence[LocationID]: ...
    @property
    @abstractmethod
    def state(self) -> PersonState: ...
    @abstractmethod
    def reset(self) -> None: ...
