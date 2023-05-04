from typing import Optional, Sequence

import numpy as np

from .ids import LocationID
from .sim_state import PandemicSimState

class PandemicObservation:
    global_infection_summary: np.ndarray
    global_infection_summary_alpha: np.ndarray
    global_infection_summary_delta: np.ndarray
    global_testing_summary: np.ndarray
    global_testing_summary_alpha: np.ndarray
    global_testing_summary_delta: np.ndarray
    stage: np.ndarray
    infection_above_threshold: np.ndarray
    time_day: np.ndarray
    state: PandemicSimState
    unlocked_non_essential_business_locations: Optional[np.ndarray]
    @classmethod
    def create_empty(
        cls, history_size: int = ..., num_non_essential_business: Optional[int] = ...
    ) -> PandemicObservation: ...
    def update_obs_with_sim_state(
        self,
        sim_state: PandemicSimState,
        hist_index: int = ...,
        business_location_ids: Optional[Sequence[LocationID]] = ...,
    ) -> None: ...
    @property
    def infection_summary_labels(self) -> Sequence[str]: ...
    def __init__(
        self,
        global_infection_summary,
        global_infection_summary_alpha,
        global_infection_summary_delta,
        global_testing_summary,
        global_testing_summary_alpha,
        global_testing_summary_delta,
        stage,
        infection_above_threshold,
        time_day,
        state,
        unlocked_non_essential_business_locations,
    ) -> None: ...
