from enum import Enum
from typing import Dict, Optional, Tuple

from ..interfaces import IndividualInfectionState, InfectionModel, Risk

class _SEIRLabel(Enum):
    susceptible: str
    exposed: str
    pre_asymp: str
    pre_symp: str
    asymp: str
    symp: str
    needs_hospitalization: str
    hospitalized: str
    recovered: str
    deceased: str

class _AgeLimit(Enum): ...

class SEIRInfectionState(IndividualInfectionState):
    label: _SEIRLabel
    def __init__(
        self,
        summary,
        spread_probability,
        exposed_rnb,
        is_hospitalized,
        shows_symptoms,
        label,
    ) -> None: ...

class SpreadProbabilityParams:
    mean: float
    sigma: float
    def __init__(self, mean, sigma) -> None: ...

class SEIRModel(InfectionModel):
    def __init__(
        self,
        symp_proportion: float = ...,
        exposed_rate: Optional[float] = ...,
        pre_asymp_rate: float = ...,
        pre_symp_rate: float = ...,
        recovery_rate_asymp: Optional[float] = ...,
        recovery_rate_symp_non_treated: Optional[float] = ...,
        recovery_rate_needs_hosp: float = ...,
        recovery_rate_hosp: Optional[float] = ...,
        hosp_rate_symp: Optional[Dict[Tuple[_AgeLimit, Risk], float]] = ...,
        death_rate_hosp: Optional[Dict[Tuple[_AgeLimit, Risk], float]] = ...,
        death_rate_needs_hosp: Optional[Dict[Tuple[_AgeLimit, Risk], float]] = ...,
        from_symp_to_hosp_rate: float = ...,
        from_needs_hosp_to_death_rate: float = ...,
        from_hosp_to_death_rate: Optional[float] = ...,
        spread_probability_params: Optional[SpreadProbabilityParams] = ...,
        pandemic_start_limit: int = ...,
    ) -> None: ...
    def step(
        self,
        subject_state: Optional[IndividualInfectionState],
        subject_age: int,
        subject_risk: Risk,
        infection_probability: float,
    ) -> IndividualInfectionState: ...
    def needs_contacts(
        self, subject_state: Optional[IndividualInfectionState]
    ) -> bool: ...
    def reset(self) -> None: ...
