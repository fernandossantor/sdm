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


def main():

    print()

    print("=" * 80)

    print("SDM - TESTE INTEGRADO")

    print("=" * 80)

    repo = DecisionRepository()

    planejamento = PlanejamentoService()

    forecast_engine = ForecastEngine()

    diagnostico_service = DiagnosticoService()

    comparador = ComparadorService()

    briefings = repo.listar_briefings()

    if len(briefings) == 0:

        print("Nenhum briefing encontrado.")

        return

    nome = briefings[0]["nome"]

    print()

    print("Briefing:", nome)

    plano = planejamento.gerar(

        nome

    )

    print()

    print("Plano Estratégico")

    print("-----------------")

    print("Cliente:", plano.cliente)

    print("Campanha:", plano.campanha)

    print("Objetivo:", plano.objetivo)

    print("Itens:", len(plano.itens))

    print("Verba:", plano.verba_total)

    forecast = forecast_engine.calcular(

        plano,

        repo.metricas()

    )

    print()

    print("Forecast")

    print("--------")

    print(

        "Conversões:",

        sum(

            i.conversoes

            for i in forecast

        )

    )

    print(

        "Cliques:",

        sum(

            i.cliques

            for i in forecast

        )

    )

    diagnostico = diagnostico_service.gerar(

        plano

    )

    print()

    print("Diagnóstico")

    print("-----------")

    print(

        "Score médio:",

        diagnostico.score_medio

    )

    print(

        "Principais:",

        diagnostico.principais

    )

    print()

    print("Observações")

    print("-----------")

    for obs in diagnostico.observacoes:

        print("-", obs)

    if len(briefings) > 1:

        plano2 = planejamento.gerar(

            briefings[1]["nome"]

        )

        forecast2 = forecast_engine.calcular(

            plano2,

            repo.metricas()

        )

        resultado = comparador.comparar(

            plano,

            forecast,

            plano2,

            forecast2

        )

        print()

        print("Comparador")

        print("-----------")

        print(

            "Vencedor:",

            resultado.vencedor

        )

        print(

            resultado.justificativa

        )

    print()

    print("=" * 80)

    print("TESTE FINALIZADO")

    print("=" * 80)

    print()


if __name__ == "__main__":

    main()