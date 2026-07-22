import unittest
from datetime import date

from domain.models.briefing import Briefing
from domain.models.workflow_state import WorkflowState
from application.services.briefing_service import BriefingService


class TestBriefing(unittest.TestCase):

    def test_frequencia_deve_respeitar_a_faixa(self):

        briefing = BriefingService().criar(
            cliente="Cliente",
            campanha="Campanha",
            objetivo_id="objetivo-1",
            objetivo="Alcance",
            kpi="Alcance",
            orcamento=1000,
            tipo_flight="ONDA",
            frequencia_objetivo="MEDIA",
            frequencia_alvo=3,
        )

        self.assertIn("Frequência média deve estar entre 4 e 7.", briefing.validar())

    def test_alcance_deve_respeitar_a_faixa(self):

        briefing = self.criar_briefing(
            alcance_objetivo="ALTO",
            alcance_percentual=69,
        )

        self.assertIn(
            "Alcance alto deve estar entre 70% e 100%.",
            briefing.validar(),
        )

    def criar_briefing(self, **alteracoes):

        dados = {
            "cliente": "Cliente",
            "campanha": "Campanha",
            "objetivo_id": "objetivo-1",
            "objetivo": "Alcance",
            "kpi": "CPM",
            "orcamento": 1000,
        }
        dados.update(alteracoes)
        return Briefing(**dados)

    def test_briefing_valido(self):

        self.assertEqual(self.criar_briefing().validar(), [])

    def test_rejeita_periodo_invertido(self):

        briefing = self.criar_briefing(
            inicio=date(2026, 2, 2),
            fim=date(2026, 2, 1),
        )

        self.assertIn("Data final anterior à data inicial.", briefing.validar())

    def test_rejeita_orcamento_nao_positivo(self):

        briefing = self.criar_briefing(orcamento=0)

        self.assertIn("Orçamento deve ser maior que zero.", briefing.validar())


class TestWorkflowState(unittest.TestCase):

    def test_progresso_e_proxima_etapa(self):

        estado = WorkflowState(
            briefing=True,
            mcp_papeis=True,
            planejamento=True,
        )

        self.assertEqual(estado.concluidas, 3)
        self.assertEqual(estado.percentual, 42.9)
        self.assertEqual(estado.proxima_etapa, "Diagnóstico do Plano")


if __name__ == "__main__":
    unittest.main()
