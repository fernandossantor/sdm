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

        ids_com_metricas = {
            metrica.get("inventario_id") for metrica in metricas
            if metrica.get("inventario_id")
        }
        nomes_com_metricas = {
            metrica.get("inventario") for metrica in metricas
            if metrica.get("inventario")
        }
        self.check(

            len(forecast) == len(plano.itens),

            "Forecast preserva todos os inventários do plano."

        )
        por_nome = {item.inventario: item for item in forecast}
        sem_defaults = all(
            (
                getattr(item, "inventario_id", None) in ids_com_metricas
                or item.inventario in nomes_com_metricas
                or getattr(item, "impressoes_estimadas", None) is not None
                or (
                    por_nome[item.inventario].impressoes is None
                    and bool(por_nome[item.inventario].lacunas)
                )
            )
            for item in plano.itens
        )
        self.check(
            sem_defaults,
            "Forecast não preenche lacunas com defaults silenciosos."
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

            try:
                resultado = self.comparador.comparar(
                    plano,
                    forecast,
                    plano2,
                    forecast2,
                )
            except ValueError as erro:
                self.check(
                    "premissas explícitas" in str(erro),
                    "Comparador bloqueia conversões incompletas."
                )
            else:
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
