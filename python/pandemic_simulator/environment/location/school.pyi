from ..interfaces import ContactRate, NonEssentialBusinessBaseLocation, NonEssentialBusinessLocationState, SimTimeTuple
from _typeshed import Incomplete

class SchoolState(NonEssentialBusinessLocationState):
    contact_rate: ContactRate
    open_time: SimTimeTuple
    def __init__(self, contact_rate, visitor_capacity, visitor_time, open_time, locked) -> None: ...

class School(NonEssentialBusinessBaseLocation[SchoolState]):
    state_type: Incomplete
