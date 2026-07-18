from domain.models.briefing import Briefing

from repositories.briefing_repository import BriefingRepository


class BriefingService:

    def __init__(self):

        self.repository = BriefingRepository()


    def load(

        self,

        campaign_id

    ):

        return self.repository.get_by_campaign(

            campaign_id

        )


    def save(

        self,

        **kwargs

    ):

        briefing = Briefing(

            **kwargs

        )

        return self.repository.save(

            briefing

        )