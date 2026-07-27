import unittest

from application.services.attribution_service import AttributionService
from engine.attribution_engine import AttributionEngine


class TestAttributionEngine(unittest.TestCase):
    def test_credito_linear_fecha_em_cem_por_cento(self):
        resultado = AttributionEngine().calcular([{
            "id": "C-1",
            "instante": "2026-07-20T12:00:00",
            "receita": 300,
            "toques": [
                {"canal": "Vídeo", "instante": "2026-07-10T12:00:00"},
                {"canal": "Busca", "instante": "2026-07-19T12:00:00"},
                {"canal": "Social", "instante": "2026-07-20T10:00:00"},
            ],
        }], "LINEAR", 30)

        self.assertAlmostEqual(
            sum(item["credito"] for item in resultado["creditos"]),
            1.0,
        )
        self.assertEqual(
            {item["tipo_conversao"] for item in resultado["creditos"]},
            {"ASSISTIDA"},
        )
        self.assertEqual(
            sum(item["receita_atribuida"] for item in resultado["creditos"]),
            300,
        )
        self.assertTrue(resultado["todos_creditos_reconciliados"])
        self.assertEqual(resultado["reconciliacao"][0]["credito_total"], 1)

    def test_janela_exclui_toque_antigo(self):
        resultado = AttributionEngine().calcular([{
            "id": "C-1",
            "instante": "2026-07-20T12:00:00",
            "toques": [
                {"canal": "Vídeo", "instante": "2026-05-01T12:00:00"},
                {"canal": "Busca", "instante": "2026-07-19T12:00:00"},
            ],
        }], "ULTIMO_TOQUE", 30)

        self.assertEqual(len(resultado["creditos"]), 1)
        self.assertEqual(resultado["creditos"][0]["canal"], "Busca")
        self.assertEqual(resultado["creditos"][0]["tipo_conversao"], "DIRETA")

    def test_servico_consolida_credito_por_canal(self):
        eventos = [
            {
                "conversao_id": "C-1",
                "instante_conversao": "2026-07-20T12:00:00",
                "receita": 100,
                "canal": "Vídeo",
                "instante_toque": "2026-07-10T12:00:00",
            },
            {
                "conversao_id": "C-1",
                "instante_conversao": "2026-07-20T12:00:00",
                "receita": 100,
                "canal": "Busca",
                "instante_toque": "2026-07-19T12:00:00",
            },
        ]

        resultado = AttributionService().calcular(eventos, "POSICIONAL", 30)

        self.assertEqual(resultado["conversoes_elegiveis"], 1)
        self.assertEqual(resultado["conversoes_assistidas"], 1)
        self.assertEqual(resultado["conversoes_diretas"], 0)
        self.assertEqual(
            sum(item["credito_em_conversoes"] for item in resultado["por_canal"]),
            1,
        )
        self.assertIn("não mede incrementalidade", resultado["limitacoes"][-1])


if __name__ == "__main__":
    unittest.main()
