from _typeshed import Incomplete

from ..interfaces import (AgeRestrictedBusinessBaseLocation, ContactRate,
                          NonEssentialBusinessBaseLocation,
                          NonEssentialBusinessLocationState, SimTimeTuple)

class RestaurantState(NonEssentialBusinessLocationState):
    contact_rate: ContactRate
    open_time: SimTimeTuple
    def __init__(
        self, contact_rate, visitor_capacity, visitor_time, open_time, locked
    ) -> None: ...

class Restaurant(NonEssentialBusinessBaseLocation[RestaurantState]):
    state_type: Incomplete

class BarState(NonEssentialBusinessLocationState):
    contact_rate: ContactRate
    open_time: SimTimeTuple
    def __init__(
        self, contact_rate, visitor_capacity, visitor_time, open_time, locked
    ) -> None: ...

class Bar(AgeRestrictedBusinessBaseLocation[BarState]):
    state_type: Incomplete
    age_limits: Incomplete
