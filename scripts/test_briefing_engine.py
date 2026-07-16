from engine.briefing_engine import (

    obter_briefing,

    obter_objetivo,

    obter_audiencias

)


briefing = obter_briefing(

    "Lançamento SDM"

)

print()

print("BRIEFING")

print(briefing)

print()


objetivo = obter_objetivo(

    briefing.objetivo_id

)

print("OBJETIVO")

print(objetivo)

print()


print("AUDIÊNCIAS")

for audiencia in obter_audiencias(

    briefing.id

):

    print(audiencia)