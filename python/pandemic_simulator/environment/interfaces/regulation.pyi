from typing import Any, Dict, List, Optional, Type, Union

from .infection_model import Risk
from .pandemic_types import Default

class PandemicRegulation:
    location_type_to_rule_kwargs: Optional[Dict[Type, Dict[str, Any]]]
    business_type_to_rule_kwargs: Optional[Dict[Type, Dict[str, Any]]]
    social_distancing: Union[float, Default, None]
    quarantine: bool
    quarantine_if_contact_positive: bool
    quarantine_if_household_quarantined: bool
    stay_home_if_sick: bool
    practice_good_hygiene: bool
    wear_facial_coverings: bool
    risk_to_avoid_gathering_size: Dict[Risk, int]
    risk_to_avoid_location_types: Optional[Dict[Risk, List[type]]]
    stage: int
    def __init__(
        self,
        location_type_to_rule_kwargs,
        business_type_to_rule_kwargs,
        social_distancing,
        quarantine,
        quarantine_if_contact_positive,
        quarantine_if_household_quarantined,
        stay_home_if_sick,
        practice_good_hygiene,
        wear_facial_coverings,
        risk_to_avoid_gathering_size,
        risk_to_avoid_location_types,
        stage,
    ) -> None: ...
