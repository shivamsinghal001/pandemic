import abc
from abc import ABC, abstractmethod
from typing import Dict

from .infection_model import InfectionSummary
from .pandemic_testing_result import PandemicTestResult
from .person import PersonState

class GlobalTestingState:
    summary: Dict[InfectionSummary, int]
    num_tests: int
    def __init__(self, summary, num_tests) -> None: ...

class PandemicTesting(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def admit_person(self, person_state: PersonState) -> bool: ...
    @abstractmethod
    def test_person(self, person_state: PersonState) -> PandemicTestResult: ...
