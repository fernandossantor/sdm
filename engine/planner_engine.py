from engine.decision_engine import DecisionEngine

from engine.models import (
    AmbientePlano,
    DecisionResult,
    InventarioPlano,
)


class PlannerEngine:

    """
    Responsável apenas pelo planejamento.

    Toda a inteligência fica no DecisionEngine.
    """

    def __init__(self):

        self.decision_engine = DecisionEngine()

    # =====================================================
    # GERAÇÃO DO PLANO
    # =====================================================

    def gerar_plano(
        self,
        briefing_id,
    ):

        resultado = self.decision_engine.decidir(
            briefing_id
        )

        return self._montar_plano(resultado)

    # =====================================================
    # PLANO
    # =====================================================

    def _montar_plano(
        self,
        resultado: DecisionResult,
    ):

        ambientes = {}

        inventarios = []

        verba_total = resultado.verba_total

        for decisao in resultado.decisoes:

            inventario = InventarioPlano(

                inventario=decisao.inventario,

                plataforma=decisao.plataforma,

                ambiente=decisao.ambiente,

                score=decisao.score,

                percentual=decisao.percentual,

                verba=decisao.verba,

                papel=decisao.papel,

                justificativas=decisao.justificativas,

            )

            inventarios.append(inventario)

            if decisao.ambiente not in ambientes:

                ambientes[decisao.ambiente] = AmbientePlano(

                    ambiente=decisao.ambiente,

                    score=0,

                    percentual=0,

                    verba=0,

                    papel=decisao.papel,

                )

            ambiente = ambientes[decisao.ambiente]

            ambiente.verba += decisao.verba

            ambiente.percentual += decisao.percentual

            ambiente.score = max(
                ambiente.score,
                decisao.score,
            )

        return {

            "inventarios": inventarios,

            "ambientes": list(ambientes.values()),

            "verba_total": verba_total,

            "score_global": resultado.score_global,

            "observacoes": resultado.observacoes,

            "alertas": resultado.alertas,

            "erros": resultado.erros,

        }