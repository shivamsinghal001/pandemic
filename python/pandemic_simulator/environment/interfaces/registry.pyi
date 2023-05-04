import abc
from .ids import LocationID, PersonID
from .infection_model import InfectionSummary
from .location import Location, LocationSummary
from .pandemic_testing_result import PandemicTestResult
from .person import Person
from .sim_time import SimTime, SimTimeTuple
from abc import ABC, abstractmethod
from typing import List, Mapping, Optional, Set, Tuple, Union

class RegistrationError(Exception): ...

class Registry(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def register_location(self, location: Location) -> None: ...
    @abstractmethod
    def register_person(self, person: Person) -> None: ...
    @abstractmethod
    def register_person_entry_in_location(
        self, person_id: PersonID, location_id: LocationID
    ) -> bool: ...
    @abstractmethod
    def update_location_specific_information(self) -> None: ...
    @abstractmethod
    def reassign_locations(self, person: Person) -> None: ...
    @property
    @abstractmethod
    def person_ids(self) -> Set[PersonID]: ...
    @property
    @abstractmethod
    def location_ids(self) -> Set[LocationID]: ...
    @property
    @abstractmethod
    def location_ids_with_social_events(self) -> List[LocationID]: ...
    @property
    @abstractmethod
    def global_location_summary(self) -> Mapping[Tuple[str, str], LocationSummary]: ...
    @property
    @abstractmethod
    def location_types(self) -> Set[str]: ...
    @abstractmethod
    def location_ids_of_type(
        self, location_type: Union[type, Tuple[type, ...]]
    ) -> Tuple[LocationID, ...]: ...
    @abstractmethod
    def get_persons_in_location(self, location_id: LocationID) -> Set[PersonID]: ...
    @abstractmethod
    def location_id_to_type(self, location_id: LocationID) -> type: ...
    @abstractmethod
    def get_location_work_time(
        self, location_id: LocationID
    ) -> Optional[SimTimeTuple]: ...
    @abstractmethod
    def is_location_open_for_visitors(
        self, location_id: LocationID, sim_time: SimTime
    ) -> bool: ...
    @abstractmethod
    def get_person_home_id(self, person_id: PersonID) -> LocationID: ...
    @abstractmethod
    def get_households(self, person_id: PersonID) -> Set[PersonID]: ...
    @abstractmethod
    def get_person_infection_summary(
        self, person_id: PersonID
    ) -> Optional[InfectionSummary]: ...
    @abstractmethod
    def get_person_test_result(self, person_id: PersonID) -> PandemicTestResult: ...
    @abstractmethod
    def quarantine_person(self, person_id: PersonID) -> None: ...
    @abstractmethod
    def clear_quarantined(self, person_id: PersonID) -> None: ...
    @abstractmethod
    def get_person_quarantined_state(self, person_id: PersonID) -> bool: ...
