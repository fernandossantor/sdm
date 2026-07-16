from infrastructure.repositories.decision_repository import DecisionRepository


repo = DecisionRepository()


print()

print("=" * 80)

print("BRIEFING")

print("=" * 80)

briefing = repo.briefing(

    "Lançamento SDM"

)

print(briefing)


print()

print("=" * 80)

print("OBJETIVO")

print("=" * 80)

objetivo = repo.objetivo(

    briefing["objetivo_id"]

)

print(objetivo)


print()

print("=" * 80)

print("AUDIÊNCIAS")

print("=" * 80)

print(

    repo.audiencias(

        briefing["id"]

    )

)


print()

print("=" * 80)

print("INVENTÁRIOS")

print("=" * 80)

print(

    len(

        repo.inventarios()

    )

)


print()

print("=" * 80)

print("OBJETIVOS x INVENTÁRIOS")

print("=" * 80)

print(

    len(

        repo.inventarios_objetivos()

    )

)


print()

print("=" * 80)

print("KPIs x INVENTÁRIOS")

print("=" * 80)

print(

    len(

        repo.inventarios_kpis()

    )

)


print()

print("=" * 80)

print("MÉTRICAS")

print("=" * 80)

print(

    len(

        repo.metricas()

    )

)