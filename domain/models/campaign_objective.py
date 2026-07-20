from dataclasses import dataclass


@dataclass
class CampaignObjective:

    id: str = None

    campaign_id: str = None

    business_objective: str = ""

    communication_objective: str = ""

    media_objective: str = ""

    primary_kpi: str = ""

    secondary_kpis: str = ""

    conversion_goal: str = ""

    desired_reach: float = 0

    desired_frequency: float = 0

    desired_impressions: int = 0

    desired_clicks: int = 0

    desired_ctr: float = 0

    desired_cpm: float = 0

    desired_cpc: float = 0

    desired_cpa: float = 0

    desired_roas: float = 0

    observations: str = ""