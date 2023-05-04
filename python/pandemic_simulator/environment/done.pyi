import enum
from .interfaces import InfectionSummary, PandemicObservation
from abc import ABCMeta, abstractmethod
from typing import Any, List, Union

class DoneFunction(metaclass=ABCMeta):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    @abstractmethod
    def calculate_done(self, obs: PandemicObservation, action: int) -> bool: ...
    def reset(self) -> None: ...

class DoneFunctionType(enum.Enum):
    INFECTION_SUMMARY_ABOVE_THRESHOLD: str
    NO_MORE_INFECTIONS: str
    NO_PANDEMIC: str
    TIME_LIMIT: str
    @staticmethod
    def values() -> List[str]: ...

class DoneFunctionFactory:
    @staticmethod
    def default(
        done_function_type: Union[str, DoneFunctionType], *args: Any, **kwargs: Any
    ) -> DoneFunction: ...

class ORDone(DoneFunction):
    def __init__(
        self, done_fns: List[DoneFunction], *args: Any, **kwargs: Any
    ) -> None: ...
    def calculate_done(self, obs: PandemicObservation, action: int) -> bool: ...
    def reset(self) -> None: ...

class InfectionSummaryAboveThresholdDone(DoneFunction):
    def __init__(
        self,
        summary_type: InfectionSummary,
        threshold: float,
        *args: Any,
        **kwargs: Any
    ) -> None: ...
    def calculate_done(self, obs: PandemicObservation, action: int) -> bool: ...

class NoMoreInfectionsDone(DoneFunction):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def calculate_done(self, obs: PandemicObservation, action: int) -> bool: ...
    def reset(self) -> None: ...

class NoPandemicDone(DoneFunction):
    def __init__(self, num_days: int, *args: Any, **kwargs: Any) -> None: ...
    def calculate_done(self, obs: PandemicObservation, action: int) -> bool: ...

class TimeLimitDone(DoneFunction):
    def __init__(self, horizon: int = ..., *args: Any, **kwargs: Any) -> None: ...
    def calculate_done(self, obs: PandemicObservation, action: int) -> bool: ...
