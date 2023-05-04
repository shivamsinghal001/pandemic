from typing import Optional

from structlog import BoundLogger as BoundLogger

from .city_registry import *
from .contact_tracing import *
from .done import *
from .infection_model import *
from .interfaces import *
from .job_counselor import *
from .location import *
from .make_population import *
from .pandemic_env import *
from .pandemic_sim import *
from .pandemic_testing_strategies import *
from .person import *
from .reward import *
from .simulator_config import *
from .simulator_opts import *

def init_globals(
    registry: Optional[Registry] = ...,
    seed: Optional[int] = ...,
    log: Optional[BoundLogger] = ...,
) -> None: ...
