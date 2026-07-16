from time import perf_counter

from application.services.planejamento_service import (
    PlanejamentoService
)

from application.services.diagnostico_service import (
    DiagnosticoService
)

from engine.forecast_engine import (
    ForecastEngine
)

from infrastructure.repositories.decision_repository import (
    DecisionRepository
)


def medir(nome, func):

    inicio = perf_counter()

    resultado = func()

    fim = perf_counter()

    tempo = fim - inicio

    print(

        f"{nome:<35} {tempo:.4f} s"

    )

    return resultado


def main():

    print()

    print("=" * 80)

    print("SDM - BENCHMARK")

    print("=" * 80)

    repo = DecisionRepository()

    planejamento = PlanejamentoService()

    diagnostico = DiagnosticoService()

    forecast_engine = ForecastEngine()

    print()

    briefings = medir(

        "Carregar Briefings",

        repo.listar_briefings

    )

    if not briefings:

        print()

        print("Nenhum briefing encontrado.")

        return

    briefing = briefings[0]["nome"]

    print()

    print("Briefing utilizado:")

    print(briefing)

    print()

    contexto = medir(

        "Carregar Contexto",

        lambda: repo.carregar_contexto(

            briefing

        )

    )

    plano = medir(

        "Planejamento",

        lambda: planejamento.gerar(

            briefing

        )

    )

    forecast = medir(

        "Forecast",

        lambda: forecast_engine.calcular(

            plano,

            contexto["metricas"]

        )

    )

    diag = medir(

        "Diagnóstico",

        lambda: diagnostico.gerar(

            plano

        )

    )

    print()

    print("-" * 80)

    print()

    print("Resumo")

    print()

    print(

        f"Inventários .......... {len(plano.itens)}"

    )

    print(

        f"Score Médio .......... {diag.score_medio}"

    )

    print(

        f"Conversões ........... {sum(f.conversoes for f in forecast)}"

    )

    print(

        f"Investimento ......... R$ {plano.verba_total:,.2f}"

    )

    print()

    print("=" * 80)

    print("BENCHMARK FINALIZADO")

    print("=" * 80)

    print()


if __name__ == "__main__":

    main()