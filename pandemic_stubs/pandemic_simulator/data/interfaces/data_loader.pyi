import numpy as np
from ...environment import PandemicObservation, PandemicSimOpts
from abc import ABC
from typing import List, Optional, Sequence

class StageSchedule:
    stage: int
    end_day: Optional[int]
    def __init__(self, stage, end_day) -> None: ...

class ExperimentResult:
    sim_opts: PandemicSimOpts
    seeds: List[Optional[int]]
    obs_trajectories: PandemicObservation
    reward_trajectories: np.ndarray
    strategy: Sequence[StageSchedule]
    num_persons: int
    def __init__(self, sim_opts, seeds, obs_trajectories, reward_trajectories, strategy, num_persons) -> None: ...

class ExperimentDataLoader(ABC):
    def get_data(self) -> Sequence[ExperimentResult]: ...
