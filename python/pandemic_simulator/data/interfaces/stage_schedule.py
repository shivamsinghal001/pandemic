import dataclasses
from typing import Optional

__all__ = ["StageSchedule"]


@dataclasses.dataclass(frozen=True)
class StageSchedule:
    stage: int
    end_day: Optional[int] = None
