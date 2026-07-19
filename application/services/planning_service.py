from engine.decision_engine import DecisionEngine
from engine.planner_engine import PlannerEngine
from engine.allocation_engine import AllocationEngine
from engine.score_engine import ScoreEngine
from engine.forecast_engine import ForecastEngine
from engine.scenario_engine import ScenarioEngine
from engine.insights_engine import InsightsEngine
from engine.recommendation_engine import RecommendationEngine
from engine.validation_engine import ValidationEngine
from engine.dashboard_engine import DashboardEngine
from engine.report_engine import ReportEngine
from engine.export_engine import ExportEngine


class PlanningService:
    """
    Orquestrador oficial do fluxo estratégico do SDM.

    Responsabilidade:
    - coordenar engines;
    - não implementar regra de mídia;
    - não acessar banco diretamente;
    - não calcular score;
    - não distribuir verba manualmente.
    """

    def __init__(self):
        self.decision_engine = DecisionEngine()
        self.score_engine = ScoreEngine()
        self.allocation_engine = AllocationEngine()
        self.planner_engine = PlannerEngine()
        self.forecast_engine = ForecastEngine()
        self.scenario_engine = ScenarioEngine()
        self.validation_engine = ValidationEngine()
        self.insights_engine = InsightsEngine()
        self.recommendation_engine = RecommendationEngine()
        self.dashboard_engine = DashboardEngine()
        self.report_engine = ReportEngine()
        self.export_engine = ExportEngine()

    # =====================================================
    # EXECUÇÃO COMPLETA
    # =====================================================

    def executar(self, briefing):
        """
        Executa o pipeline estratégico do SDM.

        Fluxo:
        Decision -> Ranking -> Allocation -> Planner -> Forecast ->
        Scenario -> Validation -> Insights -> Recommendation ->
        Dashboard -> Report.
        """

        resultado = {}

        # -------------------------------------------------
        # 1 - DECISÃO / CONTEXTO
        # -------------------------------------------------

        decision = self.decision_engine.decidir(
            briefing
        )

        resultado["decision"] = decision

        # -------------------------------------------------
        # 2 - RANKING
        # -------------------------------------------------
        #
        # Compatibilidade:
        # o DecisionEngine atual ainda devolve decisões já
        # pontuadas. Na próxima etapa, essa lógica será
        # movida para ScoreEngine.
        #

        ranking = self._ranking_from_decision(
            decision
        )

        resultado["ranking"] = ranking

        # -------------------------------------------------
        # 3 - ALOCAÇÃO
        # -------------------------------------------------

        verba_total = self._orcamento(
            briefing=briefing,
            decision=decision,
        )

        plano_tatico = self.allocation_engine.distribuir(
            ranking,
            verba_total,
        )

        resultado["plano_tatico"] = plano_tatico

        # -------------------------------------------------
        # 4 - PLANO
        # -------------------------------------------------

        plano = self.planner_engine.executar(
            briefing=briefing,
            decision=decision,
            plano_tatico=plano_tatico,
            ranking=ranking,
        )

        resultado["plano"] = plano

        # -------------------------------------------------
        # 5 - FORECAST
        # -------------------------------------------------

        forecast = self._forecast(
            plano
        )

        resultado["forecast"] = forecast

        # -------------------------------------------------
        # 6 - CENÁRIOS
        # -------------------------------------------------

        scenarios = self._scenarios(
            plano=plano,
            decision=decision,
            forecast=forecast,
        )

        resultado["scenarios"] = scenarios

        # -------------------------------------------------
        # 7 - VALIDAÇÃO
        # -------------------------------------------------

        validation = self._validation(
            briefing=briefing,
            decision=decision,
            plano=plano,
            forecast=forecast,
        )

        resultado["validation"] = validation

        # -------------------------------------------------
        # 8 - INSIGHTS
        # -------------------------------------------------

        insights = self._insights(
            briefing=briefing,
            plano=plano,
            forecast=forecast,
            scenarios=scenarios,
        )

        resultado["insights"] = insights

        # -------------------------------------------------
        # 9 - RECOMENDAÇÕES
        # -------------------------------------------------

        recommendations = self._recommendations(
            briefing=briefing,
            plano=plano,
            forecast=forecast,
            insights=insights,
        )

        resultado["recommendations"] = recommendations

        # -------------------------------------------------
        # 10 - DASHBOARD
        # -------------------------------------------------

        dashboard = self._dashboard(
            decision=decision,
            plano=plano,
            forecast=forecast,
            insights=insights,
            recommendations=recommendations,
            scenarios=scenarios,
        )

        resultado["dashboard"] = dashboard

        # -------------------------------------------------
        # 11 - RELATÓRIO
        # -------------------------------------------------

        report = self._report(
            dashboard
        )

        resultado["report"] = report

        return resultado

    # =====================================================
    # COMPATIBILIDADE
    # =====================================================

    def gerar(self, briefing):
        """
        Compatibilidade com fluxos que esperam apenas o plano.
        """

        return self.executar(
            briefing
        )["plano"]

    def exportar(
        self,
        dashboard,
        arquivo,
        formato=None,
    ):
        if hasattr(
            self.export_engine,
            "exportar",
        ):
            return self.export_engine.exportar(
                dashboard,
                arquivo,
                formato,
            )

        if formato == "json" and hasattr(
            self.export_engine,
            "json",
        ):
            return self.export_engine.json(
                dashboard,
                arquivo,
            )

        raise AttributeError(
            "ExportEngine não possui método exportar compatível."
        )

    # =====================================================
    # ADAPTADORES INTERNOS
    # =====================================================

    def _ranking_from_decision(
        self,
        decision,
    ):
        ranking = []

        for item in getattr(
            decision,
            "decisoes",
            [],
        ):
            ranking.append(
                {
                    "inventario": item.inventario,
                    "plataforma": item.plataforma,
                    "ambiente": item.ambiente,
                    "papel": item.papel,
                    "score": item.score,
                    "justificativas": item.justificativas,
                }
            )

        ranking.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return ranking

    def _orcamento(
        self,
        briefing,
        decision,
    ):
        if isinstance(
            briefing,
            dict,
        ):
            return float(
                briefing.get(
                    "orcamento",
                    getattr(
                        decision,
                        "verba_total",
                        0,
                    ),
                )
                or 0
            )

        return float(
            getattr(
                briefing,
                "orcamento",
                getattr(
                    decision,
                    "verba_total",
                    0,
                ),
            )
            or 0
        )

    def _forecast(
        self,
        plano,
    ):
        if hasattr(
            self.forecast_engine,
            "executar",
        ):
            return self.forecast_engine.executar(
                plano
            )

        return None

    def _scenarios(
        self,
        plano,
        decision,
        forecast,
    ):
        if hasattr(
            self.scenario_engine,
            "executar",
        ):
            return self.scenario_engine.executar(
                plano,
                decision,
                forecast,
            )

        return []

    def _validation(
        self,
        briefing,
        decision,
        plano,
        forecast,
    ):
        if hasattr(
            self.validation_engine,
            "validar",
        ):
            return self.validation_engine.validar(
                briefing=briefing,
                decision=decision,
                plano=plano,
                forecast=forecast,
            )

        return {
            "valido": True,
            "erros": [],
            "alertas": [],
        }

    def _insights(
        self,
        briefing,
        plano,
        forecast,
        scenarios,
    ):
        if hasattr(
            self.insights_engine,
            "executar",
        ):
            return self.insights_engine.executar(
                briefing,
                plano,
                forecast,
                scenarios,
            )

        return []

    def _recommendations(
        self,
        briefing,
        plano,
        forecast,
        insights,
    ):
        if hasattr(
            self.recommendation_engine,
            "executar",
        ):
            return self.recommendation_engine.executar(
                briefing,
                plano,
                forecast,
                insights,
            )

        return []

    def _dashboard(
        self,
        decision,
        plano,
        forecast,
        insights,
        recommendations,
        scenarios,
    ):
        if hasattr(
            self.dashboard_engine,
            "gerar",
        ):
            return self.dashboard_engine.gerar(
                decision=decision,
                plano=plano,
                forecast=forecast,
                insights=insights,
                recommendations=recommendations,
                scenarios=scenarios,
            )

        return {
            "decision": decision,
            "plano": plano,
            "forecast": forecast,
            "insights": insights,
            "recommendations": recommendations,
            "scenarios": scenarios,
        }

    def _report(
        self,
        dashboard,
    ):
        if hasattr(
            self.report_engine,
            "gerar",
        ):
            return self.report_engine.gerar(
                dashboard
            )

        return dashboard
