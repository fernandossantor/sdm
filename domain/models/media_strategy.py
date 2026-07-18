from dataclasses import dataclass


@dataclass
class MediaStrategy:

    id: str = None

    campaign_id: str = None

    strategy_type: str = ""

    purchase_model: str = ""

    campaign_type: str = ""

    coverage_scope: str = ""

    communication_phase: str = ""

    priority: str = ""

    budget_distribution: str = ""

    channel_mix: str = ""

    observations: str = ""