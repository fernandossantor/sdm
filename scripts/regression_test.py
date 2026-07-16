from application.services.planejamento_service import (
    PlanejamentoService
)

from application.services.diagnostico_service import (
    DiagnosticoService
)

from application.services.comparador_service import (
    ComparadorService
)

from engine.forecast_engine import (
    ForecastEngine
)

from infrastructure.repositories.decision_repository import (
    DecisionRepository
)


class RegressionTest:

    def __init__(self):

        self.repo = DecisionRepository()

        self.planejamento = PlanejamentoService()

        self.forecast = ForecastEngine()

        self.diagnostico = DiagnosticoService()

        self.comparador = ComparadorService()

    # =====================================================
    # ASSERT
    # =====================================================

    def check(

        self,

        condicao,

        mensagem

    ):

        if condicao:

            print(

                f"[ OK ] {mensagem}"

            )

        else:

            raise AssertionError(

                mensagem

            )

    # =====================================================
    # EXECUÇÃO
    # =====================================================

    def executar(self):

        briefings = self.repo.listar_briefings()

        self.check(

            len(briefings) > 0,

            "Existem briefings."

        )

        metricas = self.repo.metricas()

        self.check(

            len(metricas) > 0,

            "Existem métricas."

        )

        nome = briefings[0]["nome"]

        plano = self.planejamento.gerar(

            nome

        )

        self.check(

            len(plano.itens) > 0,

            "Plano possui inventários."

        )

        self.check(

            plano.verba_total > 0,

            "Plano possui verba."

        )

        forecast = self.forecast.calcular(

            plano,

            metricas

        )

        self.check(

            len(forecast) == len(plano.itens),

            "Forecast consistente."

        )

        diagnostico = self.diagnostico.gerar(

            plano

        )

        self.check(

            diagnostico.score_medio >= 0,

            "Diagnóstico gerado."

        )

        if len(briefings) > 1:

            plano2 = self.planejamento.gerar(

                briefings[1]["nome"]

            )

            forecast2 = self.forecast.calcular(

                plano2,

                metricas

            )

            resultado = self.comparador.comparar(

                plano,

                forecast,

                plano2,

                forecast2

            )

            self.check(

                resultado.vencedor is not None,

                "Comparador executado."

            )


def main():

    print()

    print("=" * 80)

    print("SDM - REGRESSION TEST")

    print("=" * 80)

    RegressionTest().executar()

    print()

    print("=" * 80)

    print("TODOS OS TESTES PASSARAM")

    print("=" * 80)

    print()


if __name__ == "__main__":

    main()