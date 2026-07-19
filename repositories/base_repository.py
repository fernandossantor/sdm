from infrastructure.database.admin_client import admin


class BaseRepository:
    """Repository base compatível com a arquitetura nova e legada."""

    def __init__(self, table_name=None):
        self.table_name = table_name
        self.db = admin

    def _resolve_table(self, table_name=None):
        table = table_name or self.table_name

        if not table:
            raise ValueError(
                "table_name não informado para o repository."
            )

        return table

    # =====================================================
    # API nova
    # =====================================================

    def list_all(self, order_by="created_at", desc=True):
        table = self._resolve_table()

        response = (
            self.db
            .table(table)
            .select("*")
            .order(
                order_by,
                desc=desc,
            )
            .execute()
        )

        return response.data

    def get(self, entity_id):
        table = self._resolve_table()

        response = (
            self.db
            .table(table)
            .select("*")
            .eq(
                "id",
                entity_id,
            )
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    def create(self, values):
        table = self._resolve_table()

        response = (
            self.db
            .table(table)
            .insert(values)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    def update(self, entity_id, values):
        table = self._resolve_table()

        response = (
            self.db
            .table(table)
            .update(values)
            .eq(
                "id",
                entity_id,
            )
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    def delete(self, entity_id):
        table = self._resolve_table()

        return (
            self.db
            .table(table)
            .delete()
            .eq(
                "id",
                entity_id,
            )
            .execute()
        )

    # =====================================================
    # API legada
    # =====================================================

    def all(
        self,
        tabela,
        campos="*",
    ):
        return (
            self.db
            .table(tabela)
            .select(campos)
            .execute()
            .data
        )

    def ordered(
        self,
        tabela,
        campo,
        campos="*",
    ):
        return (
            self.db
            .table(tabela)
            .select(campos)
            .order(campo)
            .execute()
            .data
        )

    def by_id(
        self,
        tabela,
        registro_id,
        campos="*",
    ):
        return (
            self.db
            .table(tabela)
            .select(campos)
            .eq(
                "id",
                registro_id,
            )
            .single()
            .execute()
            .data
        )

    def by_field(
        self,
        tabela,
        campo,
        valor,
        campos="*",
        single=False,
    ):
        consulta = (
            self.db
            .table(tabela)
            .select(campos)
            .eq(
                campo,
                valor,
            )
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

    def insert(
        self,
        tabela,
        registros,
    ):
        return (
            self.db
            .table(tabela)
            .insert(registros)
            .execute()
        )

    def update_by_field(
        self,
        tabela,
        campo,
        valor,
        dados,
    ):
        return (
            self.db
            .table(tabela)
            .update(dados)
            .eq(
                campo,
                valor,
            )
            .execute()
        )

    def delete_by_field(
        self,
        tabela,
        campo,
        valor,
    ):
        return (
            self.db
            .table(tabela)
            .delete()
            .eq(
                campo,
                valor,
            )
            .execute()
        )
