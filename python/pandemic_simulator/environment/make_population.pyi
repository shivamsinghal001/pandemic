from .interfaces import Person
from .simulator_config import PandemicSimConfig
from typing import List

def make_population(sim_config: PandemicSimConfig) -> List[Person]: ...
