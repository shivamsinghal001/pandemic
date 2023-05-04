from ..interfaces import PandemicTesting, PandemicTestResult, PersonState

class RandomPandemicTesting(PandemicTesting):
    def __init__(
        self,
        spontaneous_testing_rate: float = ...,
        symp_testing_rate: float = ...,
        critical_testing_rate: float = ...,
        testing_false_positive_rate: float = ...,
        testing_false_negative_rate: float = ...,
        retest_rate: float = ...,
    ) -> None: ...
    def admit_person(self, person_state: PersonState) -> bool: ...
    def test_person(self, person_state: PersonState) -> PandemicTestResult: ...
