from typing import List

from sdm.engine.briefing_engine import (
    obter_audiencias,
    obter_briefing,
    obter_objetivo,
)

from sdm.engine.models import (
    DecisionContext,
    DecisionItem,
    DecisionResult,
)


class DecisionEngine:
    """
    Motor central de decisão do SDM.

    Responsabilidades:

    - montar o contexto da decisão
    - calcular scores
    - ordenar inventários
    - produzir justificativas
    - entregar um DecisionResult
    """

    def __init__(self):
        pass

    # ==========================================================
    # CONTEXTO
    # ==========================================================

    def construir_contexto(self, briefing_id) -> DecisionContext:

        briefing = obter_briefing(briefing_id)

        objetivo = obter_objetivo(briefing)

        audiencias = obter_audiencias(briefing)

        inventarios = briefing.get("inventarios", [])

        inventarios_objetivos = briefing.get(
            "inventarios_objetivos", []
        )

        inventarios_kpis = briefing.get(
            "inventarios_kpis", []
        )

        metricas = briefing.get("metricas", [])

        consumo = briefing.get("consumo", [])

        parametros = briefing.get("parametros", {})

        restricoes = briefing.get("restricoes", [])

        return DecisionContext(
            briefing=briefing,
            objetivo=objetivo,
            audiencias=audiencias,
            inventarios=inventarios,
            inventarios_objetivos=inventarios_objetivos,
            inventarios_kpis=inventarios_kpis,
            metricas=metricas,
            consumo=consumo,
            parametros=parametros,
            restricoes=restricoes,
        )

    # ==========================================================
    # SCORE
    # ==========================================================

    def calcular_score(
        self,
        inventario: dict,
        contexto: DecisionContext,
    ) -> float:

        score = 0.0

        score += inventario.get("score_objetivo", 0)

        score += inventario.get("score_kpi", 0)

        score += inventario.get("score_publico", 0)

        score += inventario.get("score_contexto", 0)

        score += inventario.get("score_consumo", 0)

        score += inventario.get("score_sinergia", 0)

        score -= inventario.get("penalidade", 0)

        return round(score, 2)

    # ==========================================================
    # JUSTIFICATIVAS
    # ==========================================================

    def gerar_justificativas(
        self,
        inventario: dict,
    ) -> List[str]:

        justificativas = []

        if inventario.get("score_publico", 0) > 15:
            justificativas.append(
                "Alta aderência ao público."
            )

        if inventario.get("score_objetivo", 0) > 15:
            justificativas.append(
                "Compatível com o objetivo da campanha."
            )

        if inventario.get("score_kpi", 0) > 15:
            justificativas.append(
                "Favorece o KPI principal."
            )

        if inventario.get("score_sinergia", 0) > 0:
            justificativas.append(
                "Possui boa sinergia com outros canais."
            )

        return justificativas

    # ==========================================================
    # DECISÃO
    # ==========================================================

    def decidir(
        self,
        briefing_id,
    ) -> DecisionResult:

        contexto = self.construir_contexto(
            briefing_id
        )

        decisoes = []

        for inventario in contexto.inventarios:

            score = self.calcular_score(
                inventario,
                contexto,
            )

            decisoes.append(
                DecisionItem(
                    inventario=inventario["nome"],
                    plataforma=inventario.get(
                        "plataforma",
                        "",
                    ),
                    ambiente=inventario.get(
                        "ambiente",
                        "",
                    ),
                    score=score,
                    papel="Recomendado",
                    prioridade=0,
                    confianca=min(score, 100),
                    justificativas=self.gerar_justificativas(
                        inventario
                    ),
                )
            )

        decisoes.sort(
            key=lambda x: x.score,
            reverse=True,
        )

        for indice, decisao in enumerate(
            decisoes,
            start=1,
        ):
            decisao.prioridade = indice

        return DecisionResult(
            decisoes=decisoes,
            score_global=(
                sum(d.score for d in decisoes)
                / len(decisoes)
                if decisoes
                else 0
            ),
            observacoes=[],
            alertas=[],
            erros=[],
        )