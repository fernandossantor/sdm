import unittest

from application.services.version_comparison_service import (
    VersionComparisonService,
)
from domain.models.plano_estrategico import PlanoEstrategico, PlanoItem


class TestVersionComparisonService(unittest.TestCase):
    @staticmethod
    def _plano(verba, quantidade, alcance):
        plano = PlanoEstrategico(
            cliente="Cliente",
            campanha="Campanha",
            objetivo="Alcance",
            orcamento=verba,
        )
        plano.adicionar_item(PlanoItem(
            inventario="Vídeo",
            inventario_id="video-1",
            plataforma="Digital",
            ambiente="Streaming",
            papel="PRINCIPAL",
            score=90,
            verba=verba,
            percentual=100,
            quantidade_estimada=quantidade,
        ))
        plano.resultados_consolidados = {
            "investimento": verba,
            "alcance_liquido_percentual": alcance,
        }
        return plano

    def test_compara_metricas_e_itens_sem_declarar_causalidade(self):
        resultado = VersionComparisonService().comparar(
            self._plano(1000, 10, 60),
            self._plano(1200, 12, 65),
            {"versao_anterior": 1, "versao_atual": 2},
        )

        alcance = next(
            item
            for item in resultado["metricas"]
            if item["metrica"] == "Alcance líquido (%)"
        )
        self.assertEqual(alcance["variacao_absoluta"], 5)
        self.assertEqual(resultado["itens"][0]["variacao_verba"], 200)
        self.assertIn("descritiva", resultado["natureza"])

    def test_identifica_inventario_adicionado(self):
        anterior = self._plano(1000, 10, 60)
        atual = self._plano(1000, 10, 60)
        atual.adicionar_item(PlanoItem(
            inventario="Busca",
            inventario_id="busca-1",
            plataforma="Digital",
            ambiente="Busca",
            papel="APOIO",
            score=70,
            verba=100,
            percentual=10,
        ))

        resultado = VersionComparisonService().comparar(anterior, atual)

        busca = next(
            item for item in resultado["itens"]
            if item["inventario"] == "Busca"
        )
        self.assertEqual(busca["situacao"], "ADICIONADO")


if __name__ == "__main__":
    unittest.main()
