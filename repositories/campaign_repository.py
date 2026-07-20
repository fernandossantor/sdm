from infrastructure.database.admin_client import admin

from repositories.base_repository import BaseRepository


class CampaignRepository(BaseRepository):

    def __init__(self):

        super().__init__("campaigns")


    def _serialize(self, value):

        if hasattr(value, "isoformat"):

            return value.isoformat()

        return value


    def save(self, campaign):

        response = (

            admin

            .table(self.table_name)

            .insert(

                {

                    "code": campaign.code,

                    "name": campaign.name,

                    "client": campaign.client,

                    "brand": campaign.brand,

                    "product": campaign.product,

                    "objective": campaign.objective,

                    "start_date": self._serialize(campaign.start_date),

                    "end_date": self._serialize(campaign.end_date),

                    "notes": campaign.notes,

                    "status": campaign.status

                }

            )

            .execute()

        )

        return response.data[0]


    def find_by_code(self, code):

        response = (

            admin

            .table(self.table_name)

            .select("*")

            .eq(
                "code",
                code
            )

            .limit(1)

            .execute()

        )

        if not response.data:
            return None

        return response.data[0]