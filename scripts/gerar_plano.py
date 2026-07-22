from application.services.planejamento_service import (
    PlanejamentoService
)
from application.services.context_service import ContextService


service = PlanejamentoService()

briefings = ContextService().listar_briefings()
if not briefings:
    raise SystemExit("Nenhum briefing salvo para gerar um plano.")
plano = service.gerar(briefings[0]["nome"])

print()

print("=" * 100)

print("PLANO ESTRATÉGICO DE MÍDIA")

print("=" * 100)

print()

print("Cliente:")

print(plano.cliente)

print()

print("Campanha:")

print(plano.campanha)

print()

print("Objetivo:")

print(plano.objetivo)

print()

print("Orçamento:")

print(f"R$ {plano.orcamento:,.2f}")

print()

print("-" * 100)

print("RECOMENDAÇÃO")

print("-" * 100)

print()

for indice, item in enumerate(

    plano.itens,

    start=1

):

    print(f"{indice}")

    print()

    print(

        "Inventário:",

        item.inventario

    )

    print(

        "Plataforma:",

        item.plataforma

    )

    print(

        "Ambiente:",

        item.ambiente

    )

    print(

        "Papel:",

        item.papel

    )

    print(

        "Score:",

        round(item.score,2)

    )

    print(

        "Percentual:",

        f"{item.percentual:.2f}%"

    )

    print(

        "Verba:",

        f"R$ {item.verba:,.2f}"

    )

    print()

    print("Justificativas:")

    for texto in item.justificativas:

        print(

            " •",

            texto

        )

    print()

print("-" * 100)

print()

print("RESUMO")

print()

print(

    "Itens:",

    len(plano.itens)

)

print(

    "Principais:",

    plano.principal

)

print(

    "Complementares:",

    plano.complementar

)

print(

    "Apoio:",

    plano.apoio

)

print(

    "Opcionais:",

    plano.opcional

)

print()

print(

    "Verba distribuída:",

    f"R$ {plano.verba_total:,.2f}"

)

print()

print("Observações:")

for obs in plano.observacoes:

    print(

        " •",

        obs

    )

print()

print("=" * 100)

print("FIM")

print("=" * 100)
