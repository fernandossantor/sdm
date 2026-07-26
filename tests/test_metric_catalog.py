import unittest
from datetime import date

from domain.metric_catalog import (
    ContextoMetrica,
    NaturezaMetrica,
    NivelConfianca,
    OrigemMetrica,
    SituacaoComparabilidade,
    ValorMetrica,
    comparar_contextos,
)


class TestValorMetrica(unittest.TestCase):
    def contexto(self, **alteracoes):
        dados = {
            "universo": "BR-18+",
            "publico_alvo": "Adultos",
            "praca": "Brasil",
            "inicio_referencia": date(2026, 7, 1),
            "fim_referencia": date(2026, 7, 31),
            "metrica_nativa": "IMPRESSOES",
            "metodologia": "Ad server",
            "granularidade": "MENSAL",
        }
        dados.update(alteracoes)
        return ContextoMetrica(**dados)

    def test_metrica_medida_exige_fonte(self):
        metrica = ValorMetrica(
            valor=1000,
            unidade="IMPRESSAO",
            natureza=NaturezaMetrica.FATO,
            origem=OrigemMetrica.MEDIDO,
            contexto=self.contexto(),
            confianca=NivelConfianca.ALTA,
        )

        self.assertIn("Uma métrica medida deve informar a fonte.", metrica.validar())

    def test_resultado_exige_versao_e_entradas(self):
        metrica = ValorMetrica(
            valor=10,
            unidade="PERCENTUAL",
            natureza=NaturezaMetrica.RESULTADO,
            origem=OrigemMetrica.CALCULADO,
            contexto=self.contexto(),
        )

        self.assertEqual(
            metrica.validar(),
            (
                "Um resultado deve informar a versão do método.",
                "Um resultado deve apontar suas entradas.",
            ),
        )

    def test_metrica_auditavel_e_valida(self):
        metrica = ValorMetrica(
            valor=10,
            unidade="PERCENTUAL",
            natureza=NaturezaMetrica.RESULTADO,
            origem=OrigemMetrica.CALCULADO,
            contexto=self.contexto(),
            versao_metodo="alcance-v1",
            entradas=(1000, 100),
        )

        self.assertEqual(metrica.validar(), ())


class TestComparabilidade(unittest.TestCase):
    def contexto(self, **alteracoes):
        dados = {
            "universo": "BR-18+",
            "publico_alvo": "Adultos",
            "praca": "Brasil",
            "inicio_referencia": date(2026, 7, 1),
            "fim_referencia": date(2026, 7, 31),
            "metrica_nativa": "IMPRESSOES",
            "metodologia": "Ad server",
            "granularidade": "MENSAL",
        }
        dados.update(alteracoes)
        return ContextoMetrica(**dados)

    def test_contextos_iguais_sao_comparaveis(self):
        resultado = comparar_contextos(self.contexto(), self.contexto())

        self.assertEqual(resultado.situacao, SituacaoComparabilidade.COMPARAVEL)
        self.assertTrue(resultado.permite_agregacao_direta)

    def test_divergencia_bloqueia_agregacao_direta(self):
        resultado = comparar_contextos(
            self.contexto(),
            self.contexto(universo="SP-18+"),
        )

        self.assertEqual(
            resultado.situacao,
            SituacaoComparabilidade.NAO_COMPARAVEL,
        )
        self.assertEqual(resultado.divergencias, ("universo",))

    def test_conversao_precisa_ser_explicita(self):
        resultado = comparar_contextos(
            self.contexto(metrica_nativa="IMPACTOS"),
            self.contexto(),
            conversao_explicita=True,
        )

        self.assertEqual(resultado.situacao, SituacaoComparabilidade.CONVERTIVEL)
        self.assertEqual(resultado.divergencias, ("metrica_nativa",))

    def test_metadado_ausente_deixa_resultado_indeterminado(self):
        resultado = comparar_contextos(
            self.contexto(metodologia=None),
            self.contexto(),
        )

        self.assertEqual(resultado.situacao, SituacaoComparabilidade.INDETERMINADO)
        self.assertEqual(resultado.divergencias, ("metodologia",))


if __name__ == "__main__":
    unittest.main()
