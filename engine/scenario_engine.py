from copy import deepcopy


class ScenarioEngine:

    CENARIOS = {

        "CONSERVADOR": {

            "PRINCIPAL": 1.30,

            "COMPLEMENTAR": 0.90,

            "APOIO": 0.70,

            "OPCIONAL": 0.40

        },

        "EQUILIBRADO": {

            "PRINCIPAL": 1.00,

            "COMPLEMENTAR": 1.00,

            "APOIO": 1.00,

            "OPCIONAL": 1.00

        },

        "AGRESSIVO": {

            "PRINCIPAL": 1.50,

            "COMPLEMENTAR": 1.10,

            "APOIO": 0.80,

            "OPCIONAL": 0.30

        },

        "BRANDING": {

            "PRINCIPAL": 1.20,

            "COMPLEMENTAR": 1.10,

            "APOIO": 1.00,

            "OPCIONAL": 0.80

        },

        "PERFORMANCE": {

            "PRINCIPAL": 1.40,

            "COMPLEMENTAR": 1.00,

            "APOIO": 0.80,

            "OPCIONAL": 0.50

        },

        "OMNICHANNEL": {

            "PRINCIPAL": 1.00,

            "COMPLEMENTAR": 1.20,

            "APOIO": 1.10,

            "OPCIONAL": 0.90

        }

    }

    # =====================================================
    # LISTA
    # =====================================================

    def listar(self):

        return list(

            self.CENARIOS.keys()

        )

    # =====================================================
    # APLICAR
    # =====================================================

    def aplicar(

        self,

        ranking,

        cenario="EQUILIBRADO"

    ):

        ranking = deepcopy(

            ranking

        )

        pesos = self.CENARIOS.get(

            cenario.upper(),

            self.CENARIOS["EQUILIBRADO"]

        )

        for item in ranking:

            peso = pesos.get(

                item["papel"],

                1.0

            )

            item["score"] = round(

                item["score"] * peso,

                2

            )

        ranking.sort(

            key=lambda x: x["score"],

            reverse=True

        )

        return ranking

    # =====================================================
    # COMPARAÇÃO
    # =====================================================

    def comparar(

        self,

        ranking

    ):

        resultado = {}

        for nome in self.listar():

            resultado[nome] = self.aplicar(

                ranking,

                nome

            )

        return resultado

    # =====================================================
    # RESUMO
    # =====================================================

    def resumo(

        self,

        ranking,

        cenario

    ):

        dados = self.aplicar(

            ranking,

            cenario

        )

        if not dados:

            return {
                "cenario": cenario.upper(),
                "score_medio": 0,
                "inventarios": 0,
                "principais": 0,
            }

        media = round(

            sum(

                i["score"]

                for i in dados

            )

            /

            len(dados),

            2

        )

        principais = len(

            [

                i

                for i in dados

                if i["papel"] == "PRINCIPAL"

            ]

        )

        return {

            "cenario": cenario,

            "score_medio": media,

            "principais": principais,

            "inventarios": len(

                dados

            )

        }
