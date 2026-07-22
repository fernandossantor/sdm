import unittest

from engine.allocation_engine import AllocationEngine
from engine.budget_optimizer import BudgetOptimizer
from engine.classificacao_papeis_engine import ClassificacaoPapeisEngine
from engine.forecast_engine import ForecastEngine
from engine.insights_engine import InsightsEngine
from engine.inventory_engine import InventoryEngine
from engine.recommendation_engine import RecommendationEngine
from engine.scenario_engine import ScenarioEngine
from engine.score_engine import ScoreEngine
from domain.models.plano_tatico import PlanoTatico, PlanoTaticoItem


class TestAllocationEngine(unittest.TestCase):

    def test_distribui_toda_a_verba(self):

        ranking = [
            {
                "inventario": "TV",
                "plataforma": "Aberta",
                "ambiente": "Vídeo",
                "papel": "PRINCIPAL",
                "score": 90,
            },
            {
                "inventario": "Rádio",
                "plataforma": "FM",
                "ambiente": "Áudio",
                "papel": "COMPLEMENTAR",
                "score": 70,
            },
        ]

        plano = AllocationEngine().distribuir(ranking, 1000)

        self.assertEqual(plano.verba_distribuida, 1000)
        self.assertAlmostEqual(plano.percentual_total, 100, places=1)

    def test_ignora_scores_nao_positivos(self):

        ranking = [
            {
                "inventario": "Inválido",
                "plataforma": "",
                "ambiente": "",
                "papel": "APOIO",
                "score": 0,
            }
        ]

        plano = AllocationEngine().distribuir(ranking, 1000)

        self.assertEqual(plano.itens, [])


class TestClassificacaoPapeisEngine(unittest.TestCase):

    def test_calcula_score_ponderado(self):

        engine = ClassificacaoPapeisEngine()

        self.assertEqual(engine.calcular_score(100, 80, 60), 81)

    def test_classifica_por_ordem_de_score(self):

        resultado = ClassificacaoPapeisEngine().classificar(
            {"TV": 80, "Digital": 95, "Rádio": 60}
        )

        self.assertEqual(resultado[0]["meio"], "Digital")
        self.assertEqual(resultado[0]["papel"], "Principal")
        self.assertEqual(resultado[1]["papel"], "Complementar")
        self.assertEqual(resultado[2]["papel"], "Apoio")


class TestScenarioEngine(unittest.TestCase):

    def test_aplicar_nao_altera_ranking_original(self):

        ranking = [{"inventario": "TV", "papel": "PRINCIPAL", "score": 80}]

        resultado = ScenarioEngine().aplicar(ranking, "CONSERVADOR")

        self.assertEqual(ranking[0]["score"], 80)
        self.assertEqual(resultado[0]["score"], 104)

    def test_resumo_vazio(self):

        resumo = ScenarioEngine().resumo([], "EQUILIBRADO")

        self.assertEqual(resumo["inventarios"], 0)
        self.assertEqual(resumo["score_medio"], 0)


class TestForecastEngine(unittest.TestCase):

    def criar_plano(self):

        return PlanoTatico(
            verba_total=1000,
            itens=[
                PlanoTaticoItem(
                    inventario="TV",
                    plataforma="Aberta",
                    ambiente="Vídeo",
                    papel="PRINCIPAL",
                    percentual=100,
                    verba=1000,
                    score=90,
                )
            ],
        )

    def test_calcula_indicadores_de_midia(self):

        resultado = ForecastEngine().calcular(
            self.criar_plano(),
            [
                {
                    "inventario_id": "tv-1",
                    "inventario": "TV",
                    "cpm": 10,
                    "ctr": 2,
                    "taxa_conversao": 0.05,
                    "frequencia_media": 2,
                }
            ],
        )

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].impressoes, 100000)
        self.assertEqual(resultado[0].alcance, 50000)
        self.assertEqual(resultado[0].cliques, 2000)
        self.assertEqual(resultado[0].conversoes, 100)

    def test_frequencia_do_plano_controla_o_alcance(self):

        plano = self.criar_plano()
        plano.frequencia_alvo = 5
        resultado = ForecastEngine().calcular(
            plano,
            [{
                "inventario_id": "tv-1",
                "inventario": "TV",
                "cpm": 10,
                "ctr": 2,
                "frequencia_media": 2,
            }],
        )

        self.assertEqual(resultado[0].alcance, 20000)

    def test_ignora_inventario_sem_metrica(self):

        self.assertEqual(ForecastEngine().calcular(self.criar_plano(), []), [])


class TestInsightsEngine(unittest.TestCase):

    def test_plano_vazio_produz_aviso(self):

        plano = PlanoTatico(verba_total=0)

        self.assertEqual(
            InsightsEngine().gerar(plano),
            ["Nenhum inventário selecionado."],
        )

    def test_identifica_concentracao_e_baixa_diversidade(self):

        plano = PlanoTatico(
            verba_total=1000,
            itens=[
                PlanoTaticoItem(
                    inventario="TV",
                    plataforma="Aberta",
                    ambiente="Vídeo",
                    papel="PRINCIPAL",
                    percentual=100,
                    verba=1000,
                    score=90,
                )
            ],
        )

        insights = InsightsEngine().gerar(plano)

        self.assertTrue(any("Alta concentração" in item for item in insights))
        self.assertIn("O plano utiliza apenas um ambiente de mídia.", insights)
        self.assertIn("Existe dependência de um único canal principal.", insights)


