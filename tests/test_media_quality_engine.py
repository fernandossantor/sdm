import unittest

from application.services.media_quality_service import MediaQualityService
from engine.media_quality_engine import MediaQualityEngine


class TestMediaQualityEngine(unittest.TestCase):
    def test_preserva_dimensoes_sem_indice_composto(self):
        resultado = MediaQualityEngine().avaliar_qualidade([{
            "inventario": "Display",
            "viewability_percentual": 72,
            "trafego_invalido_percentual": 3,
            "fraude_percentual": 1,
            "brand_safety": "ADEQUADO",
            "brand_suitability": "ADEQUADO",
            "fonte": "Verificador independente",
            "inicio": "2026-07-01",
            "fim": "2026-07-31",
        }])

        self.assertEqual(resultado[0]["situacao"], "DOCUMENTADO")
        self.assertEqual(resultado[0]["viewability_percentual"], 72)
        self.assertNotIn("score", resultado[0])

    def test_qualidade_sem_fonte_fica_incompleta(self):
        resultado = MediaQualityEngine().avaliar_qualidade([{
            "inventario": "Vídeo",
            "viewability_percentual": 80,
            "inicio": "2026-07-01",
            "fim": "2026-07-31",
        }])

        self.assertEqual(resultado[0]["situacao"], "INCOMPLETO")
        self.assertIn("fonte", resultado[0]["lacunas"])

    def test_localizacao_distingue_visita_e_exige_proveniencia(self):
        resultado = MediaQualityService().avaliar([], [{
            "inventario": "OOH",
            "fonte_sinal": "GPS consentido",
            "precisao_metros": 15,
            "raio_metros": 100,
            "inicio": "2026-07-01",
            "fim": "2026-07-31",
            "finalidade": "Mensuração de visita",
            "base_legal": "Consentimento",
            "metodo_associacao": "Presença no raio por 5 minutos",
            "confianca_percentual": 90,
            "natureza_visita": "OBSERVADA",
        }])

        self.assertEqual(resultado["resumo"]["localizacao_documentada"], 1)
        self.assertEqual(
            resultado["localizacao"][0]["natureza_visita"],
            "OBSERVADA",
        )
        self.assertIn("não são equivalentes", resultado["limitacoes"][1])

    def test_rejeita_percentual_fora_do_dominio(self):
        with self.assertRaisesRegex(ValueError, "entre 0% e 100%"):
            MediaQualityEngine().avaliar_qualidade([{
                "inventario": "Display",
                "fraude_percentual": 120,
            }])

    def test_localizacao_nao_aplicavel_nao_cria_lacuna(self):
        resultado = MediaQualityEngine().avaliar_localizacao([{
            "inventario": "TV",
        }])

        self.assertEqual(resultado, [])


if __name__ == "__main__":
    unittest.main()
