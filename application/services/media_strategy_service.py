from repositories.media_strategy_repository import MediaStrategyRepository

from domain.models.media_strategy import MediaStrategy


class MediaStrategyService:

    def __init__(self):

        self.repository = MediaStrategyRepository()

    def load(self, campaign_id):

        return self.repository.get_by_campaign(
            campaign_id
        )

    def save(self, **kwargs):

        strategy = MediaStrategy(**kwargs)

        return self.repository.save(strategy)