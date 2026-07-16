from infrastructure.database.database_schema import *

from infrastructure.repositories.base_repository import (
    BaseRepository
)


class BriefingRepository(BaseRepository):

    def __init__(self):

        super().__init__()

    # =====================================================
    # LISTAR
    # =====================================================

    def listar(self):

        return self.ordered(

            BRIEFINGS,

            "nome"

        )

    # =====================================================
    # BUSCAR POR NOME
    # =====================================================

    def buscar(

        self,

        nome

    ):

        return self.by_field(

            BRIEFINGS,

            "nome",

            nome,

            single=True

        )

    # =====================================================
    # BUSCAR POR ID
    # =====================================================

    def buscar_por_id(

        self,

        briefing_id

    ):

        return self.by_id(

            BRIEFINGS,

            briefing_id

        )