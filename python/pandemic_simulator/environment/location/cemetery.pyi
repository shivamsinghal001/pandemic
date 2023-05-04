from _typeshed import Incomplete

from ..interfaces import (BaseLocation, ContactRate, LocationRule,
                          LocationState, PersonID)

class CemeteryRule(LocationRule):
    def __post_init__(self) -> None: ...
    def __init__(self, contact_rate, visitor_time, visitor_capacity) -> None: ...

class CemeteryState(LocationState):
    contact_rate: ContactRate
    def __init__(self, contact_rate, visitor_capacity, visitor_time) -> None: ...

class Cemetery(BaseLocation[CemeteryState]):
    location_rule_type: Incomplete
    state_type: Incomplete
    def update_rules(self, new_rule: LocationRule) -> None: ...
    def remove_person_from_location(self, person_id: PersonID) -> None: ...
