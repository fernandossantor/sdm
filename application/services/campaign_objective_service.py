from repositories.campaign_objective_repository import CampaignObjectiveRepository

from domain.models.campaign_objective import CampaignObjective


class CampaignObjectiveService:

    def __init__(self):

        self.repository = CampaignObjectiveRepository()

    def load(self, campaign):

        return self.repository.get_by_campaign(campaign)

    def save(self, **kwargs):

        objective = CampaignObjective(**kwargs)

        return self.repository.save(objective)