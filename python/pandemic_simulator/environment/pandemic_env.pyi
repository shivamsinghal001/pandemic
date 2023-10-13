from typing import Dict, List, Optional, Sequence, Tuple

import gymnasium
import numpy as np
from _typeshed import Incomplete

from .done import DoneFunction
from .interfaces import LocationID, PandemicObservation, PandemicRegulation
from .pandemic_sim import PandemicSim
from .reward import RewardFunction
from .simulator_config import PandemicSimConfig
from .simulator_opts import PandemicSimOpts

class PandemicGymEnv(gymnasium.Env):
    observation_space: Incomplete
    constrain: Incomplete
    action_space: Incomplete
    four_start: Incomplete
    def __init__(
        self,
        pandemic_sim: PandemicSim,
        pandemic_regulations: Sequence[PandemicRegulation],
        reward_fn: Optional[RewardFunction] = ...,
        true_reward_fn: Optional[RewardFunction] = ...,
        done_fn: Optional[DoneFunction] = ...,
        obs_history_size: int = ...,
        num_days_in_obs: int = ...,
        sim_steps_per_regulation: int = ...,
        non_essential_business_location_ids: Optional[List[LocationID]] = ...,
        constrain: bool = ...,
        four_start: bool = ...,
    ) -> None: ...
    @classmethod
    def from_config(
        cls,
        sim_config: PandemicSimConfig,
        pandemic_regulations: Sequence[PandemicRegulation],
        sim_opts: PandemicSimOpts = ...,
        reward_fn: Optional[RewardFunction] = ...,
        done_fn: Optional[DoneFunction] = ...,
        obs_history_size: int = ...,
        num_days_in_obs: int = ...,
        non_essential_business_location_ids: Optional[List[LocationID]] = ...,
    ) -> PandemicGymEnv: ...
    @property
    def pandemic_sim(self) -> PandemicSim: ...
    @property
    def observation(self) -> PandemicObservation: ...
    @property
    def last_reward(self) -> float: ...
    @property
    def get_true_reward(self) -> float: ...
    @property
    def get_true_reward2(self) -> float: ...
    def obs_to_numpy(self, obs: PandemicObservation) -> np.ndarray: ...
    def step(self, action: int) -> Tuple[PandemicObservation, float, bool, Dict]: ...
    def reset(self) -> np.ndarray: ...
    def render(self, mode: str = ...) -> bool: ...

class PandemicPolicyGymEnv(PandemicGymEnv):
    def __init__(self, config=..., **kwargs) -> None: ...
    @classmethod
    def from_config(
        cls,
        sim_config: PandemicSimConfig,
        pandemic_regulations: Sequence[PandemicRegulation],
        sim_opts: PandemicSimOpts = ...,
        reward_fn: Optional[RewardFunction] = ...,
        done_fn: Optional[DoneFunction] = ...,
        obs_history_size: int = ...,
        num_days_in_obs: int = ...,
        non_essential_business_location_ids: Optional[List[LocationID]] = ...,
        alpha: float = ...,
        beta: float = ...,
        gamma: float = ...,
        delta: float = ...,
        constrain: bool = ...,
        four_start: bool = ...,
    ) -> PandemicPolicyGymEnv: ...
