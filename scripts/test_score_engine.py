from engine.briefing_engine import (

    obter_briefing,

    obter_objetivo,

    obter_audiencias

)

from engine.score_engine import (

    calcular_scores

)


briefing = obter_briefing(

    "Lançamento SDM"

)


objetivo = obter_objetivo(

    briefing.objetivo_id

)


audiencias = obter_audiencias(

    briefing.id

)


ranking = calcular_scores(

    objetivo,

    audiencias

)


print()

print("=" * 70)

print("SCORE ENGINE")

print("=" * 70)

print()


for ambiente in ranking:

    print(

        f"{ambiente.ambiente:20}",

        f"{ambiente.score:7.2f}",

        ambiente.papel

    )