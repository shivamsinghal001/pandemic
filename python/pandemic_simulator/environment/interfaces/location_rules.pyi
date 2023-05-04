from typing import Optional, Union

from .location_states import ContactRate
from .pandemic_types import Default
from .sim_time import SimTimeTuple

class LocationRule:
    contact_rate: Union[ContactRate, Default, None]
    visitor_time: Union[SimTimeTuple, Default, None]
    visitor_capacity: Union[Default, int, None]
    @classmethod
    def get_default(cls) -> LocationRule: ...
    def __init__(self, contact_rate, visitor_time, visitor_capacity) -> None: ...

class BusinessLocationRule(LocationRule):
    open_time: Union[SimTimeTuple, Default, None]
    def __init__(
        self, contact_rate, visitor_time, visitor_capacity, open_time
    ) -> None: ...

class NonEssentialBusinessLocationRule(BusinessLocationRule):
    lock: Optional[bool]
    def __init__(
        self, contact_rate, visitor_time, visitor_capacity, open_time, lock
    ) -> None: ...
