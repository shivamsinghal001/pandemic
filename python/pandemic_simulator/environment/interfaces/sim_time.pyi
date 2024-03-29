from typing import List, Optional, Tuple, Union

class SimTime:
    hour: int
    week_day: int
    day: int
    year: int
    def __post_init__(self) -> None: ...
    def now(self, frmt: str = ...) -> List[int]: ...
    def step(self) -> None: ...
    def in_hours(self) -> int: ...
    @classmethod
    def from_hours(cls, hours: int) -> SimTime: ...
    def __add__(self, other: Union["SimTime", "SimTimeInterval"]) -> SimTime: ...
    def __init__(self, hour, week_day, day, year) -> None: ...

class SimTimeInterval:
    hour: int
    day: int
    year: int
    offset_hour: int
    offset_day: int
    def __post_init__(self) -> None: ...
    def trigger_at_interval(self, sim_time: SimTime) -> bool: ...
    def in_hours(self) -> int: ...
    def __init__(self, hour, day, year, offset_hour, offset_day) -> None: ...

class SimTimeTuple:
    hours: Optional[Tuple[int, ...]]
    week_days: Optional[Tuple[int, ...]]
    days: Optional[Tuple[int, ...]]
    def __post_init__(self) -> None: ...
    def __contains__(self, item: SimTime) -> bool: ...
    def __init__(self, hours, week_days, days) -> None: ...
