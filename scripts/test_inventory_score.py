from infrastructure.repositories.decision_repository import DecisionRepository

from engine.inventory_engine import InventoryEngine


repo = DecisionRepository()

engine = InventoryEngine()


briefing = repo.briefing(

    "Lançamento SDM"

)

objetivo = repo.objetivo(

    briefing["objetivo_id"]

)


inventarios = repo.inventarios()


consumo = {

    "Search":5,

    "Retail":4,

    "Social":4.5,

    "Mensageria":2,

    "Sites":1,

    "Portais":1,

    "Vídeo":1

}


print()

print("="*100)

print("INVENTORY ENGINE")

print("="*100)

print()


resultado = []


for inv in inventarios:

    r = engine.calcular(

        inv,

        objetivo["id"],

        briefing["kpi"],

        consumo

    )

    resultado.append(r)


resultado.sort(

    key=lambda x:x["score"],

    reverse=True

)


for r in resultado:

    print(

        f'{r["inventario"]:35}'

        f'{r["score"]:8.2f}   '

        f'OBJ={r["objetivo"]} '

        f'KPI={r["kpi"]} '

        f'AUD={r["audiencia"]:.1f} '

        f'F={r["fator"]:.2f}'

    )