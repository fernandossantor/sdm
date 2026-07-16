from engine.planner_engine import PlannerEngine


planner = PlannerEngine()

plano = planner.gerar_plano(

    "Lançamento SDM"

)


print()

print("=" * 80)

print("PLANO ESTRATÉGICO DE MÍDIA")

print("=" * 80)

print()

print("Cliente:")

print(plano.briefing.anunciante)

print()

print("Campanha:")

print(plano.briefing.nome)

print()

print("Objetivo:")

print(plano.objetivo.nome)

print()

print("Orçamento:")

print(

    f"R$ {plano.briefing.orcamento:,.2f}"

)

print()

print("-" * 80)

print("AMBIENTES")

print("-" * 80)

print()


for ambiente in plano.ambientes:

    print(

        f"{ambiente.ambiente:20}"

        f"{ambiente.percentual*100:8.2f}%"

        f"R$ {ambiente.verba:12,.2f}"

        f"   {ambiente.papel}"

    )


print()

print("-" * 80)

print("INDICADORES")

print("-" * 80)

print()


for k, v in plano.indicadores.items():

    print(

        f"{k:20}",

        v

    )


print()

print("-" * 80)

print("JUSTIFICATIVAS")

print("-" * 80)

print()


for j in plano.justificativas:

    print(

        "•",

        j

    )