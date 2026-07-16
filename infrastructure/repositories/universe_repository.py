from infrastructure.repositories.base_repository import (
    BaseRepository
)


UNIVERSOS = "universos"


class UniverseRepository(BaseRepository):

    def __init__(self):

        super().__init__()

    # =====================================================
    # LISTAR
    # =====================================================

    def listar(self):

        return self.ordered(

            UNIVERSOS,

            "nome"

        )

    # =====================================================
    # BUSCAR
    # =====================================================

    def buscar(

        self,

        universo_id

    ):

        return self.by_id(

            UNIVERSOS,

            universo_id

        )

    # =====================================================
    # SALVAR
    # =====================================================

    def salvar(

        self,

        dados

    ):

        return self.insert(

            UNIVERSOS,

            dados

        )

    # =====================================================
    # ATUALIZAR
    # =====================================================

    def atualizar(

        self,

        universo_id,

        dados

    ):

        return self.update(

            UNIVERSOS,

            "id",

            universo_id,

            dados

        )

    # =====================================================
    # EXCLUIR
    # =====================================================

    def excluir(

        self,

        universo_id

    ):

        return self.delete(

            UNIVERSOS,

            "id",

            universo_id

        )

    # =====================================================
    # ATIVOS
    # =====================================================

    def ativos(self):

        return self.by_field(

            UNIVERSOS,

            "ativo",

            True

        )

    # =====================================================
    # RESUMO
    # =====================================================

    def resumo(self):

        universos = self.listar()

        return {

            "total": len(

                universos

            ),

            "ativos": len(

                [

                    u

                    for u in universos

                    if u.get(

                        "ativo",

                        True

                    )

                ]

            )

        }