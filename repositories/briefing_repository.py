from infrastructure.database.admin_client import admin

from repositories.base_repository import BaseRepository


class BriefingRepository(BaseRepository):

    def __init__(self):

        super().__init__("briefings")


    def get_by_campaign(

        self,

        campaign_id

    ):

        response = (

            admin

            .table(self.table_name)

            .select("*")

            .eq(

                "campaign_id",

                campaign_id

            )

            .limit(1)

            .execute()

        )

        if not response.data:

            return None

        return response.data[0]


    def save(self, briefing):

        existing = self.get_by_campaign(

            briefing.campaign_id

        )

        values = {

            "campaign_id": briefing.campaign_id,

            "company": briefing.company,

            "market": briefing.market,

            "product": briefing.product,

            "category": briefing.category,

            "positioning": briefing.positioning,

            "differential": briefing.differential,

            "objectives": briefing.objectives,

            "communication_problem": briefing.communication_problem,

            "target_audience": briefing.target_audience,

            "competitors": briefing.competitors,

            "budget": briefing.budget,

            "start_date": briefing.start_date,

            "end_date": briefing.end_date,

            "observations": briefing.observations

        }

        if existing:

            return (

                admin

                .table(self.table_name)

                .update(values)

                .eq(

                    "campaign_id",

                    briefing.campaign_id

                )

                .execute()

            ).data[0]

        return (

            admin

            .table(self.table_name)

            .insert(values)

            .execute()

        ).data[0]