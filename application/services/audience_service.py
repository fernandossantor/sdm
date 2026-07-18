from repositories.audience_repository import AudienceRepository

from domain.models.audience import Audience


class AudienceService:

    def __init__(self):

        self.repository = AudienceRepository()

    def load(self, campaign_id):

        return self.repository.get_by_campaign(
            campaign_id
        )

    def save(self, **kwargs):

        audience = Audience(
            **kwargs
        )

        return self.repository.save(
            audience
        )