class TestBudgetOptimizer(unittest.TestCase):

    def test_reserva_percentual_para_testes(self):

        resultado = BudgetOptimizer().otimizar(
            [
                {
                    "inventario": "TV",
                    "ambiente": "Vídeo",
                    "plataforma": "Aberta",
                    "score": 100,
                }
            ],
            verba_total=1000,
            percentual_teste=0.1,
        )

        self.assertEqual(resultado["verba_distribuida"], 900)
        self.assertEqual(resultado["reserva_testes"], 100)
        self.assertEqual(resultado["itens"][0]["percentual"], 100)

    def test_retorna_vazio_quando_nao_ha_score(self):

        resultado = BudgetOptimizer().otimizar(
            [
                {
                    "inventario": "TV",
                    "ambiente": "Vídeo",
                    "plataforma": "Aberta",
                    "score": 0,
                }
            ],
            verba_total=1000,
        )

        self.assertEqual(resultado, [])


class TestScoreEngine(unittest.TestCase):

    def test_interesses_ponderam_afinidade_com_o_ambiente(self):

        score = ScoreEngine.interesses(
            {"ambiente_id": "social"},
            [{"interesses": [{"id": "games", "peso": 100}]}],
            {("games", "social"): 90},
        )

        self.assertEqual(score, 90)

    def test_calcula_componentes_e_papel(self):

        self.assertEqual(
            ScoreEngine.objetivo({"score_base": 4, "peso_manual": 1}),
            80,
        )
        self.assertEqual(
            ScoreEngine.kpis(
                "inventario-1",
                {("inventario-1", "kpi-1"): {"score_base": 5}},
                [("kpi-1", 100)],
            ),
            100,
        )
        self.assertEqual(ScoreEngine.papel(85), "PRINCIPAL")
        self.assertEqual(ScoreEngine.papel(49), "OPCIONAL")

    def test_score_final_aplica_bonus_e_penalidade(self):

        score = ScoreEngine.score_final(100, 100, 100, 100, 10, 20)

        self.assertEqual(score, 90)


class TestInventoryEngine(unittest.TestCase):

    @staticmethod
    def contexto_base():

        return {
            "briefing": {"kpi": "Alcance"},
            "objetivo": {"id": "objetivo-1"},
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
            "metricas": [],
            "consumo": [],
            "kpis": [{"id": "kpi-1", "nome": "Alcance"}],
        }

    def test_aplica_papel_mcp_e_preco_vigente(self):

        contexto = self.contexto_base()
        contexto["papeis_inventarios"] = [
            {
                "inventario_id": "inventario-1",
                "score": 95,
                "papel": "COMPLEMENTAR",
            }
        ]
        contexto["precos"] = [
            {
                "inventario_id": "inventario-1",
                "valor_bruto": 20,
                "desconto_percentual": 10,
                "unidade": "CPM",
                "inicio_vigencia": "2020-01-01",
                "fim_vigencia": "2090-01-01",
            },
            {
                "inventario_id": "inventario-1",
                "valor_bruto": 999,
                "desconto_percentual": 0,
                "unidade": "CPM",
                "inicio_vigencia": "2099-01-01",
            },
        ]

        item = InventoryEngine().calcular(contexto)[0]

        self.assertEqual(item["papel"], "COMPLEMENTAR")
        self.assertEqual(item["score_mcp"], 95)
        self.assertEqual(item["preco_unitario"], 18)

    def test_calcula_e_ordena_inventarios(self):

        contexto = {
            "briefing": {"kpi": "Alcance"},
            "objetivo": {"id": "objetivo-1"},
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
                    "ctr": 2,
                    "viewability": 80,
                    "frequencia_media": 4,
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

        resultado = InventoryEngine().calcular(contexto)

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["inventario"], "TV")
        self.assertEqual(resultado[0]["papel"], "PRINCIPAL")
        self.assertEqual(resultado[0]["audiencia"], 100)


class TestRecommendationEngine(unittest.TestCase):

    def test_ranking_vazio_tem_retorno_explicito(self):

        engine = RecommendationEngine()

        self.assertEqual(
            engine.resumo([]),
            ["Nenhum inventário disponível para análise."],
        )
        self.assertEqual(
            engine.riscos([]),
            ["Baixa diversidade de inventários."],
        )

    def test_recomenda_inventario_principal(self):

        recomendacoes = RecommendationEngine().recomendar(
            {
                "objetivo": 95,
                "kpi": 95,
                "audiencia": 95,
                "metricas": 105,
                "papel": "PRINCIPAL",
            }
        )

        self.assertIn("Elevada aderência ao objetivo da campanha.", recomendacoes)
        self.assertIn("Recomendado como canal principal do plano.", recomendacoes)


if __name__ == "__main__":
    unittest.main()
