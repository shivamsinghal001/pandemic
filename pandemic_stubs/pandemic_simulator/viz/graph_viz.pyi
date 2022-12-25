from ..environment import PandemicSim
from .pandemic_viz import PandemicViz
from typing import Any, List

class GraphViz(PandemicViz):
    def __init__(self, sim: PandemicSim, num_stages: int = ..., days_per_interval: int = ...) -> None: ...
    @property
    def num_components_per_interval(self) -> List[int]: ...
    def record(self, data: Any, **kwargs: Any) -> None: ...
    def plot(self, *args: Any, **kwargs: Any) -> None: ...