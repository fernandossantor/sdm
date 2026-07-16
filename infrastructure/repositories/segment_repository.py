from infrastructure.repositories.base_repository import (
    BaseRepository
)


SEGMENTOS = "segmentos"


class SegmentRepository(BaseRepository):

    def __init__(self):

        super().__init__()

    # =====================================================
    # LISTAR
    # =====================================================

    def listar(self):

        return self.ordered(

            SEGMENTOS,

            "nome"

        )

    # =====================================================
    # BUSCAR
    # =====================================================

    def buscar(

        self,

        segmento_id

    ):

        return self.by_id(

            SEGMENTOS,

            segmento_id

        )

    # =====================================================
    # POR UNIVERSO
    # =====================================================

    def listar_por_universo(

        self,

        universo_id

    ):

        return self.by_field(

            SEGMENTOS,

            "universo_id",

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

            SEGMENTOS,

            dados

        )

    # =====================================================
    # ATUALIZAR
    # =====================================================

    def atualizar(

        self,

        segmento_id,

        dados

    ):

        return self.update(

            SEGMENTOS,

            "id",

            segmento_id,

            dados

        )

    # =====================================================
    # EXCLUIR
    # =====================================================

    def excluir(

        self,

        segmento_id

    ):

        return self.delete(

            SEGMENTOS,

            "id",

            segmento_id

        )