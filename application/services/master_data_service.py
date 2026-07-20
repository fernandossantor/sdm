from repositories.master_repository import MasterRepository


class MasterDataService:

    def __init__(self, table):

        self.repository = MasterRepository(table)

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

    def get(self, record_id):

        return self.repository.get(record_id)

    def save(self, **kwargs):

        return self.repository.save(kwargs)

    def delete(self, record_id):

        self.repository.delete(record_id)