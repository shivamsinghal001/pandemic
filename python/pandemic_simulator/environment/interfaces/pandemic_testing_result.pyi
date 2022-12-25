from enum import IntEnum

class PandemicTestResult(IntEnum):
    UNTESTED: int
    NEGATIVE: int
    POSITIVE: int
    CRITICAL: int
    DEAD: int
