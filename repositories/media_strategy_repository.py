from infrastructure.database.admin_client import admin

from repositories.base_repository import BaseRepository


class MediaStrategyRepository(BaseRepository):

    def __init__(self):

        super().__init__("media_strategy")

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

    def save(self, strategy):

        values = self.clean_data(strategy.__dict__)

        existing = self.get_by_campaign(
            strategy.campaign_id
        )

        if existing:

            return (

                admin

                .table(self.table_name)

                .update(values)

                .eq(
                    "campaign_id",
                    strategy.campaign_id
                )

                .execute()

            ).data[0]

        return (

            admin

            .table(self.table_name)

            .insert(values)

            .execute()

        ).data[0]