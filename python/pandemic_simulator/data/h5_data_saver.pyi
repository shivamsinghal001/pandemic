from pathlib import Path
from typing import Any, Optional, Union

import numpy as np

from ..environment import PandemicObservation
from .interfaces import ExperimentDataSaver

class H5DataSaver(ExperimentDataSaver):
    def __init__(
        self, filename: str, path: Path = ..., overwrite: bool = ...
    ) -> None: ...
    def begin(self, obs: PandemicObservation) -> None: ...
    def record(
        self, obs: PandemicObservation, reward: Optional[Union[np.ndarray, float]] = ...
    ) -> None: ...
    def finalize(self, **kwargs: Any) -> bool: ...
    def close(self) -> None: ...
