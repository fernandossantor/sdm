from infrastructure.repositories.base_repository import (
    BaseRepository
)
from infrastructure.database.database_schema import (
    BIBLIOTECA_PUBLICOS,
    BIBLIOTECA_PUBLICOS_INTERESSES,
    BIBLIOTECA_PUBLICOS_JORNADAS,
    BIBLIOTECA_PUBLICOS_SEGMENTOS,
)


# =====================================================
# TABELAS
# =====================================================

PUBLICOS = BIBLIOTECA_PUBLICOS

PUBLICOS_SEGMENTOS = BIBLIOTECA_PUBLICOS_SEGMENTOS

PUBLICOS_INTERESSES = BIBLIOTECA_PUBLICOS_INTERESSES

PUBLICOS_JORNADAS = BIBLIOTECA_PUBLICOS_JORNADAS


class PublicRepository(BaseRepository):

    def __init__(self):

        super().__init__()

    # =====================================================
    # PÚBLICOS
    # =====================================================

    def listar(self):

        return self.ordered(

            PUBLICOS,

            "nome"

        )

    def buscar(

        self,

        publico_id

    ):

        return self.by_id(

            PUBLICOS,

            publico_id

        )

    def salvar(

        self,

        dados

    ):

        return self.insert(

            PUBLICOS,

            dados

        )

    def atualizar(

        self,

        publico_id,

        dados

    ):

        return self.update(

            PUBLICOS,

            "id",

            publico_id,

            dados

        )

    def excluir(

        self,

        publico_id

    ):

        #
        # Remove segmentos
        #

        self.delete(

            PUBLICOS_SEGMENTOS,

            "publico_id",

            publico_id

        )

        #
        # Remove interesses
        #

        self.delete(

            PUBLICOS_INTERESSES,

            "publico_id",

            publico_id

        )

        self.delete(

            PUBLICOS_JORNADAS,

            "publico_id",

            publico_id

        )

        #
        # Remove o público
        #

        return self.delete(

            PUBLICOS,

            "id",

            publico_id

        )

    # =====================================================
    # SEGMENTOS
    # =====================================================

    def segmentos(

        self,

        publico_id

    ):

        return self.by_field(

            PUBLICOS_SEGMENTOS,

            "publico_id",

            publico_id

        )

    def salvar_segmentos(

        self,

        registros

    ):

        if registros:

            self.insert(

                PUBLICOS_SEGMENTOS,

                registros

            )

    # =====================================================
    # INTERESSES
    # =====================================================

    def interesses(

        self,

        publico_id

    ):

        return self.by_field(

            PUBLICOS_INTERESSES,

            "publico_id",

            publico_id

        )

    def salvar_interesses(

        self,

        registros

    ):

        if registros:

            self.insert(

                PUBLICOS_INTERESSES,

                registros

            )

    # =====================================================
    # JORNADA
    # =====================================================

    def jornadas(self, publico_id):

        return self.by_field(

            PUBLICOS_JORNADAS,

            "publico_id",

            publico_id

        )

    def salvar_jornada(self, publico_id, jornada_id):

        return self.insert(

            PUBLICOS_JORNADAS,

            {

                "publico_id": publico_id,

                "jornada_id": jornada_id

            }

        )
