# Confidential, Copyright 2020, Sony Corporation of America, All rights reserved.
import pdb
from copy import deepcopy
from typing import Dict, List, Mapping, Optional, Sequence, Tuple, Type

import gymnasium
import numpy as np
from gymnasium import spaces
from ray.rllib.env.multi_agent_env import make_multi_agent
from ray.tune.registry import register_env

from .interfaces import StageSchedule
from .done import DoneFunction
from .interfaces import (InfectionSummary, LocationID,
                         NonEssentialBusinessLocationState,
                         PandemicObservation, PandemicRegulation,
                         sorted_infection_summary)
from .pandemic_sim import PandemicSim
from .reward import (RewardFunction, RewardFunctionFactory, RewardFunctionType,
                     SumReward)
from .simulator_config import PandemicSimConfig
from .simulator_opts import PandemicSimOpts

__all__ = ["PandemicGymEnv", "PandemicPolicyGymEnv"]

safe_policies = {
    "S0": 0,
    "S1": 1,
    "S2": 2,
    "S3": 3,
    "S4": 4,
    "S0-4-0": [
        StageSchedule(stage=4, end_day=30),
        StageSchedule(stage=0, end_day=None),
    ],
    "S0-4-0-FI": [
        StageSchedule(stage=4, end_day=30),
        StageSchedule(stage=3, end_day=35),
        StageSchedule(stage=2, end_day=40),
        StageSchedule(stage=1, end_day=45),
        StageSchedule(stage=0, end_day=None),
    ],
    "S0-4-0-GI": [
        StageSchedule(stage=4, end_day=30),
        StageSchedule(stage=3, end_day=50),
        StageSchedule(stage=2, end_day=70),
        StageSchedule(stage=1, end_day=90),
        StageSchedule(stage=0, end_day=None),
    ],
    "swedish_strategy": [
        StageSchedule(stage=0, end_day=3),
        StageSchedule(stage=1, end_day=None),
    ],
    "italian_strategy": [
        StageSchedule(stage=0, end_day=3),
        StageSchedule(stage=1, end_day=8),
        StageSchedule(stage=2, end_day=13),
        StageSchedule(stage=3, end_day=25),
        StageSchedule(stage=4, end_day=59),
        StageSchedule(stage=3, end_day=79),
        StageSchedule(stage=2, end_day=None),
    ],
}


