from statistics import mean

from infrastructure.database.admin_client import admin


def carregar(tabela):

    return (

        admin

        .table(tabela)

        .select("*")

        .execute()

        .data

    )


def contar(dados, campo):

    resultado = {}

    for item in dados:

        chave = item.get(campo)

        resultado[chave] = resultado.get(chave, 0) + 1

    return resultado


def media(dados, campo):

    valores = []

    for item in dados:

        valor = item.get(campo)

        if valor is None:

            continue

        try:

            valores.append(float(valor))

        except Exception:

            pass

    if not valores:

        return 0

    return round(mean(valores), 2)


def imprimir_contagem(titulo, dados):

    print()

    print(titulo)

    print("-" * 80)

    for chave, valor in sorted(

        dados.items(),

        key=lambda x: str(x[0])

    ):

        print(

            f"{str(chave):30} {valor:>6}"

        )


def main():

    print()

    print("=" * 80)

    print("SDM - ESTATÍSTICAS DA BASE")

    print("=" * 80)

    inventarios = carregar(

        "inventarios_v3"

    )

    objetivos = carregar(

        "inventarios_objetivos_v3"

    )

    kpis = carregar(

        "inventarios_kpis_v3"

    )

    metricas = carregar(

        "inventarios_metricas_v3"

    )

    consumo = carregar(

        "consumo_midia_v3"

    )

    print()

    print("RESUMO")

    print("-" * 80)

    print(

        f"Inventários............. {len(inventarios)}"

    )

    print(

        f"Objetivo x Inventário... {len(objetivos)}"

    )

    print(

        f"KPI x Inventário........ {len(kpis)}"

    )

    print(

        f"Métricas................ {len(metricas)}"

    )

    print(

        f"Consumo................. {len(consumo)}"

    )

    imprimir_contagem(

        "INVENTÁRIOS POR PLATAFORMA",

        contar(

            inventarios,

            "plataforma_id"

        )

    )

    imprimir_contagem(

        "INVENTÁRIOS POR AMBIENTE",

        contar(

            inventarios,

            "ambiente_id"

        )

    )

    imprimir_contagem(

        "INVENTÁRIOS POR FORMATO",

        contar(

            inventarios,

            "formato_id"

        )

    )

    print()

    print("MÉDIAS DAS MÉTRICAS")

    print("-" * 80)

    print(

        f"CTR................. {media(metricas,'ctr')}"

    )

    print(

        f"CPC................. {media(metricas,'cpc')}"

    )

    print(

        f"CPM................. {media(metricas,'cpm')}"

    )

    print(

        f"CPA................. {media(metricas,'cpa')}"

    )

    print(

        f"ROI................. {media(metricas,'roi')}"

    )

    print(

        f"ROAS................ {media(metricas,'roas')}"

    )

    print(

        f"Viewability......... {media(metricas,'viewability')}"

    )

    print(

        f"VTR................. {media(metricas,'vtr')}"

    )

    print(

        f"Frequência.......... {media(metricas,'frequencia_media')}"

    )

    print(

        f"Taxa Conversão...... {media(metricas,'taxa_conversao')}"

    )

    print()

    print("=" * 80)

    print("FIM")

    print("=" * 80)


if __name__ == "__main__":

    main()