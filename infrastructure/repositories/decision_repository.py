from infrastructure.database.database_schema import *

from infrastructure.repositories.base_repository import (
    BaseRepository
)


class DecisionRepository(BaseRepository):

    def __init__(self):

        super().__init__()

    # =====================================================
    # BRIEFINGS
    # =====================================================

    def listar_briefings(self):

        return self.ordered(

            BRIEFINGS,

            "nome"

        )

    def briefing(self, nome):

        return self.by_field(

            BRIEFINGS,

            "nome",

            nome,

            single=True

        )

    # =====================================================
    # OBJETIVOS
    # =====================================================

    def objetivo(self, objetivo_id):

        return self.by_id(

            OBJETIVOS,

            objetivo_id

        )

    # =====================================================
    # KPIs
    # =====================================================

    def kpis(self):

        return self.ordered(

            KPIS,

            "nome"

        )

    # =====================================================
    # AUDIÊNCIAS
    # =====================================================

    # =====================================================
    # AUDIÊNCIAS V3
    # =====================================================

    def audiencias(
        self,
        briefing_id
    ):

        campos = """
            audiencia_id,
            peso,
            observacao,
            audiencias_v3(
                id,
                nome,
                descricao,
                faixa_etaria
            )
        """

        return (
            self.db
            .table(
                "briefing_audiencias_v3"
            )
            .select(
                campos
            )
            .eq(
                "briefing_id",
                briefing_id
            )
            .execute()
            .data
        )

    def audiencia(self, audiencia_id):

        return self.by_id(

            AUDIENCIAS,

            audiencia_id

        )

    # =====================================================
    # INVENTÁRIOS
    # =====================================================

    def inventarios(self):

        campos = """

            id,

            nome,

            descricao,

            plataforma_id,

            ambiente_id,

            formato_id,

            plataformas_v3(

                id,

                nome

            ),

            ambientes_v3(

                id,

                nome

            ),

            formatos_v3(

                id,

                nome

            )

        """

        return self.ordered(

            INVENTARIOS,

            "nome",

            campos

        )

    # =====================================================
    # RELACIONAMENTOS
    # =====================================================

    def inventarios_objetivos(self):

        return self.all(

            INVENTARIOS_OBJETIVOS

        )

    def inventarios_kpis(self):

        return self.all(

            INVENTARIOS_KPIS

        )

    def metricas(self):

        return self.all(

            INVENTARIOS_METRICAS

        )

    def consumo(self):

        return self.all(

            CONSUMO

        )

    # =====================================================
    # CONTEXTO
    # =====================================================

    def carregar_contexto(

        self,

        nome_briefing

    ):

        briefing = self.briefing(

            nome_briefing

        )

        return {

            "briefing": briefing,

            "objetivo": self.objetivo(

                briefing["objetivo_id"]

            ),

            "kpis": self.kpis(),

            "audiencias": self.audiencias(

                briefing["id"]

            ),

            "inventarios": self.inventarios(),

            "inventarios_objetivos":

                self.inventarios_objetivos(),

            "inventarios_kpis":

                self.inventarios_kpis(),

            "metricas":

                self.metricas(),

            "consumo":

                self.consumo()

        }

    # =====================================================
    # CONTEXTO A PARTIR DE UM BRIEFING
    # =====================================================

    def carregar_contexto_por_objeto(

        self,

        briefing

    ):

        objetivo = self.objetivo(

            briefing.objetivo_id

        )

        audiencias = []

        #
        # Compatibilidade
        #
        # Briefing antigo
        #

        if hasattr(

            briefing,

            "audiencia_id"

        ) and briefing.audiencia_id:

            audiencia = self.audiencia(

                briefing.audiencia_id

            )

            if audiencia:

                audiencias.append(
                    {
                        "audiencia_id": publico["id"],
                        "peso": float(
                            publico.get(
                                "peso",
                                100
                            )
                        )
                    }
                )

        #
        # Novo Briefing
        #

        elif hasattr(

            briefing,

            "publicos"

        ):

            for publico in briefing.publicos:

                if isinstance(

                    publico,

                    dict

                ) and "id" in publico:

                    audiencias.append(
                        {
                            "audiencia_id": audiencia["id"],
                            "peso": 100.0
                        }
                    )

        return {

            "briefing": briefing,

            "objetivo": objetivo,

            "kpis": self.kpis(),

            "audiencias": audiencias,

            "inventarios": self.inventarios(),

            "inventarios_objetivos":

                self.inventarios_objetivos(),

            "inventarios_kpis":

                self.inventarios_kpis(),

            "metricas":

                self.metricas(),

            "consumo":

                self.consumo()

        }