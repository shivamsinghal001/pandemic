from typing import Set

from _typeshed import Incomplete

from ..interfaces import (BusinessBaseLocation, BusinessLocationState,
                          PersonID, SimTimeTuple)

class HospitalState(BusinessLocationState):
    patient_capacity: int
    patients_in_location: Set[PersonID]
    num_admitted_patients: int
    open_time: SimTimeTuple
    @property
    def persons_in_location(self) -> Set[PersonID]: ...
    def __init__(
        self, contact_rate, visitor_capacity, visitor_time, patient_capacity
    ) -> None: ...

class Hospital(BusinessBaseLocation[HospitalState]):
    state_type: Incomplete
    def is_entry_allowed(self, person_id: PersonID) -> bool: ...
    def add_person_to_location(self, person_id: PersonID) -> None: ...
    def remove_person_from_location(self, person_id: PersonID) -> None: ...
    def get_worker_work_time(self) -> SimTimeTuple: ...
