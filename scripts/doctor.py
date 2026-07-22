from infrastructure.repositories.decision_repository import DecisionRepository


repo = DecisionRepository()

briefings = repo.listar_briefings()
if not briefings:
    raise SystemExit("Nenhum briefing salvo para diagnosticar.")
ctx = repo.carregar_contexto(briefings[0]["nome"])

print()
print("=" * 80)
print("SDM DOCTOR")
print("=" * 80)


# ==========================================================
# CONTAGEM
# ==========================================================

print("\nCONTAGEM\n")

print(
    f"Inventários .............. {len(ctx['inventarios'])}"
)

print(
    f"Inventários x Objetivos .. {len(ctx['inventarios_objetivos'])}"
)

print(
    f"Inventários x KPIs ....... {len(ctx['inventarios_kpis'])}"
)

print(
    f"Métricas ................. {len(ctx['metricas'])}"
)

print(
    f"Consumo de mídia ......... {len(ctx['consumo'])}"
)

print(
    f"Audiências ............... {len(ctx['audiencias'])}"
)


# ==========================================================
# ÍNDICES
# ==========================================================

objetivos = {}

for item in ctx["inventarios_objetivos"]:

    objetivos[
        (
            item["inventario_id"],
            item["objetivo_id"]
        )
    ] = item


kpis = {}

for item in ctx["inventarios_kpis"]:

    kpis[
        (
            item["inventario_id"],
            item["kpi_id"]
        )
    ] = item


metricas = {}

for item in ctx["metricas"]:

    metricas[
        item["inventario_id"]
    ] = item


consumo = {}

for item in ctx["consumo"]:

    consumo[
        (
            item["audiencia_id"],
            item["ambiente_id"]
        )
    ] = item


# ==========================================================
# DIAGNÓSTICO
# ==========================================================

print()

print("=" * 80)

print("VALIDAÇÃO DOS INVENTÁRIOS")

print("=" * 80)

audiencia = ctx["audiencias"][0]["audiencia_id"]

objetivo = ctx["objetivo"]["id"]

for inv in ctx["inventarios"]:

    print()

    print(inv["nome"])

    print("-" * len(inv["nome"]))

    chave_obj = (

        inv["id"],

        objetivo

    )

    if chave_obj in objetivos:

        o = objetivos[chave_obj]

        print(

            "Objetivo ............ OK",

            o["score_base"],

            o["peso_manual"]

        )

    else:

        print(

            "Objetivo ............ FALTANDO"

        )

    encontrou = False

    for chave in kpis:

        if chave[0] == inv["id"]:

            encontrou = True

            k = kpis[chave]

            print(

                "KPI ................. OK",

                k["score_base"],

                k["peso_manual"]

            )

    if not encontrou:

        print(

            "KPI ................. FALTANDO"

        )

    if inv["id"] in metricas:

        m = metricas[

            inv["id"]

        ]

        print(

            "Métricas ............ OK"

        )

        print(

            "CTR:",

            m["ctr"],

            "View:",

            m["viewability"]

        )

    else:

        print(

            "Métricas ............ FALTANDO"

        )

    chave = (

        audiencia,

        inv["ambiente_id"]

    )

    if chave in consumo:

        print(

            "Consumo .............",

            consumo[chave]["score"]

        )

    else:

        print(

            "Consumo ............. NÃO ENCONTRADO"

        )

print()

print("=" * 80)

print("FIM DO DIAGNÓSTICO")

print("=" * 80)