class PandemicGymEnv(gymnasium.Env):
    """A gymnasium environment interface wrapper for the Pandemic Simulator."""

    _pandemic_sim: PandemicSim
    _stage_to_regulation: Mapping[int, PandemicRegulation]
    _obs_history_size: int
    _sim_steps_per_regulation: int
    _non_essential_business_loc_ids: Optional[List[LocationID]]
    _reward_fn: Optional[RewardFunction]
    _done_fn: Optional[DoneFunction]

    _obs_with_history: np.ndarray
    _last_observation: PandemicObservation
    _last_reward: float

    def __init__(
        self,
        pandemic_sim: PandemicSim,
        pandemic_regulations: Sequence[PandemicRegulation],
        reward_fn: Optional[RewardFunction] = None,
        true_reward_fn: Optional[RewardFunction] = None,
        proxy_reward_fn: Optional[RewardFunction] = None,
        done_fn: Optional[DoneFunction] = None,
        obs_history_size: int = 1,
        num_days_in_obs: int = 1,
        sim_steps_per_regulation: int = 24,
        non_essential_business_location_ids: Optional[List[LocationID]] = None,
        constrain: bool = False,
        four_start: bool = False,
        use_safe_policy_actions=False,
        safe_policy="S0-4-0",
    ):
        """
        :param pandemic_sim: Pandemic simulator instance
        :param pandemic_regulations: A sequence of pandemic regulations
        :param reward_fn: reward function
        :param done_fn: done function
        :param obs_history_size: number of latest sim step states to include in the observation
        :param sim_steps_per_regulation: number of sim_steps to run for each regulation
        :param non_essential_business_location_ids: an ordered list of non-essential business location ids
        """
        self._pandemic_sim = pandemic_sim
        self._stage_to_regulation = {reg.stage: reg for reg in pandemic_regulations}
        self._obs_history_size = obs_history_size
        self._num_days_in_obs = num_days_in_obs
        self._sim_steps_per_regulation = sim_steps_per_regulation

        if non_essential_business_location_ids is not None:
            for loc_id in non_essential_business_location_ids:
                assert isinstance(
                    self._pandemic_sim.state.id_to_location_state[loc_id],
                    NonEssentialBusinessLocationState,
                )
        self._non_essential_business_loc_ids = non_essential_business_location_ids

        self._reward_fn = reward_fn
        self._true_reward_fn = true_reward_fn
        self._proxy_reward_fn = proxy_reward_fn
        self._use_safe_policy_actions = use_safe_policy_actions
        self._safe_policy = safe_policy
        assert self._safe_policy in safe_policies
        stages_to_execute = safe_policies[self._safe_policy]
        self.stages = (
            [StageSchedule(stage=stages_to_execute, end_day=None)]
            if isinstance(stages_to_execute, int)
            else stages_to_execute
        )
        self.stage_idx = 0

        self._done_fn = done_fn

        self._obs_with_history = self.obs_to_numpy(
            PandemicObservation.create_empty(
                history_size=self._obs_history_size * self._num_days_in_obs
            )
        )
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=self._obs_with_history.shape, dtype=np.float64
        )

        self.constrain = constrain
        if self.constrain:
            self.action_space = gymnasium.spaces.Discrete(3)
        else:
            self.action_space = gymnasium.spaces.Discrete(len(self._stage_to_regulation))
        self.four_start = four_start

    @classmethod
    def from_config(
        cls: Type["PandemicGymEnv"],
        sim_config: PandemicSimConfig,
        pandemic_regulations: Sequence[PandemicRegulation],
        sim_opts: PandemicSimOpts = PandemicSimOpts(),
        reward_fn: Optional[RewardFunction] = None,
        done_fn: Optional[DoneFunction] = None,
        obs_history_size: int = 1,
        num_days_in_obs: int = 1,
        non_essential_business_location_ids: Optional[List[LocationID]] = None,
    ) -> "PandemicGymEnv":
        """
        Creates an instance using config

        :param sim_config: Simulator config
        :param pandemic_regulations: A sequence of pandemic regulations
        :param sim_opts: Simulator opts
        :param reward_fn: reward function
        :param done_fn: done function
        :param obs_history_size: number of latest sim step states to include in the observation
        :param non_essential_business_location_ids: an ordered list of non-essential business location ids
        """
        sim = PandemicSim.from_config(sim_config, sim_opts)

        if sim_config.max_hospital_capacity == -1:
            raise Exception("Nothing much to optimise if max hospital capacity is -1.")

        reward_fn = reward_fn or SumReward(
            reward_fns=[
                RewardFunctionFactory.default(
                    RewardFunctionType.INFECTION_SUMMARY_ABOVE_THRESHOLD,
                    summary_type=InfectionSummary.CRITICAL,
                    threshold=sim_config.max_hospital_capacity / sim_config.num_persons,
                ),
                RewardFunctionFactory.default(
                    RewardFunctionType.INFECTION_SUMMARY_ABOVE_THRESHOLD,
                    summary_type=InfectionSummary.CRITICAL,
                    threshold=3
                    * sim_config.max_hospital_capacity
                    / sim_config.num_persons,
                ),
                RewardFunctionFactory.default(
                    RewardFunctionType.LOWER_STAGE, num_stages=len(pandemic_regulations)
                ),
                RewardFunctionFactory.default(
                    RewardFunctionType.SMOOTH_STAGE_CHANGES,
                    num_stages=len(pandemic_regulations),
                ),
            ],
            weights=[0.4, 1, 0.1, 0.02],
        )

        return PandemicGymEnv(
            pandemic_sim=sim,
            pandemic_regulations=pandemic_regulations,
            sim_steps_per_regulation=sim_opts.sim_steps_per_regulation,
            reward_fn=reward_fn,
            done_fn=done_fn,
            obs_history_size=obs_history_size,
            num_days_in_obs=num_days_in_obs,
            non_essential_business_location_ids=non_essential_business_location_ids,
        )

    @property
    def pandemic_sim(self) -> PandemicSim:
        return self._pandemic_sim

    @property
    def observation(self) -> PandemicObservation:
        return self._last_observation

    @property
    def last_reward(self) -> float:
        return self._last_reward

    @property
    def get_true_reward(self) -> float:
        return self._last_true_reward

    @property
    def get_proxy_reward(self) -> float:
        return self._last_proxy_reward

    @property
    def get_true_reward2(self) -> float:
        return self._last_true_reward

    def obs_to_numpy(self, obs: PandemicObservation) -> np.ndarray:
        return np.concatenate(
            [
                obs.time_day,
                obs.stage,
                obs.infection_above_threshold,
                obs.global_testing_summary_alpha,
                obs.global_testing_summary_delta,
            ],
            axis=2,
        )

    def step(self, action: int) -> Tuple[PandemicObservation, float, bool, Dict]:
        cur_stage = self.stages[self.stage_idx]
        stage = cur_stage.stage
        actual_stage = self._last_observation.stage[-1, 0, 0]
        if (
            cur_stage.end_day is not None
            and self._last_observation.state is not None
            and cur_stage.end_day <= self._last_observation.state.sim_time.day
        ):
            self.stage_idx += 1

        if stage > actual_stage: # decrease
            safe_policy_action = 0
        elif stage==actual_stage: # do nothing
            safe_policy_action = 1
        elif stage < actual_stage: # increase
            safe_policy_action = 2

        if self._use_safe_policy_actions:
            obs, reward, terminated, truncated, info = self._step(safe_policy_action)
        else:
            obs, reward, terminated, truncated, info = self._step(action)

        info[self._safe_policy] = safe_policy_action

        return obs, reward, terminated, truncated, info

    def _step(self, action: int) -> Tuple[PandemicObservation, float, bool, Dict]:
        # assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))

        # execute the action if different from the current stage
        if self.constrain:
            prev_stage = self._last_observation.stage[-1, 0, 0]
            regulation = self._stage_to_regulation[
                int(min(max(prev_stage + action - 1, 0), 4))
            ]
            self._pandemic_sim.impose_regulation(regulation=regulation)

        else:
            if (
                action != self._last_observation.stage[-1, 0, 0]
            ):  # stage has a TNC layout
                regulation = self._stage_to_regulation[action]
                self._pandemic_sim.impose_regulation(regulation=regulation)

        # update the sim until next regulation interval trigger and construct obs from state hist
        obs = PandemicObservation.create_empty(
            history_size=self._obs_history_size,
            num_non_essential_business=len(self._non_essential_business_loc_ids)
            if self._non_essential_business_loc_ids is not None
            else None,
        )

        hist_index = 0
        for i in range(self._sim_steps_per_regulation):
            # step sim
            self._pandemic_sim.step()

            # store only the last self._history_size state values
            if (i + 1) % (
                self._sim_steps_per_regulation // self._obs_history_size
            ) == 0:
                obs.update_obs_with_sim_state(
                    self._pandemic_sim.state,
                    hist_index,
                    self._non_essential_business_loc_ids,
                )
                hist_index += 1

            # append the last timestep if there's an overflow
            if (
                (i + 1) == self._sim_steps_per_regulation
                and self._sim_steps_per_regulation % self._obs_history_size != 0
            ):
                obs.update_obs_with_sim_state(
                    self._pandemic_sim.state,
                    hist_index,
                    self._non_essential_business_loc_ids,
                )

        prev_obs = self._last_observation
        self._last_reward, last_rew_breakdown = (
            self._reward_fn.calculate_reward(prev_obs, action, obs)
            if self._reward_fn
            else 0.0
        )
        self._last_true_reward, last_true_rew_breakdown = (
            self._true_reward_fn.calculate_reward(prev_obs, action, obs)
            if self._true_reward_fn is not None
            else 0.0
        )
        self._last_proxy_reward, last_proxy_rew_breakdown = (
            self._proxy_reward_fn.calculate_reward(prev_obs, action, obs)
            if self._proxy_reward_fn is not None
            else 0.0
        )
        terminated = self._done_fn.calculate_done(obs, action) if self._done_fn else False
        self._last_observation = obs
        self._obs_with_history = np.concatenate(
            [
                self._obs_with_history[self._obs_history_size :],
                self.obs_to_numpy(self._last_observation),
            ]
        )
        return (
            self._obs_with_history,
            self._last_reward,
            terminated,
            False,
            {
                "rew": self._last_reward,
                "true_rew": self._last_true_reward,
                "proxy_rew": self._last_proxy_reward,
                "rew_breakdown": last_rew_breakdown,
                "true_rew_breakdown": last_true_rew_breakdown,
                "proxy_rew_breakdown": last_proxy_rew_breakdown,
            },
        )

    def reset(self, *, seed=None, options=None):
        self._pandemic_sim.reset()
        self._last_reward = 0.0
        self._last_true_reward = 0.0
        if self._done_fn is not None:
            self._done_fn.reset()

        self._last_observation = PandemicObservation.create_empty(
            history_size=self._obs_history_size,
            num_non_essential_business=len(self._non_essential_business_loc_ids)
            if self._non_essential_business_loc_ids is not None
            else None,
        )
        self._obs_with_history = self.obs_to_numpy(
            PandemicObservation.create_empty(
                history_size=self._obs_history_size * self._num_days_in_obs,
                num_non_essential_business=len(self._non_essential_business_loc_ids)
                if self._non_essential_business_loc_ids is not None
                else None,
            )
        )

        if self.four_start:
            return self.step(4)[0], {}
        else:
            return self._obs_with_history, {}

    def render(self, mode: str = "human") -> bool:
        pass


