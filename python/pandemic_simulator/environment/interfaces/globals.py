# Confidential, Copyright 2020, Sony Corporation of America, All rights reserved.
from typing import Optional

import numpy as np

from .registry import Registry
from pandemic_simulator.environment.city_registry import *

registry: Optional[Registry] = CityRegistry()
numpy_rng: np.random.RandomState = np.random.RandomState(seed=0)
