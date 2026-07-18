from infrastructure.database.admin_client import admin


class BaseRepository:

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.table = admin.table(table_name)

    def list_all(self, order_by="created_at", desc=True):

        response = (

            admin

            .table(self.table_name)

            .select("*")

            .order(
                order_by,
                desc=desc
            )

            .execute()

        )

        return response.data

    # =====================================================
    # SELECT + ORDER
    # =====================================================

    def ordered(

        self,

        tabela,

        campo,

        campos="*"

    ):

        return (

            self.db

            .table(tabela)

            .select(campos)

            .order(campo)

            .execute()

            .data

        )

    # =====================================================
    # BY FIELD
    # =====================================================

    def by_field(

        self,

        tabela,

        campo,

        valor,

        campos="*",

        single=False

    ):

        consulta = (

            self.db

            .table(tabela)

            .select(campos)

            .eq(campo, valor)

        )

        if single:

            return (

                consulta

                .single()

                .execute()

                .data

            )

        return (

            consulta

            .execute()

            .data

        )

    def get(self, entity_id):

        response = (

            admin

            .table(self.table_name)

            .select("*")

            .eq(
                "id",
                entity_id
            )

            .limit(1)

            .execute()

        )

        if not response.data:
            return None

        return response.data[0]

    def delete(self, entity_id):

        return (

            admin

            .table(self.table_name)

            .delete()

            .eq(
                "id",
                entity_id
            )

            .execute()

        )

    def update(self, entity_id, values: dict):

        response = (

            admin

            .table(self.table_name)

            .update(values)

            .eq(
                "id",
                entity_id
            )

            .execute()

        )

        if not response.data:
            return None

        return response.data[0]