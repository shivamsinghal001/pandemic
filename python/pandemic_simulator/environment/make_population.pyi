from typing import List

from .interfaces import Person
from .simulator_config import PandemicSimConfig

def make_population(sim_config: PandemicSimConfig) -> List[Person]: ...
