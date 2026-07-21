import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from application.services.briefing_service import BriefingService
from application.services.diagnostico_service import DiagnosticoService
from application.services.exportacao_service import ExportacaoService
from application.services.forecast_service import ForecastService
from application.services.insights_service import InsightsService
from application.services.planejamento_service import PlanejamentoService
from application.services.universe_service import UniverseService


class TestWorkflowCompleto(unittest.TestCase):

    def test_briefing_ate_exportacao(self):

        briefing_service = BriefingService()
        briefing = briefing_service.criar(
            cliente="Cliente",
            campanha="Campanha",
            objetivo_id="objetivo-1",
            objetivo="Alcance",
            kpi="Alcance",
            orcamento=1000,
        )
        session_state = {}
        briefing_service.salvar(session_state, briefing)

        contexto = {
            "briefing": briefing,
            "objetivo": {"id": "objetivo-1", "nome": "Alcance"},
            "inventarios": [
                {
                    "id": "inventario-1",
                    "nome": "TV",
                    "plataforma_id": "plataforma-1",
                    "ambiente_id": "ambiente-1",
                    "formato_id": "formato-1",
                    "plataformas_v3": {"nome": "Aberta"},
                    "ambientes_v3": {"nome": "Vídeo"},
                }
            ],
            "audiencias": [{"audiencia_id": "audiencia-1", "peso": 100}],
            "inventarios_objetivos": [
                {
                    "inventario_id": "inventario-1",
                    "objetivo_id": "objetivo-1",
                    "score_base": 5,
                }
            ],
            "inventarios_kpis": [
                {
                    "inventario_id": "inventario-1",
                    "kpi_id": "kpi-1",
                    "score_base": 5,
                }
            ],
            "metricas": [
                {
                    "inventario_id": "inventario-1",
                    "inventario": "TV",
                    "cpm": 10,
                    "ctr": 2,
                    "taxa_conversao": 0.05,
                    "frequencia_media": 2,
                }
            ],
            "consumo": [
                {
                    "audiencia_id": "audiencia-1",
                    "ambiente_id": "ambiente-1",
                    "score": 5,
                }
            ],
            "kpis": [{"id": "kpi-1", "nome": "Alcance"}],
        }

        planejamento = PlanejamentoService()
        planejamento.context_service.carregar_por_objeto = Mock(
            return_value=contexto
        )
        plano = planejamento.gerar(briefing=briefing)
        diagnostico = DiagnosticoService().gerar(plano)
        forecast = ForecastService().gerar(plano, contexto["metricas"])
        insights = InsightsService().gerar(plano, forecast.itens)

        self.assertIs(session_state["briefing"], briefing)
        self.assertEqual(plano.verba_total, 1000)
        self.assertEqual(len(diagnostico.itens), 1)
        self.assertGreater(forecast.impressoes, 0)
        self.assertTrue(insights)

        exportacao = ExportacaoService()

        with tempfile.TemporaryDirectory() as pasta:
            excel = exportacao.excel(plano, Path(pasta) / "plano.xlsx")
            csv = exportacao.csv(plano, Path(pasta) / "plano.csv")

            self.assertGreater(excel.stat().st_size, 0)
            self.assertGreater(csv.stat().st_size, 0)


class TestPersistenciaSimulada(unittest.TestCase):

    def test_universo_valido_e_enviado_ao_repositorio(self):

        service = UniverseService()
        service.repository = Mock()
        dados = {
            "nome": "Brasil",
            "populacao": 1000,
            "publico_alvo": 500,
        }

        ok, erros = service.salvar(dados)

        self.assertTrue(ok)
        self.assertIsNone(erros)
        service.repository.salvar.assert_called_once_with(dados)

    def test_universo_invalido_nao_e_persistido(self):

        service = UniverseService()
        service.repository = Mock()

        ok, erros = service.salvar(
            {"nome": "Brasil", "populacao": 100, "publico_alvo": 200}
        )

        self.assertFalse(ok)
        self.assertIn(
            "O público-alvo não pode ser maior que a população.",
            erros,
        )
        service.repository.salvar.assert_not_called()


if __name__ == "__main__":
    unittest.main()
