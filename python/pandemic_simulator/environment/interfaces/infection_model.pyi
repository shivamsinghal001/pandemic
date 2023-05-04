import abc
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

from _typeshed import Incomplete

class InfectionSummary(Enum):
    NONE: str
    INFECTED: str
    CRITICAL: str
    RECOVERED: str
    DEAD: str

sorted_infection_summary: Incomplete

class Risk(Enum):
    LOW: int
    HIGH: int

class IndividualInfectionState:
    summary: InfectionSummary
    spread_probability: float
    exposed_rnb: float
    is_hospitalized: bool
    shows_symptoms: bool
    def __init__(
        self, summary, spread_probability, exposed_rnb, is_hospitalized, shows_symptoms
    ) -> None: ...

class InfectionModel(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def step(
        self,
        subject_infection_state: Optional[IndividualInfectionState],
        subject_age: int,
        subject_risk: Risk,
        infection_probability: float,
    ) -> IndividualInfectionState: ...
    @abstractmethod
    def needs_contacts(
        self, subject_infection_state: Optional[IndividualInfectionState]
    ) -> bool: ...
    @abstractmethod
    def reset(self) -> None: ...
