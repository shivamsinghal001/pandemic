import abc
from abc import ABC, abstractmethod
from typing import Any

class PandemicViz(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def record(self, data: Any) -> None: ...
    def plot(self, *args: Any, **kwargs: Any) -> None: ...
