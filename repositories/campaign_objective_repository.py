from infrastructure.database.admin_client import admin

from repositories.base_repository import BaseRepository


class CampaignObjectiveRepository(BaseRepository):

    def __init__(self):

        super().__init__("campaign_objectives")

    def get_by_campaign(self, campaign_id):

        response = (

            admin

            .table(self.table_name)

            .select("*")

            .eq("campaign_id", campaign_id)

            .limit(1)

            .execute()

        )

        if not response.data:

            return None

        return response.data[0]

    def save(self, objective):

        values = objective.__dict__

        existing = self.get_by_campaign(

            objective.campaign_id

        )

        if existing:

            return (

                admin

                .table(self.table_name)

                .update(values)

                .eq(

                    "campaign_id",

                    objective.campaign_id

                )

                .execute()

            ).data[0]

        return (

            admin

            .table(self.table_name)

            .insert(values)

            .execute()

        ).data[0]