class PandemicPolicyGymEnv(PandemicGymEnv):
    def __init__(self, config={}, **kwargs):
        config.update(kwargs)
        sim_config = config["sim_config"]
        pandemic_regulations = config["pandemic_regulations"]
        sim_opts = config["sim_opts"]
        config["reward_fun"]
        true_reward_fn = config["true_reward_fun"]
        proxy_reward_fn = config["proxy_reward_fun"]
        if config["reward_fun"] == "proxy":
            reward_fn = proxy_reward_fn
        else:
            reward_fn = true_reward_fn
        use_safe_policy_actions = config.get("use_safe_policy_actions", False)
        safe_policy = config.get("safe_policy", "S0-4-0")
        done_fn = config["done_fn"]
        obs_history_size = config["obs_history_size"]
        num_days_in_obs = config["num_days_in_obs"]

        sim = PandemicSim.from_config(sim_config, sim_opts)

        if "sim_steps_per_regulation" in config:
            sim_steps_per_regulation = config["sim_steps_per_regulation"]
        else:
            sim_steps_per_regulation = 24

        if "non_essential_business_location_ids" in config:
            non_essential_business_location_ids = config[
                "non_essential_business_location_ids"
            ]
        else:
            non_essential_business_location_ids = None

        if "constrain" in config:
            constrain = config["constrain"]
        else:
            constrain = False

        if "four_start" in config:
            four_start = config["four_start"]
        else:
            four_start = False

        super().__init__(
            sim,
            pandemic_regulations,
            reward_fn,
            true_reward_fn,
            proxy_reward_fn,
            done_fn,
            obs_history_size,
            num_days_in_obs,
            sim_steps_per_regulation,
            non_essential_business_location_ids,
            constrain,
            four_start,
            use_safe_policy_actions,
            safe_policy,
        )

    @classmethod
    def from_config(
        cls: Type["PandemicPolicyGymEnv"],
        sim_config: PandemicSimConfig,
        pandemic_regulations: Sequence[PandemicRegulation],
        sim_opts: PandemicSimOpts = PandemicSimOpts(),
        reward_fn: Optional[RewardFunction] = None,
        done_fn: Optional[DoneFunction] = None,
        obs_history_size: int = 1,
        num_days_in_obs: int = 1,
        non_essential_business_location_ids: Optional[List[LocationID]] = None,
        alpha: float = 0.4,
        beta: float = 1,
        gamma: float = 0.1,
        delta: float = 0.02,
        constrain: bool = False,
        four_start: bool = False,
    ) -> "PandemicPolicyGymEnv":
        """
        Creates an instance using config

        :param sim_config: Simulator config
        :param pandemic_regulations: A sequence of pandemic regulations
        :param raw_regulations: The raw regulations output by regulation_network before processing
        :param sim_opts: Simulator opts
        :param reward_fn: reward function
        :param done_fn: done function
        :param obs_history_size: number of latest sim step states to include in the observation
        :param non_essential_business_location_ids: an ordered list of non-essential business location ids
        """
        sim = PandemicSim.from_config(sim_config, sim_opts)

        if sim_config.max_hospital_capacity == -1:
            raise Exception("Nothing much to optimise if max hospital capacity is -1.")

        reward_fn = reward_fn or SumReward(
            reward_fns=[
                RewardFunctionFactory.default(
                    RewardFunctionType.INFECTION_SUMMARY_ABOVE_THRESHOLD,
                    summary_type=InfectionSummary.CRITICAL,
                    threshold=sim_config.max_hospital_capacity / sim_config.num_persons,
                ),
                RewardFunctionFactory.default(
                    RewardFunctionType.INFECTION_SUMMARY_ABOVE_THRESHOLD,
                    summary_type=InfectionSummary.CRITICAL,
                    threshold=3
                    * sim_config.max_hospital_capacity
                    / sim_config.num_persons,
                ),
                RewardFunctionFactory.default(
                    RewardFunctionType.LOWER_STAGE, num_stages=len(pandemic_regulations)
                ),
                RewardFunctionFactory.default(
                    RewardFunctionType.SMOOTH_STAGE_CHANGES,
                    num_stages=len(pandemic_regulations),
                ),
            ],
            weights=[alpha, beta, gamma, delta],
        )

        true_reward_fn = SumReward(
            reward_fns=[
                RewardFunctionFactory.default(
                    RewardFunctionType.INFECTION_SUMMARY_ABSOLUTE,
                    summary_type=InfectionSummary.CRITICAL,
                ),
                RewardFunctionFactory.default(
                    RewardFunctionType.POLITICAL, summary_type=InfectionSummary.CRITICAL
                ),
                RewardFunctionFactory.default(
                    RewardFunctionType.LOWER_STAGE, num_stages=len(pandemic_regulations)
                ),
                RewardFunctionFactory.default(
                    RewardFunctionType.SMOOTH_STAGE_CHANGES,
                    num_stages=len(pandemic_regulations),
                ),
            ],
            weights=[10, 10, 0.1, 0.02],
        )

        proxy_reward_fn = reward_fn or SumReward(
            reward_fns=[
                RewardFunctionFactory.default(
                    RewardFunctionType.INFECTION_SUMMARY_ABOVE_THRESHOLD,
                    summary_type=InfectionSummary.CRITICAL,
                    threshold=sim_config.max_hospital_capacity / sim_config.num_persons,
                ),
                RewardFunctionFactory.default(
                    RewardFunctionType.INFECTION_SUMMARY_ABOVE_THRESHOLD,
                    summary_type=InfectionSummary.CRITICAL,
                    threshold=3
                    * sim_config.max_hospital_capacity
                    / sim_config.num_persons,
                ),
                RewardFunctionFactory.default(
                    RewardFunctionType.LOWER_STAGE, num_stages=len(pandemic_regulations)
                ),
                RewardFunctionFactory.default(
                    RewardFunctionType.SMOOTH_STAGE_CHANGES,
                    num_stages=len(pandemic_regulations),
                ),
            ],
            weights=[alpha, beta, gamma, delta],
        )

        return PandemicPolicyGymEnv(
            pandemic_sim=sim,
            pandemic_regulations=pandemic_regulations,
            sim_steps_per_regulation=sim_opts.sim_steps_per_regulation,
            reward_fn=reward_fn,
            true_reward_fn=true_reward_fn,
            proxy_reward_fn=proxy_reward_fn,
            done_fn=done_fn,
            obs_history_size=obs_history_size,
            non_essential_business_location_ids=non_essential_business_location_ids,
            constrain=constrain,
            four_start=four_start,
        )

register_env(
    "pandemic_env_multiagent",
    make_multi_agent(lambda config: PandemicPolicyGymEnv(config)),
)

