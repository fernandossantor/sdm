from engine.models import (
    AmbientePlano,
    DecisionResult,
    InventarioPlano,
)


class PlannerEngine:
    """
    Responsável apenas pela montagem do plano.

    Não carrega briefing.
    Não chama DecisionEngine.
    Não calcula score.
    Não distribui orçamento.
    """

    # =====================================================
    # API PRINCIPAL
    # =====================================================

    def executar(
        self,
        briefing=None,
        decision=None,
        plano_tatico=None,
        ranking=None,
    ):
        """
        Monta uma estrutura de plano a partir de resultados já calculados.

        Compatibilidade:
        - PlanningService atual chama executar(briefing=..., decision=...).
        - Fluxos futuros poderão chamar com plano_tatico/ranking.
        """

        if plano_tatico is not None:
            return self._montar_plano_tatico(
                plano_tatico=plano_tatico,
                decision=decision,
                briefing=briefing,
                ranking=ranking,
            )

        if decision is not None:
            return self._montar_plano_decision(
                decision
            )

        raise ValueError(
            "PlannerEngine precisa receber decision ou plano_tatico."
        )

    # =====================================================
    # COMPATIBILIDADE
    # =====================================================

    def gerar_plano(
        self,
        resultado,
    ):
        """
        Compatibilidade com chamadas legadas.

        Antes este método recebia briefing_id e chamava DecisionEngine.
        Agora recebe um DecisionResult já produzido por outro componente.
        """

        if isinstance(
            resultado,
            DecisionResult,
        ):
            return self._montar_plano_decision(
                resultado
            )

        raise TypeError(
            "PlannerEngine.gerar_plano agora espera um DecisionResult. "
            "Use PlanningService para orquestrar o fluxo completo."
        )

    # =====================================================
    # MONTAGEM A PARTIR DE DECISION RESULT
    # =====================================================

    def _montar_plano_decision(
        self,
        resultado: DecisionResult,
    ):
        ambientes = {}

        inventarios = []

        verba_total = getattr(
            resultado,
            "verba_total",
            0,
        )

        for decisao in getattr(
            resultado,
            "decisoes",
            [],
        ):
            percentual = getattr(
                decisao,
                "percentual",
                0,
            )

            verba = getattr(
                decisao,
                "verba",
                0,
            )

            inventario = InventarioPlano(
                inventario=decisao.inventario,
                plataforma=decisao.plataforma,
                ambiente=decisao.ambiente,
                score=decisao.score,
                percentual=percentual,
                verba=verba,
                papel=decisao.papel,
                justificativas=decisao.justificativas,
            )

            inventarios.append(
                inventario
            )

            if decisao.ambiente not in ambientes:
                ambientes[decisao.ambiente] = AmbientePlano(
                    ambiente=decisao.ambiente,
                    score=0,
                    percentual=0,
                    verba=0,
                    papel=decisao.papel,
                )

            ambiente = ambientes[decisao.ambiente]

            ambiente.verba += verba

            ambiente.percentual += percentual

            ambiente.score = max(
                ambiente.score,
                decisao.score,
            )

        return {
            "inventarios": inventarios,
            "ambientes": list(
                ambientes.values()
            ),
            "verba_total": verba_total,
            "score_global": getattr(
                resultado,
                "score_global",
                0,
            ),
            "observacoes": getattr(
                resultado,
                "observacoes",
                [],
            ),
            "alertas": getattr(
                resultado,
                "alertas",
                [],
            ),
            "erros": getattr(
                resultado,
                "erros",
                [],
            ),
        }

    # =====================================================
    # MONTAGEM A PARTIR DE PLANO TÁTICO
    # =====================================================

    def _montar_plano_tatico(
        self,
        plano_tatico,
        decision=None,
        briefing=None,
        ranking=None,
    ):
        ambientes = {}

        inventarios = []

        for item in getattr(
            plano_tatico,
            "itens",
            [],
        ):
            inventario = InventarioPlano(
                inventario=item.inventario,
                plataforma=item.plataforma,
                ambiente=item.ambiente,
                score=item.score,
                percentual=item.percentual,
                verba=item.verba,
                papel=item.papel,
                justificativas=[],
            )

            inventarios.append(
                inventario
            )

            if item.ambiente not in ambientes:
                ambientes[item.ambiente] = AmbientePlano(
                    ambiente=item.ambiente,
                    score=0,
                    percentual=0,
                    verba=0,
                    papel=item.papel,
                )

            ambiente = ambientes[item.ambiente]

            ambiente.verba += item.verba

            ambiente.percentual += item.percentual

            ambiente.score = max(
                ambiente.score,
                item.score,
            )

        return {
            "inventarios": inventarios,
            "ambientes": list(
                ambientes.values()
            ),
            "verba_total": getattr(
                plano_tatico,
                "verba_total",
                0,
            ),
            "score_global": self._score_global(
                inventarios
            ),
            "observacoes": [],
            "alertas": [],
            "erros": [],
        }

    # =====================================================
    # APOIO
    # =====================================================

    @staticmethod
    def _score_global(
        inventarios,
    ):
        if not inventarios:
            return 0

        return round(
            sum(
                item.score
                for item in inventarios
            )
            / len(inventarios),
            2,
        )
