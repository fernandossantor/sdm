from engine.budget_optimizer import (
    BudgetOptimizer
)


class BudgetOptimizerService:

    def __init__(self):

        self.optimizer = BudgetOptimizer()

    # =====================================================
    # OTIMIZAÇÃO
    # =====================================================

    def otimizar(

        self,

        ranking,

        verba_total,

        minimo_ambiente=None,

        maximo_ambiente=None,

        minimo_plataforma=None,

        maximo_plataforma=None,

        obrigatorios=None,

        excluidos=None,

        percentual_teste=0

    ):

        return self.optimizer.otimizar(

            ranking=ranking,

            verba_total=verba_total,

            minimo_ambiente=minimo_ambiente,

            maximo_ambiente=maximo_ambiente,

            minimo_plataforma=minimo_plataforma,

            maximo_plataforma=maximo_plataforma,

            obrigatorios=obrigatorios,

            excluidos=excluidos,

            percentual_teste=percentual_teste

        )

    # =====================================================
    # RESUMO
    # =====================================================

    def resumo(

        self,

        resultado

    ):

        itens = resultado["itens"]

        return {

            "inventarios": len(itens),

            "verba_total": resultado["verba_total"],

            "verba_distribuida": resultado["verba_distribuida"],

            "reserva_testes": resultado["reserva_testes"],

            "maior_investimento": max(

                itens,

                key=lambda x: x["verba"]

            )["inventario"]

            if itens else None,

            "maior_verba": max(

                (

                    item["verba"]

                    for item in itens

                ),

                default=0

            )

        }

    # =====================================================
    # AGRUPAR POR AMBIENTE
    # =====================================================

    def ambiente(

        self,

        resultado

    ):

        agrupado = {}

        for item in resultado["itens"]:

            nome = item["ambiente"]

            agrupado[nome] = agrupado.get(

                nome,

                0

            ) + item["verba"]

        return agrupado

    # =====================================================
    # AGRUPAR POR PLATAFORMA
    # =====================================================

    def plataforma(

        self,

        resultado

    ):

        agrupado = {}

        for item in resultado["itens"]:

            nome = item["plataforma"]

            agrupado[nome] = agrupado.get(

                nome,

                0

            ) + item["verba"]

        return agrupado

    # =====================================================
    # VALIDAÇÃO
    # =====================================================

    def validar(

        self,

        resultado,

        tolerancia=0.01

    ):

        diferenca = abs(

            resultado["verba_total"]

            -

            (

                resultado["verba_distribuida"]

                +

                resultado["reserva_testes"]

            )

        )

        return diferenca <= tolerancia