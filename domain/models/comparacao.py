from dataclasses import dataclass


# ==========================================================
# RESULTADO DA COMPARAÇÃO
# ==========================================================

@dataclass
class ComparacaoResultado:

    vencedor: str

    score_plano_1: float

    score_plano_2: float

    conversoes_plano_1: float

    conversoes_plano_2: float

    investimento_plano_1: float

    investimento_plano_2: float

    justificativa: str

    # ------------------------------------------------------

    @property
    def diferenca_score(self):

        return round(

            abs(

                self.score_plano_1

                -

                self.score_plano_2

            ),

            2

        )

    # ------------------------------------------------------

    @property
    def diferenca_conversoes(self):

        return round(

            abs(

                self.conversoes_plano_1

                -

                self.conversoes_plano_2

            ),

            2

        )

    # ------------------------------------------------------

    @property
    def diferenca_investimento(self):

        return round(

            abs(

                self.investimento_plano_1

                -

                self.investimento_plano_2

            ),

            2

        )

    # ------------------------------------------------------

    @property
    def melhor_score(self):

        return max(

            self.score_plano_1,

            self.score_plano_2

        )

    # ------------------------------------------------------

    @property
    def melhor_conversao(self):

        return max(

            self.conversoes_plano_1,

            self.conversoes_plano_2

        )

    # ------------------------------------------------------

    @property
    def investimento_total(self):

        return round(

            self.investimento_plano_1

            +

            self.investimento_plano_2,

            2

        )