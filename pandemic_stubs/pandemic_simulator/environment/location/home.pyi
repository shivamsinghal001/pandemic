from ..interfaces import BaseLocation, ContactRate, LocationRule, LocationState, SimTime
from _typeshed import Incomplete

class HomeState(LocationState):
    contact_rate: ContactRate
    visitor_time: Incomplete
    def __init__(self, contact_rate, visitor_capacity, visitor_time) -> None: ...

class Home(BaseLocation[HomeState]):
    state_type: Incomplete
    def sync(self, sim_time: SimTime) -> None: ...
    def update_rules(self, new_rule: LocationRule) -> None: ...
