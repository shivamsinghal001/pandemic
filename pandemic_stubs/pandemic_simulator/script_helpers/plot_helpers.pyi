from ..data import ExperimentResult
from ..environment import PandemicSimConfig
from pathlib import Path
from typing import Optional, Sequence, Tuple, Union

def make_evaluation_plots_from_data(data: Sequence[ExperimentResult], exp_name: str, param_labels: Sequence[str], bar_plot_xlabel: str, fig_save_path: Path = ..., sim_config: Optional[PandemicSimConfig] = ..., show_summary_plots: bool = ..., show_cumulative_reward: bool = ..., show_time_to_peak: bool = ..., show_pandemic_duration: bool = ..., show_stage_trials: bool = ..., annotate_stages: Union[bool, Sequence[bool]] = ..., figsize: Optional[Tuple[int, int]] = ...) -> None: ...
def make_evaluation_plots(exp_name: str, param_labels: Sequence[str], bar_plot_xlabel: str, data_saver_path: Path = ..., sim_config: Optional[PandemicSimConfig] = ..., show_summary_plots: bool = ..., show_cumulative_reward: bool = ..., show_time_to_peak: bool = ..., show_pandemic_duration: bool = ..., show_stage_trials: bool = ..., annotate_stages: Union[bool, Sequence[bool]] = ..., figsize: Optional[Tuple[int, int]] = ...) -> None: ...
