import enum
from abc import ABCMeta, abstractmethod
from typing import Any, List, Optional, Sequence, Union

from .interfaces import InfectionSummary, PandemicObservation

class RewardFunction(metaclass=ABCMeta):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    @abstractmethod
    def calculate_reward(
        self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation
    ) -> float: ...

class RewardFunctionType(enum.Enum):
    INFECTION_SUMMARY_INCREASE: str
    INFECTION_SUMMARY_ABOVE_THRESHOLD: str
    INFECTION_SUMMARY_ABSOLUTE: str
    UNLOCKED_BUSINESS_LOCATIONS: str
    LOWER_STAGE: str
    AVERAGE_STAGE: str
    SMOOTH_STAGE_CHANGES: str
    ELDERLY_HOSPITALIZED: str
    POLITICAL: str
    @staticmethod
    def values() -> List[str]: ...

class RewardFunctionFactory:
    @staticmethod
    def default(
        reward_function_type: Union[str, RewardFunctionType], *args: Any, **kwargs: Any
    ) -> RewardFunction: ...

class SumReward(RewardFunction):
    def __init__(
        self,
        reward_fns: List[RewardFunction],
        weights: Optional[List[float]] = ...,
        *args: Any,
        **kwargs: Any
    ) -> None: ...
    def calculate_reward(
        self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation
    ) -> float: ...

class InfectionSummaryIncreaseReward(RewardFunction):
    def __init__(
        self, summary_type: InfectionSummary, *args: Any, **kwargs: Any
    ) -> None: ...
    def calculate_reward(
        self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation
    ) -> float: ...

class InfectionSummaryAbsoluteReward(RewardFunction):
    def __init__(
        self, summary_type: InfectionSummary, *args: Any, **kwargs: Any
    ) -> None: ...
    def calculate_reward(
        self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation
    ) -> float: ...

class InfectionSummaryAboveThresholdReward(RewardFunction):
    def __init__(
        self,
        summary_type: InfectionSummary,
        threshold: float,
        *args: Any,
        **kwargs: Any
    ) -> None: ...
    def calculate_reward(
        self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation
    ) -> float: ...

class UnlockedBusinessLocationsReward(RewardFunction):
    def __init__(
        self, obs_indices: Optional[Sequence[int]] = ..., *args: Any, **kwargs: Any
    ) -> None: ...
    def calculate_reward(
        self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation
    ) -> float: ...

class LowerStageReward(RewardFunction):
    def __init__(self, num_stages: int, *args: Any, **kwargs: Any) -> None: ...
    def calculate_reward(
        self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation
    ) -> float: ...

class AverageStageReward(RewardFunction):
    def __init__(self, num_stages: int, *args: Any, **kwargs: Any) -> None: ...
    def calculate_reward(
        self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation
    ) -> float: ...

class SmoothStageChangesReward(RewardFunction):
    def __init__(self, num_stages: int, *args: Any, **kwargs: Any) -> None: ...
    def calculate_reward(
        self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation
    ) -> float: ...

class ElderlyHospitalizedReward(RewardFunction):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def calculate_reward(
        self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation
    ) -> float: ...

class PoliticalReward(RewardFunction):
    def __init__(self, threshold: float = ..., *args: Any, **kwargs: Any) -> None: ...
    def calculate_reward(
        self, prev_obs: PandemicObservation, action: int, obs: PandemicObservation
    ) -> float: ...
