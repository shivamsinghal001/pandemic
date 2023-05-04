class PandemicSimOpts:
    infection_spread_rate_mean: float
    infection_spread_rate_sigma: float
    infection_delta_spread_rate_mean: float
    infection_delta_spread_rate_sigma: float
    spontaneous_testing_rate: float
    symp_testing_rate: float
    critical_testing_rate: float
    testing_false_positive_rate: float
    testing_false_negative_rate: float
    retest_rate: float
    sim_steps_per_regulation: int
    use_contact_tracer: bool
    contact_tracer_history_size: int
    infection_threshold: int
    def __init__(
        self,
        infection_spread_rate_mean,
        infection_spread_rate_sigma,
        infection_delta_spread_rate_mean,
        infection_delta_spread_rate_sigma,
        spontaneous_testing_rate,
        symp_testing_rate,
        critical_testing_rate,
        testing_false_positive_rate,
        testing_false_negative_rate,
        retest_rate,
        sim_steps_per_regulation,
        use_contact_tracer,
        contact_tracer_history_size,
        infection_threshold,
    ) -> None: ...
