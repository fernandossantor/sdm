from copy import deepcopy
from statistics import mean


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

        return sorted(self.CENARIOS.keys())

    # =====================================================
    # PESOS
    # =====================================================

    def pesos(self, cenario):

        return self.CENARIOS.get(

            cenario.upper(),

            self.CENARIOS["EQUILIBRADO"]

        )

    # =====================================================
    # APLICAR
    # =====================================================

    def aplicar(

        self,

        ranking,

        cenario="EQUILIBRADO"

    ):

        pesos = self.pesos(cenario)

        resultado = deepcopy(ranking)

        for item in resultado:

            fator = pesos.get(

                item["papel"],

                1.0

            )

            item["score_original"] = item["score"]

            item["fator_cenario"] = fator

            item["score"] = round(

                item["score"] * fator,

                2

            )

        resultado.sort(

            key=lambda x: x["score"],

            reverse=True

        )

        return resultado

    # =====================================================
    # COMPARAR
    # =====================================================

    def comparar(

        self,

        ranking

    ):

        return {

            nome: self.resumo(

                ranking,

                nome

            )

            for nome in self.listar()

        }

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

        scores = [

            item["score"]

            for item in dados

        ]

        papeis = {

            "PRINCIPAL": 0,

            "COMPLEMENTAR": 0,

            "APOIO": 0,

            "OPCIONAL": 0

        }

        for item in dados:

            papel = item["papel"]

            papeis[papel] += 1

        return {

            "cenario": cenario,

            "inventarios": len(dados),

            "score_medio": round(mean(scores), 2) if scores else 0,

            "score_maximo": max(scores) if scores else 0,

            "score_minimo": min(scores) if scores else 0,

            "principais": papeis["PRINCIPAL"],

            "complementares": papeis["COMPLEMENTAR"],

            "apoio": papeis["APOIO"],

            "opcionais": papeis["OPCIONAL"],

            "ranking": dados

        }

    # =====================================================
    # MELHOR CENÁRIO
    # =====================================================

    def melhor(

        self,

        ranking

    ):

        cenarios = self.comparar(

            ranking

        )

        return max(

            cenarios.values(),

            key=lambda c: c["score_medio"]

        )

    # =====================================================
    # CENÁRIO CUSTOMIZADO
    # =====================================================

    def personalizado(

        self,

        ranking,

        pesos

    ):

        resultado = deepcopy(ranking)

        for item in resultado:

            fator = pesos.get(

                item["papel"],

                1.0

            )

            item["score_original"] = item["score"]

            item["fator_cenario"] = fator

            item["score"] = round(

                item["score"] * fator,

                2

            )

        resultado.sort(

            key=lambda x: x["score"],

            reverse=True

        )

        return resultado