from ..interfaces import (
    AgeRestrictedBusinessBaseLocation,
    ContactRate,
    NonEssentialBusinessLocationState,
    SimTimeTuple,
)
from _typeshed import Incomplete

class OfficeState(NonEssentialBusinessLocationState):
    contact_rate: ContactRate
    open_time: SimTimeTuple
    def __init__(
        self, contact_rate, visitor_capacity, visitor_time, open_time, locked
    ) -> None: ...

class Office(AgeRestrictedBusinessBaseLocation[OfficeState]):
    state_type: Incomplete
    age_limits: Incomplete
