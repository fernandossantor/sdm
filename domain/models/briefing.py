from dataclasses import dataclass
from datetime import date


@dataclass
class Briefing:

    id: str = None

    campaign_id: str = None

    company: str = ""

    market: str = ""

    product: str = ""

    category: str = ""

    positioning: str = ""

    differential: str = ""

    objectives: str = ""

    communication_problem: str = ""

    target_audience: str = ""

    competitors: str = ""

    budget: float = 0

    start_date: date = None

    end_date: date = None

    observations: str = ""

    created_at: str = None

    updated_at: str = None