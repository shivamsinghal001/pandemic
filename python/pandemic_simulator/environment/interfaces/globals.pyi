from typing import Optional

import numpy as np

from .registry import Registry as Registry

registry: Optional[Registry]
numpy_rng: np.random.RandomState
