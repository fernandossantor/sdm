from datetime import datetime

from application.exceptions import ValidationError

from domain.models.campaign import Campaign

from repositories.campaign_repository import CampaignRepository


class CampaignService:

    def __init__(self):

        self.repository = CampaignRepository()


    def _generate_code(self):

        year = datetime.now().year

        campaigns = self.repository.list_all()

        total = len(campaigns) + 1

        return f"CMP-{year}-{total:04d}"


    def create(

        self,

        name,

        client,

        brand,

        product,

        objective,

        start_date,

        end_date,

        notes

    ):

        name = name.strip()

        if not name:

            raise ValidationError(

                "Informe o nome da campanha."

            )

        campaign = Campaign(

            code=self._generate_code(),

            name=name,

            client=client,

            brand=brand,

            product=product,

            objective=objective,

            start_date=start_date,

            end_date=end_date,

            notes=notes,

            status="draft"

        )

        return self.repository.save(campaign)


    def list(self):

        try:
            return self.repository.list_all()
        except Exception as exc:
            if (
                exc.__class__.__name__ == "APIError"
                and "PGRST205" in str(exc)
            ):
                return []

            raise


    def get(self, campaign_id):

        return self.repository.get(campaign_id)


    def update(self, campaign_id, values):

        return self.repository.update(

            campaign_id,

            values

        )


    def delete(self, campaign_id):

        return self.repository.delete(

            campaign_id

        )