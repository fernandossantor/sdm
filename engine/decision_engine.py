from engine.briefing_engine import (
    obter_audiencias,
    obter_briefing,
    obter_objetivo,
)

from engine.models import (
    DecisionContext,
)


class DecisionEngine:
    """
    Responsável apenas por construir o contexto de decisão.

    Não calcula score.
    Não ordena ranking.
    Não distribui verba.
    Não monta plano.
    """

    # ==========================================================
    # API PRINCIPAL
    # ==========================================================

    def executar(
        self,
        briefing,
    ) -> DecisionContext:
        return self.construir_contexto(
            briefing
        )

    # ==========================================================
    # COMPATIBILIDADE
    # ==========================================================

    def decidir(
        self,
        briefing,
    ) -> DecisionContext:
        """
        Compatibilidade temporária com fluxos antigos.

        Antes retornava DecisionResult.
        Agora retorna DecisionContext.
        """

        return self.construir_contexto(
            briefing
        )

    # ==========================================================
    # CONTEXTO
    # ==========================================================

    def construir_contexto(
        self,
        briefing,
    ) -> DecisionContext:
        briefing_data = self._carregar_briefing(
            briefing
        )

        objetivo_id = self._valor(
            briefing_data,
            "objetivo_id",
        )

        briefing_id = self._valor(
            briefing_data,
            "id",
        )

        objetivo = self._valor(
            briefing_data,
            "objetivo",
            None,
        )

        if objetivo is None:
            objetivo = self._carregar_objetivo(
                objetivo_id
            )

        audiencias = self._valor(
            briefing_data,
            "audiencias",
            None,
        )

        if audiencias is None:
            audiencias = self._carregar_audiencias(
                briefing_id
            )

        return DecisionContext(
            briefing=briefing_data,
            objetivo=objetivo,
            audiencias=audiencias,
            inventarios=self._valor(
                briefing_data,
                "inventarios",
                [],
            ),
            inventarios_objetivos=self._valor(
                briefing_data,
                "inventarios_objetivos",
                [],
            ),
            inventarios_kpis=self._valor(
                briefing_data,
                "inventarios_kpis",
                [],
            ),
            metricas=self._valor(
                briefing_data,
                "metricas",
                [],
            ),
            consumo=self._valor(
                briefing_data,
                "consumo",
                [],
            ),
            parametros=self._valor(
                briefing_data,
                "parametros",
                {},
            ),
            restricoes=self._valor(
                briefing_data,
                "restricoes",
                [],
            ),
        )

    # ==========================================================
    # CARREGAMENTO
    # ==========================================================

    def _carregar_briefing(
        self,
        briefing,
    ):
        if isinstance(
            briefing,
            dict,
        ):
            return briefing

        if hasattr(
            briefing,
            "__dict__",
        ) and not isinstance(
            briefing,
            str,
        ):
            return briefing

        return obter_briefing(
            briefing
        )

    def _carregar_objetivo(
        self,
        objetivo_id,
    ):
        if not objetivo_id:
            return {}

        return obter_objetivo(
            objetivo_id
        )

    def _carregar_audiencias(
        self,
        briefing_id,
    ):
        if not briefing_id:
            return []

        return obter_audiencias(
            briefing_id
        )

    # ==========================================================
    # UTIL
    # ==========================================================

    @staticmethod
    def _valor(
        objeto,
        chave,
        padrao=None,
    ):
        if isinstance(
            objeto,
            dict,
        ):
            return objeto.get(
                chave,
                padrao,
            )

        return getattr(
            objeto,
            chave,
            padrao,
        )
