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

    def interesses_afinidade(self):

        try:
            return self.all(INTERESSES_AMBIENTES_AFINIDADE)
        except Exception:
            return []

    def precos(self):

        try:
            return self.by_field(PRECOS_INVENTARIO, "ativo", True)
        except Exception:
            return []

    def papeis_inventarios(self, campanha_ref):

        try:
            return (
                self.db.table(INVENTARIOS_PAPEIS)
                .select("*")
                .eq("campanha_ref", campanha_ref)
                .eq("selecionado", True)
                .execute()
                .data
            )
        except Exception:
            return []

    @staticmethod
    def campanha_ref(briefing):

        if isinstance(briefing, dict):
            if briefing.get("id"):
                return f"briefing:{briefing['id']}"
            nome = briefing.get("nome") or briefing.get("campanha") or "sem-nome"
        else:
            nome = getattr(briefing, "campanha", "sem-nome")
        return f"sessao:{nome}"

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

                self.consumo(),

            "interesses_afinidade": self.interesses_afinidade(),

            "precos": self.precos(),

            "papeis_inventarios": self.papeis_inventarios(
                self.campanha_ref(briefing)
            ),

        }

    # =====================================================
    # CONTEXTO A PARTIR DE UM BRIEFING
    # =====================================================

    def carregar_contexto_por_objeto(

        self,

        briefing

    ):

        def valor(nome, padrao=None):
            if isinstance(briefing, dict):
                return briefing.get(nome, padrao)
            return getattr(briefing, nome, padrao)

        objetivo_id = valor("objetivo_id")

        if not objetivo_id:
            raise ValueError("O briefing selecionado não possui objetivo_id.")

        objetivo = self.objetivo(objetivo_id)

        audiencias = []

        #
        # Compatibilidade
        #
        # Briefing antigo
        #

        audiencia_id = valor("audiencia_id")

        if audiencia_id:

            audiencia = self.audiencia(

                audiencia_id

            )

            if audiencia:

                audiencias.append(
                    {
                        "audiencia_id": audiencia["id"],
                        "peso": 100.0,
                    }
                )

        #
        # Novo Briefing
        #

        publicos = valor("publicos", []) or []

        if not audiencia_id:

            for publico in publicos:

                if isinstance(

                    publico,

                    dict

                ) and "id" in publico:

                    audiencias.append(
                        {
                            "audiencia_id": publico.get(
                                "audiencia_id",
                                publico["id"],
                            ),
                            "peso": float(publico.get("peso", 100)),
                            "interesses": publico.get("interesses", []),
                            "jornada": publico.get("jornada"),
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

                self.consumo(),

            "interesses_afinidade": self.interesses_afinidade(),

            "precos": self.precos(),

            "papeis_inventarios": self.papeis_inventarios(
                self.campanha_ref(briefing)
            ),

        }
