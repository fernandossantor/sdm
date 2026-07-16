from engine.insights_engine import InsightsEngine


class InsightsService:

    def __init__(self):

        self.engine = InsightsEngine()

    # =====================================================
    # INSIGHTS
    # =====================================================

    def gerar(

        self,

        plano,

        forecast=None

    ):

        return self.engine.gerar(

            plano,

            forecast

        )

    # =====================================================
    # RESUMO EXECUTIVO
    # =====================================================

    def resumo(

        self,

        plano,

        forecast=None,

        limite=5

    ):

        insights = self.gerar(

            plano,

            forecast

        )

        return insights[:limite]

    # =====================================================
    # RELATÓRIO
    # =====================================================

    def relatorio(

        self,

        plano,

        forecast=None

    ):

        return {

            "cliente": plano.cliente,

            "campanha": plano.campanha,

            "objetivo": plano.objetivo,

            "investimento": plano.verba_total,

            "inventarios": len(plano.itens),

            "insights": self.gerar(

                plano,

                forecast

            )

        }

    # =====================================================
    # TEXTO
    # =====================================================

    def texto(

        self,

        plano,

        forecast=None

    ):

        linhas = []

        linhas.append(

            f"Cliente: {plano.cliente}"

        )

        linhas.append(

            f"Campanha: {plano.campanha}"

        )

        linhas.append(

            f"Objetivo: {plano.objetivo}"

        )

        linhas.append(

            f"Investimento: R$ {plano.verba_total:,.2f}"

        )

        linhas.append("")

        linhas.append(

            "Principais Insights"

        )

        linhas.append(

            "-" * 40

        )

        for insight in self.gerar(

            plano,

            forecast

        ):

            linhas.append(

                f"• {insight}"

            )

        return "\n".join(

            linhas

        )