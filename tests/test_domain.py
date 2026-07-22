import unittest
from datetime import date

from domain.models.briefing import Briefing
from domain.models.workflow_state import WorkflowState
from application.services.briefing_service import BriefingService
from domain.media_metrics import resolver_grp


class TestBriefing(unittest.TestCase):

    def test_calcula_grp_com_alcance_e_frequencia(self):
        self.assertEqual(resolver_grp(60, 5, None), (60.0, 5.0, 300.0))

    def test_calcula_frequencia_com_grp_e_alcance(self):
        self.assertEqual(resolver_grp(60, None, 300), (60.0, 5.0, 300.0))

    def test_calcula_alcance_com_grp_e_frequencia(self):
        self.assertEqual(resolver_grp(None, 5, 300), (60.0, 5.0, 300.0))

    def test_servico_completa_o_terceiro_indicador(self):
        briefing = BriefingService().criar(
            cliente="Cliente", campanha="Campanha", objetivo_id="objetivo-1",
            objetivo="Alcance", kpi="Alcance", orcamento=1000,
            alcance_percentual=50, frequencia_alvo=None, grp=200,
        )

        self.assertEqual(briefing.frequencia_alvo, 4)
        self.assertEqual(briefing.frequencia_objetivo, "MEDIA")

    def test_frequencia_define_a_faixa_correspondente(self):

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

        self.assertEqual(briefing.frequencia_objetivo, "BAIXA")
        self.assertEqual(briefing.validar(), [])

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
