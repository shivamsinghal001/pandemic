from ..data import StageSchedule
from ..environment import PandemicRegulation, PandemicSimConfig, PandemicSimOpts
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Union

population_size_to_config: Dict[int, PandemicSimConfig]

class EvaluationOpts:
    num_seeds: int
    spread_rates: Optional[Sequence[float]]
    pandemic_test_rate_scales: Optional[Sequence[float]]
    avoid_gathering_sizes: Optional[Sequence[int]]
    social_distancing: Optional[Sequence[float]]
    population_sizes: Optional[Sequence[int]]
    strategies: Optional[Sequence[Union[int, Sequence[StageSchedule]]]]
    pandemic_regulations: Optional[List[PandemicRegulation]]
    default_sim_config: PandemicSimConfig
    sim_opts: Optional[List[PandemicSimOpts]]
    enable_warm_up: bool
    max_episode_length: int
    data_saver_path: Path
    data_filename: str
    render_runs: bool
    def __post_init__(self) -> None: ...
    def __init__(self, num_seeds, spread_rates, pandemic_test_rate_scales, avoid_gathering_sizes, social_distancing, population_sizes, strategies, pandemic_regulations, default_sim_config, sim_opts, enable_warm_up, max_episode_length, data_saver_path, render_runs) -> None: ...

def evaluate_strategies(exp_name: str, eval_opts: EvaluationOpts) -> None: ...
def evaluate_spread_rates(exp_name: str, eval_opts: EvaluationOpts) -> None: ...
def evaluate_testing_rates(exp_name: str, eval_opts: EvaluationOpts) -> None: ...
def evaluate_social_gatherings(exp_name: str, eval_opts: EvaluationOpts) -> None: ...
def evaluate_location_contact_rates(exp_name: str, eval_opts: EvaluationOpts) -> None: ...
def evaluate_population_sizes(exp_name: str, eval_opts: EvaluationOpts) -> None: ...
