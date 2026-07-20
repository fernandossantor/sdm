from dataclasses import fields

from repositories.campaign_objective_repository import CampaignObjectiveRepository
from domain.models.campaign_objective import CampaignObjective


class CampaignObjectiveService:

    def __init__(self):

        self.repository = CampaignObjectiveRepository()

    def load(self, campaign):

        return self.repository.get_by_campaign(campaign)

    def save(self, **kwargs):

        allowed_fields = {
            field.name
            for field in fields(CampaignObjective)
        }

        values = {
            key: value
            for key, value in kwargs.items()
            if key in allowed_fields
        }

        objective = CampaignObjective(**values)

        return self.repository.save(objective)
