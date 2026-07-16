from engine.recommendation_engine import RecommendationEngine


class RecomendacaoService:

    def __init__(self):

        self.engine = RecommendationEngine()

    # =====================================================
    # RECOMENDAÇÕES DE UM INVENTÁRIO
    # =====================================================

    def inventario(

        self,

        item

    ):

        return self.engine.recomendar(

            item

        )

    # =====================================================
    # RESUMO DO PLANO
    # =====================================================

    def resumo(

        self,

        ranking

    ):

        return self.engine.resumo(

            ranking

        )

    # =====================================================
    # RISCOS
    # =====================================================

    def riscos(

        self,

        ranking

    ):

        return self.engine.riscos(

            ranking

        )

    # =====================================================
    # PARECER EXECUTIVO
    # =====================================================

    def parecer(

        self,

        ranking

    ):

        return {

            "resumo": self.resumo(

                ranking

            ),

            "riscos": self.riscos(

                ranking

            )

        }

    # =====================================================
    # RECOMENDAÇÕES COMPLETAS
    # =====================================================

    def plano(

        self,

        ranking

    ):

        resultado = []

        for item in ranking:

            resultado.append(

                {

                    "inventario": item["inventario"],

                    "papel": item["papel"],

                    "score": item["score"],

                    "recomendacoes": self.inventario(

                        item

                    )

                }

            )

        return resultado