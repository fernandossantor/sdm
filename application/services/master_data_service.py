from repositories.master_repository import MasterRepository


class MasterDataService:

    def __init__(self, table):

        self.repository = MasterRepository(table)

    def list(self):

        return self.repository.list_all()

    def get(self, record_id):

        return self.repository.get(record_id)

    def save(self, **kwargs):

        return self.repository.save(kwargs)

    def delete(self, record_id):

        self.repository.delete(record_id)