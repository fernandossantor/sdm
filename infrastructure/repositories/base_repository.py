from infrastructure.database.data_client import get_data_client
from infrastructure.database.database_schema import (
    ARTEFATOS_WORKFLOW,
    BRIEFINGS,
    PLANEJAMENTOS,
    PROJETOS,
)
from infrastructure.database.workspace_context import get_workspace


TABELAS_POR_ESPACO = {
    ARTEFATOS_WORKFLOW,
    BRIEFINGS,
    PLANEJAMENTOS,
    PROJETOS,
}


class BaseRepository:

    def __init__(self, db=None):

        self.db = db or get_data_client()

    @staticmethod
    def _com_espaco(tabela, registros):
        espaco_id = get_workspace()
        if tabela not in TABELAS_POR_ESPACO or not espaco_id:
            return registros
        if isinstance(registros, list):
            return [
                {**registro, "espaco_id": espaco_id}
                for registro in registros
            ]
        return {**registros, "espaco_id": espaco_id}

    @staticmethod
    def _filtrar_espaco(consulta, tabela):
        espaco_id = get_workspace()
        if tabela in TABELAS_POR_ESPACO and espaco_id:
            return consulta.eq("espaco_id", espaco_id)
        return consulta

    # =====================================================
    # SELECT
    # =====================================================

    def all(

        self,

        tabela,

        campos="*"

    ):

        consulta = self.db.table(tabela).select(campos)
        return self._filtrar_espaco(consulta, tabela).execute().data

    # =====================================================
    # SELECT + ORDER
    # =====================================================

    def ordered(

        self,

        tabela,

        campo,

        campos="*"

    ):

        consulta = self.db.table(tabela).select(campos)
        return (
            self._filtrar_espaco(consulta, tabela)
            .order(campo)
            .execute()
            .data
        )

    # =====================================================
    # BY ID
    # =====================================================

    def by_id(

        self,

        tabela,

        registro_id,

        campos="*"

    ):

        consulta = self.db.table(tabela).select(campos)
        return (
            self._filtrar_espaco(consulta, tabela)
            .eq("id", registro_id)
            .single()
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

        consulta = self.db.table(tabela).select(campos)
        consulta = self._filtrar_espaco(consulta, tabela).eq(campo, valor)

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

    # =====================================================
    # INSERT
    # =====================================================

    def insert(

        self,

        tabela,

        registros

    ):

        return (

            self.db

            .table(tabela)

            .insert(self._com_espaco(tabela, registros))

            .execute()

        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(

        self,

        tabela,

        campo,

        valor,

        dados

    ):

        return (

            self.db

            .table(tabela)

            .update(dados)

            .eq(campo, valor)

            .execute()

        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete(

        self,

        tabela,

        campo,

        valor

    ):

        return (

            self.db

            .table(tabela)

            .delete()

            .eq(campo, valor)

            .execute()

        )
