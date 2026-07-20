from dataclasses import dataclass
from datetime import date


@dataclass
class Audience:

    id: str = None

    campaign_id: str = None

    target_name: str = ""

    gender: str = ""

    age_min: int = 18

    age_max: int = 65

    social_class: str = ""

    income: str = ""

    education: str = ""

    occupation: str = ""

    city: str = ""

    state: str = ""

    region: str = ""

    interests: str = ""

    habits: str = ""

    pain_points: str = ""

    media_consumption: str = ""

    devices: str = ""

    observations: str = ""