from _typeshed import Incomplete

from ..interfaces import (BusinessLocationState, ContactRate,
                          EssentialBusinessBaseLocation,
                          NonEssentialBusinessBaseLocation,
                          NonEssentialBusinessLocationState, SimTimeTuple)

class GroceryStoreState(BusinessLocationState):
    contact_rate: ContactRate
    open_time: SimTimeTuple
    def __init__(
        self, contact_rate, visitor_capacity, visitor_time, open_time
    ) -> None: ...

class GroceryStore(EssentialBusinessBaseLocation[GroceryStoreState]):
    state_type: Incomplete

class RetailStoreState(NonEssentialBusinessLocationState):
    contact_rate: ContactRate
    open_time: SimTimeTuple
    def __init__(
        self, contact_rate, visitor_capacity, visitor_time, open_time, locked
    ) -> None: ...

class RetailStore(NonEssentialBusinessBaseLocation[RetailStoreState]):
    state_type: Incomplete
