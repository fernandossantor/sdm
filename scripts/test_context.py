from infrastructure.repositories.decision_repository import DecisionRepository
from engine.inventory_engine import InventoryEngine


def main():

    print()
    print("=" * 100)
    print("SDM - INVENTORY ENGINE")
    print("=" * 100)

    repo = DecisionRepository()

    contexto = repo.carregar_contexto(
        "Lançamento SDM"
    )

    print()
    print("Briefing:")
    print(contexto["briefing"]["nome"])

    print()
    print("Objetivo:")
    print(contexto["objetivo"]["nome"])

    print()
    print("KPI:")
    print(contexto["briefing"]["kpi"])

    print()
    print("Inventários carregados:",
          len(contexto["inventarios"]))

    print("Objetivos carregados:",
          len(contexto["inventarios_objetivos"]))

    print("KPIs carregados:",
          len(contexto["inventarios_kpis"]))

    print("Métricas carregadas:",
          len(contexto["metricas"]))

    print("Consumo carregado:",
          len(contexto["consumo"]))

    engine = InventoryEngine()

    ranking = engine.calcular(
        contexto
    )

    print()
    print("=" * 100)
    print("RANKING DOS INVENTÁRIOS")
    print("=" * 100)
    print()

    print(
        f'{"Inventário":35}'
        f'{"Ambiente":18}'
        f'{"Score":>10}'
        f'{"Papel":>18}'
    )

    print("-" * 100)

    for item in ranking:

        print(

            f'{item["inventario"]:35}'

            f'{item["ambiente"]:18}'

            f'{item["score"]:10.2f}'

            f'{item["papel"]:>18}'

        )

    print()

    print("=" * 100)
    print("TOP 5")
    print("=" * 100)
    print()

    for posicao, item in enumerate(ranking[:5], start=1):

        print(f"{posicao}º")

        print("Inventário :", item["inventario"])

        print("Plataforma :", item["plataforma"])

        print("Ambiente   :", item["ambiente"])

        print("Score      :", item["score"])

        print("Papel      :", item["papel"])

        print()

    print("=" * 100)
    print("FIM")
    print("=" * 100)


if __name__ == "__main__":
    main()