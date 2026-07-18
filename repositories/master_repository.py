from infrastructure.database.admin_client import admin

from repositories.base_repository import BaseRepository


class MasterRepository(BaseRepository):

    def __init__(self, table_name):

        super().__init__(table_name)

    def save(self, values):

        if values.get("id"):

            return (

                admin

                .table(self.table_name)

                .update(values)

                .eq("id", values["id"])

                .execute()

            ).data[0]

        return (

            admin

            .table(self.table_name)

            .insert(values)

            .execute()

        ).data[0]