from engine.mcp_engine import *


briefing = obter_briefing(

    "Lançamento SDM"

)

print(briefing)


objetivo = obter_objetivo(

    "Conversão"

)

print(objetivo)


ambientes = ambientes_por_objetivo(

    objetivo["id"]

)


for a in ambientes:

    print(a)