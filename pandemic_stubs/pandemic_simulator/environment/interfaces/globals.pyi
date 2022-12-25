import numpy as np
from .registry import Registry as Registry
from typing import Optional

registry: Optional[Registry]
numpy_rng: np.random.RandomState
