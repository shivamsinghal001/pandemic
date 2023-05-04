from pathlib import Path
from typing import Sequence

from .interfaces import ExperimentDataLoader, ExperimentResult

class H5DataLoader(ExperimentDataLoader):
    def __init__(self, filename: str, path: Path = ...) -> None: ...
    def get_data(self) -> Sequence[ExperimentResult]: ...
