import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from application.services.scenario_service import ScenarioService
from application.services.workflow_service import WorkflowService
from application.services.planejamento_service import PlanejamentoService
from datetime import date
from domain.models.plano_estrategico import PlanoEstrategico, PlanoItem
from infrastructure.database import admin_client
from infrastructure.repositories.decision_repository import DecisionRepository


class TestPlanejamentoService(unittest.TestCase):

    def test_calcula_meta_e_projecao_de_alcance(self):

        plano = PlanoEstrategico(
            cliente="Cliente",
            campanha="Campanha",
            objetivo="Alcance",
            orcamento=1000,
            frequencia_alvo=5,
            alcance_objetivo="ALTO",
            alcance_percentual=80,
            publico_referencia=10000,
            alcance_meta=8000,
        )
        plano.adicionar_item(
            PlanoItem(
                inventario="Vídeo",
                plataforma="Digital",
                ambiente="Vídeo",
                papel="PRINCIPAL",
                score=90,
                verba=1000,
                percentual=100,
                preco_unitario=10,
                unidade_compra="CPM",
            )
        )

        PlanejamentoService._calcular_entrega(plano)

        self.assertEqual(plano.alcance_meta, 8000)
        self.assertEqual(plano.alcance_projetado, 10000)

    def test_publico_referencia_considera_pesos(self):

        total = PlanejamentoService._publico_referencia(
            [
                {"populacao_estimada": 10000, "peso": 100},
                {"populacao_estimada": 5000, "peso": 50},
            ]
        )

        self.assertEqual(total, 12500)

    def test_flight_concentrado_aloca_apenas_o_inicio(self):

        cronograma = PlanejamentoService._cronograma(
            date(2026, 7, 1),
            date(2026, 7, 28),
            "CONCENTRADO",
        )

        self.assertEqual(sum(item["percentual"] for item in cronograma), 100)
        self.assertEqual(cronograma[-1]["percentual"], 0)


class TestContextoCampanha(unittest.TestCase):

    def test_referencia_mcp_e_especifica_por_campanha(self):

        briefing = SimpleNamespace(campanha="Lançamento")

        self.assertEqual(
            DecisionRepository.campanha_ref(briefing),
            "sessao:Lançamento",
        )

    def test_novo_briefing_invalida_etapas_posteriores(self):

        session_state = {
            "mcp_papeis": "antigo",
            "plano": "antigo",
            "diagnostico": "antigo",
        }
        briefing = SimpleNamespace(campanha="Nova campanha")

        from application.services.briefing_service import BriefingService

        BriefingService().salvar(session_state, briefing)

        self.assertIs(session_state["briefing"], briefing)
        self.assertNotIn("mcp_papeis", session_state)
        self.assertNotIn("plano", session_state)


class TestAdminClient(unittest.TestCase):

    def tearDown(self):

        admin_client.get_admin_client.cache_clear()

    def test_import_offline_nao_cria_cliente(self):

        admin_client.get_admin_client.cache_clear()

        with (
            patch.object(admin_client, "load_dotenv"),
            patch.dict(
                admin_client.os.environ,
                {
                    "SUPABASE_URL": "",
                    "SUPABASE_SERVICE_KEY": "",
                },
            ),
            patch.object(admin_client, "create_client") as criar_cliente,
        ):
            with self.assertRaisesRegex(RuntimeError, "devem estar configuradas"):
                admin_client.admin.table("inventarios_v3")

        criar_cliente.assert_not_called()


class TestScenarioService(unittest.TestCase):

    def criar_service(self):

        service = ScenarioService()
        contexto = {
            "briefing": {
                "anunciante": "Cliente",
                "nome": "Campanha",
                "orcamento": 1000,
            },
            "objetivo": {"nome": "Alcance"},
        }
        ranking = [
            {
                "inventario": "TV",
                "plataforma": "Aberta",
                "ambiente": "Vídeo",
                "papel": "PRINCIPAL",
                "score": 90,
                "objetivo": 90,
                "kpi": 90,
                "audiencia": 90,
                "metricas": 105,
            }
        ]
        service.planejamento = SimpleNamespace(
            context_service=SimpleNamespace(
                carregar=Mock(return_value=contexto),
            ),
            inventory_engine=SimpleNamespace(
                calcular=Mock(return_value=ranking),
            ),
            recomendacao_service=SimpleNamespace(
                inventario=Mock(return_value=["Recomendado."]),
            ),
        )
        return service

    def test_gera_cenario_usando_context_service(self):

        service = self.criar_service()

        plano = service.gerar("Campanha", "EQUILIBRADO")

        service.planejamento.context_service.carregar.assert_called_once_with(
            "Campanha"
        )
        self.assertEqual(plano.cliente, "Cliente")
        self.assertEqual(len(plano.itens), 1)
        self.assertEqual(plano.verba_total, 1000)

    def test_resumo_aceita_plano_sem_inventarios(self):

        service = self.criar_service()
        service.gerar_todos = Mock(
            return_value={
                "EQUILIBRADO": PlanoEstrategico(
                    cliente="Cliente",
                    campanha="Campanha",
                    objetivo="Alcance",
                    orcamento=1000,
                )
            }
        )

        resumo = service.resumo("Campanha")

        self.assertEqual(resumo[0]["score_medio"], 0)
        self.assertEqual(resumo[0]["inventarios"], 0)

    def test_gera_cenarios_a_partir_de_planejamento_salvo(self):

        plano = PlanoEstrategico(
            cliente="Cliente",
            campanha="Campanha",
            objetivo="Alcance",
            orcamento=1000,
        )
        plano.adicionar_item(
            PlanoItem(
                inventario="Vídeo",
                plataforma="Digital",
                ambiente="Portal",
                papel="PRINCIPAL",
                score=90,
                verba=1000,
                percentual=100,
                objetivo_score=95,
                kpi_score=90,
                audiencia_score=85,
                metricas_score=105,
            )
        )

        cenarios = ScenarioService().gerar_todos_de_plano(plano)

        self.assertTrue(cenarios)
        self.assertTrue(all(cenario.itens for cenario in cenarios.values()))


class TestWorkflowService(unittest.TestCase):

    def test_registra_etapas_com_chaves_canonicas(self):

        session_state = {}
        service = WorkflowService()

        service.registrar_briefing(session_state, "Campanha")
        service.concluir(session_state, "mcp_papeis", "sessao:Campanha")
        service.concluir(session_state, "planejamento", "plano")
        service.concluir(session_state, "diagnostico", "diagnostico")

        estado = service.estado(session_state)

        self.assertTrue(estado.briefing)
        self.assertTrue(estado.mcp_papeis)
        self.assertTrue(estado.planejamento)
        self.assertTrue(estado.diagnostico)
        self.assertEqual(estado.proxima_etapa, "Forecast")

    def test_valida_pre_requisitos_de_acesso(self):

        session_state = {"briefing_ref": "Campanha"}
        service = WorkflowService()

        self.assertTrue(service.pode_acessar(session_state, "mcp_papeis"))
        self.assertFalse(service.pode_acessar(session_state, "planejamento"))
        self.assertFalse(service.pode_acessar(session_state, "forecast"))

        service.concluir(session_state, "mcp_papeis", "sessao:Campanha")
        service.concluir(session_state, "planejamento", "plano")
        service.concluir(session_state, "diagnostico", "diagnostico")

        self.assertTrue(service.pode_acessar(session_state, "forecast"))

    def test_rejeita_etapa_desconhecida(self):

        with self.assertRaises(ValueError):
            WorkflowService().concluir({}, "desconhecida")


if __name__ == "__main__":
    unittest.main()
