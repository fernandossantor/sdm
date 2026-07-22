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

    def listar(self, projeto_id=None):

        if projeto_id:
            return self.by_field(BRIEFINGS, "projeto_id", projeto_id)

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

    def salvar(self, dados):
        return self.insert(BRIEFINGS, dados)

    def atualizar(self, briefing_id, dados):
        return self.update(BRIEFINGS, "id", briefing_id, dados)

    def excluir(self, briefing_id):
        return self.delete(BRIEFINGS, "id", briefing_id)
