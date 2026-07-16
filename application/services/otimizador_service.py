from dataclasses import dataclass


# ==========================================================
# RESULTADO
# ==========================================================

@dataclass
class ResultadoOtimizacao:

    inventario: str

    verba_original: float

    verba_otimizada: float

    percentual_original: float

    percentual_otimizado: float

    diferenca: float


# ==========================================================
# OTIMIZADOR
# ==========================================================

class OtimizadorService:

    def otimizar(

        self,

        plano,

        percentual_minimo=5,

        percentual_maximo=35

    ):

        itens = plano.itens

        verba_total = plano.verba_total

        score_total = sum(

            item.score

            for item in itens

        )

        resultado = []

        restante = verba_total

        restantes = len(itens)

        for item in itens:

            percentual = (

                item.score

                / score_total

            ) * 100

            percentual = max(

                percentual,

                percentual_minimo

            )

            percentual = min(

                percentual,

                percentual_maximo

            )

            verba = (

                verba_total

                * percentual

                / 100

            )

            resultado.append(

                ResultadoOtimizacao(

                    inventario=item.inventario,

                    verba_original=round(

                        item.verba,

                        2

                    ),

                    verba_otimizada=round(

                        verba,

                        2

                    ),

                    percentual_original=round(

                        item.percentual,

                        2

                    ),

                    percentual_otimizado=round(

                        percentual,

                        2

                    ),

                    diferenca=round(

                        verba - item.verba,

                        2

                    )

                )

            )

            restante -= verba

            restantes -= 1

        #
        # Ajuste fino para fechar exatamente o orçamento
        #

        if resultado:

            ajuste = round(restante, 2)

            resultado[-1].verba_otimizada = round(

                resultado[-1].verba_otimizada + ajuste,

                2

            )

            resultado[-1].diferenca = round(

                resultado[-1].verba_otimizada

                - resultado[-1].verba_original,

                2

            )

        return resultado