from domain.models.comparacao import ComparacaoResultado


class ComparadorService:

    # =====================================================
    # COMPARAÇÃO
    # =====================================================

    def comparar(

        self,

        plano1,

        forecast1,

        plano2,

        forecast2

    ):

        score1 = self._score_medio(

            plano1

        )

        score2 = self._score_medio(

            plano2

        )

        conv1 = self._conversoes(

            forecast1

        )

        conv2 = self._conversoes(

            forecast2

        )

        inv1 = plano1.verba_total

        inv2 = plano2.verba_total

        if (

            score1 > score2

            and

            conv1 >= conv2

        ):

            vencedor = plano1.campanha

            justificativa = (

                "Maior score estratégico e desempenho previsto."

            )

        elif (

            score2 > score1

            and

            conv2 >= conv1

        ):

            vencedor = plano2.campanha

            justificativa = (

                "Maior score estratégico e desempenho previsto."

            )

        elif conv1 > conv2:

            vencedor = plano1.campanha

            justificativa = (

                "Maior potencial de conversão."

            )

        elif conv2 > conv1:

            vencedor = plano2.campanha

            justificativa = (

                "Maior potencial de conversão."

            )

        else:

            vencedor = "Empate"

            justificativa = (

                "Os cenários apresentam desempenho equivalente."

            )

        return ComparacaoResultado(

            vencedor=vencedor,

            score_plano_1=round(

                score1,

                2

            ),

            score_plano_2=round(

                score2,

                2

            ),

            conversoes_plano_1=round(

                conv1,

                2

            ),

            conversoes_plano_2=round(

                conv2,

                2

            ),

            investimento_plano_1=round(

                inv1,

                2

            ),

            investimento_plano_2=round(

                inv2,

                2

            ),

            justificativa=justificativa

        )

    # =====================================================
    # SCORE MÉDIO
    # =====================================================

    def _score_medio(

        self,

        plano

    ):

        if not plano.itens:

            return 0

        return sum(

            item.score

            for item in plano.itens

        ) / len(

            plano.itens

        )

    # =====================================================
    # CONVERSÕES
    # =====================================================

    def _conversoes(

        self,

        forecast

    ):

        return sum(

            item.conversoes

            for item in forecast

        )
