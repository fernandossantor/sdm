import unittest
from datetime import date

from domain.models.briefing import Briefing
from domain.models.workflow_state import WorkflowState


class TestBriefing(unittest.TestCase):

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

        estado = WorkflowState(briefing=True, planejamento=True)

        self.assertEqual(estado.concluidas, 2)
        self.assertEqual(estado.percentual, 33.3)
        self.assertEqual(estado.proxima_etapa, "Diagnóstico")


if __name__ == "__main__":
    unittest.main()
