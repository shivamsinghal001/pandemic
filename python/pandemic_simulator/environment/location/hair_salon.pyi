from _typeshed import Incomplete

from ..interfaces import (ContactRate, NonEssentialBusinessBaseLocation,
                          NonEssentialBusinessLocationState, SimTimeTuple)

class HairSalonState(NonEssentialBusinessLocationState):
    contact_rate: ContactRate
    open_time: SimTimeTuple
    def __init__(
        self, contact_rate, visitor_capacity, visitor_time, open_time, locked
    ) -> None: ...

class HairSalon(NonEssentialBusinessBaseLocation[HairSalonState]):
    state_type: Incomplete
