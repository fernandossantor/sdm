from domain.models.plano_tatico import (
    PlanoTatico,
    PlanoTaticoItem
)


class AllocationEngine:

    # =====================================================
    # PESOS DOS PAPÉIS
    # =====================================================

    PESOS = {

        "PRINCIPAL": 1.20,

        "COMPLEMENTAR": 1.00,

        "APOIO": 0.80,

        "OPCIONAL": 0.50

    }

    # =====================================================
    # DISTRIBUIÇÃO
    # =====================================================

    def distribuir(

        self,

        ranking,

        verba_total,

        percentual_minimo=0.03,

        percentual_maximo=0.35

    ):

        ranking = [

            item

            for item in ranking

            if item["score"] > 0

        ]

        plano = PlanoTatico(

            verba_total=verba_total

        )

        if not ranking:

            return plano

        #
        # Score ponderado
        #

        pesos = []

        for item in ranking:

            peso = self.PESOS.get(

                item["papel"],

                1.0

            )

            pesos.append(

                item["score"] * peso

            )

        total = sum(pesos)

        percentuais = []

        #
        # Distribuição inicial
        #

        for peso in pesos:

            percentual = peso / total

            percentual = max(

                percentual,

                percentual_minimo

            )

            percentual = min(

                percentual,

                percentual_maximo

            )

            percentuais.append(

                percentual

            )

        #
        # Normalização
        #

        soma = sum(percentuais)

        percentuais = [

            p / soma

            for p in percentuais

        ]

        #
        # Montagem
        #

        verba_distribuida = 0

        for indice, item in enumerate(ranking):

            percentual = percentuais[indice]

            verba = round(

                percentual * verba_total,

                2

            )

            verba_distribuida += verba

            plano.adicionar(

                PlanoTaticoItem(

                    inventario=item["inventario"],

                    plataforma=item["plataforma"],

                    ambiente=item["ambiente"],

                    papel=item["papel"],

                    percentual=round(

                        percentual * 100,

                        2

                    ),

                    verba=verba,

                    score=item["score"]

                )

            )

        #
        # Ajuste centesimal
        #

        diferenca = round(

            verba_total - verba_distribuida,

            2

        )

        if plano.itens:

            plano.itens[0].verba = round(

                plano.itens[0].verba + diferenca,

                2

            )

        return plano