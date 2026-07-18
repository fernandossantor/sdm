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
    Serviço responsável por orquestrar todo o fluxo do SDM.

    Não contém regras de mídia.
    Apenas coordena os engines.
    """

    def __init__(self):

        self.decision_engine = DecisionEngine()
        self.planner_engine = PlannerEngine()
        self.allocation_engine = AllocationEngine()
        self.score_engine = ScoreEngine()
        self.forecast_engine = ForecastEngine()
        self.scenario_engine = ScenarioEngine()
        self.insights_engine = InsightsEngine()
        self.recommendation_engine = RecommendationEngine()
        self.validation_engine = ValidationEngine()
        self.dashboard_engine = DashboardEngine()
        self.report_engine = ReportEngine()
        self.export_engine = ExportEngine()

    # =====================================================
    # EXECUÇÃO COMPLETA
    # =====================================================

    def executar(self, briefing):

        resultado = {}

        # -------------------------------------------------
        # 1 - DECISÃO
        # -------------------------------------------------

        decision = self.decision_engine.executar(
            briefing
        )

        resultado["decision"] = decision

        # -------------------------------------------------
        # 2 - PLANO
        # -------------------------------------------------

        plano = self.planner_engine.executar(
            briefing=briefing,
            decision=decision
        )

        resultado["plano"] = plano

        # -------------------------------------------------
        # 3 - ALOCAÇÃO
        # -------------------------------------------------

        plano = self.allocation_engine.executar(
            plano
        )

        resultado["plano"] = plano

        # -------------------------------------------------
        # 4 - SCORE
        # -------------------------------------------------

        decision = self.score_engine.executar(
            decision
        )

        resultado["decision"] = decision

        # -------------------------------------------------
        # 5 - FORECAST
        # -------------------------------------------------

        forecast = self.forecast_engine.executar(
            plano
        )

        resultado["forecast"] = forecast

        # -------------------------------------------------
        # 6 - CENÁRIOS
        # -------------------------------------------------

        scenarios = self.scenario_engine.executar(
            plano,
            decision,
            forecast
        )

        resultado["scenarios"] = scenarios

        # -------------------------------------------------
        # 7 - INSIGHTS
        # -------------------------------------------------

        insights = self.insights_engine.executar(
            briefing,
            plano,
            forecast,
            scenarios
        )

        resultado["insights"] = insights

        # -------------------------------------------------
        # 8 - RECOMENDAÇÕES
        # -------------------------------------------------

        recommendations = self.recommendation_engine.executar(
            briefing,
            plano,
            forecast,
            insights
        )

        resultado["recommendations"] = recommendations

        # -------------------------------------------------
        # 9 - VALIDAÇÃO
        # -------------------------------------------------

        validation = self.validation_engine.validar(
            briefing=briefing,
            decision=decision,
            plano=plano,
            forecast=forecast
        )

        resultado["validation"] = validation

        # -------------------------------------------------
        # 10 - DASHBOARD
        # -------------------------------------------------

        dashboard = self.dashboard_engine.gerar(
            decision=decision,
            plano=plano,
            forecast=forecast,
            insights=insights,
            recommendations=recommendations,
            scenarios=scenarios
        )

        resultado["dashboard"] = dashboard

        # -------------------------------------------------
        # 11 - RELATÓRIO
        # -------------------------------------------------

        report = self.report_engine.gerar(
            dashboard
        )

        resultado["report"] = report

        return resultado

    # =====================================================
    # EXPORTAÇÃO
    # =====================================================

    def exportar(

        self,

        dashboard,

        arquivo,

        formato=None

    ):

        return self.export_engine.exportar(

            dashboard,

            arquivo,

            formato

        )