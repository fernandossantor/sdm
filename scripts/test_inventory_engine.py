from engine.decision_engine import DecisionEngine

from engine.inventory_engine import InventoryEngine


decision = DecisionEngine()

context = decision.construir(

    "Lançamento SDM"

)

engine = InventoryEngine()

inventarios = engine.carregar(

    context

)

print()

print("=" * 80)

print("INVENTÁRIOS")

print("=" * 80)

print()

for i in inventarios:

    print(

        f"{i.inventario:35}"

        f"{i.ambiente:15}"

        f"{i.plataforma}"

    )