from typing import Set

from ordered_set import OrderedSet

from .ids import PersonID
from .sim_time import SimTimeTuple

class ContactRate:
    min_assignees: int
    min_assignees_visitors: int
    min_visitors: int
    fraction_assignees: float
    fraction_assignees_visitors: float
    fraction_visitors: float
    def __post_init__(self) -> None: ...
    def __init__(
        self,
        min_assignees,
        min_assignees_visitors,
        min_visitors,
        fraction_assignees,
        fraction_assignees_visitors,
        fraction_visitors,
    ) -> None: ...

class LocationState:
    contact_rate: ContactRate
    visitor_capacity: int
    visitor_time: SimTimeTuple
    is_open: bool
    assignees: OrderedSet
    assignees_in_location: OrderedSet
    visitors_in_location: OrderedSet
    social_gathering_event: bool
    @property
    def persons_in_location(self) -> Set[PersonID]: ...
    @property
    def num_persons_in_location(self) -> int: ...
    def __init__(self, contact_rate, visitor_capacity, visitor_time) -> None: ...

class BusinessLocationState(LocationState):
    open_time: SimTimeTuple
    def __init__(
        self, contact_rate, visitor_capacity, visitor_time, open_time
    ) -> None: ...

class NonEssentialBusinessLocationState(BusinessLocationState):
    locked: bool
    def __init__(
        self, contact_rate, visitor_capacity, visitor_time, open_time, locked
    ) -> None: ...
