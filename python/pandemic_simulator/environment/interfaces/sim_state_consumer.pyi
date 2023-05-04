import abc
from abc import ABC, abstractmethod
from typing import Any

from .regulation import PandemicRegulation
from .sim_state import PandemicSimState

class SimStateConsumer(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def consume_begin(self, sim_state: PandemicSimState) -> None: ...
    @abstractmethod
    def consume_state(
        self, sim_state: PandemicSimState, regulation: PandemicRegulation
    ) -> None: ...
    @abstractmethod
    def finalize(self, *args: Any, **kwargs: Any) -> Any: ...
    @abstractmethod
    def reset(self) -> None: ...
    def close(self) -> None: ...
