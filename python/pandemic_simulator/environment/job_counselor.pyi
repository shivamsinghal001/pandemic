from typing import Optional, Sequence

from .interfaces import LocationID, SimTimeTuple
from .simulator_config import LocationConfig

class WorkPackage:
    work: LocationID
    work_time: SimTimeTuple
    def __init__(self, work, work_time) -> None: ...

class JobCounselor:
    def __init__(self, location_configs: Sequence[LocationConfig]) -> None: ...
    def next_available_work(self) -> Optional[WorkPackage]: ...
