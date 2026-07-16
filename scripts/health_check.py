from infrastructure.database.admin_client import admin


TABELAS = [

    "briefings_v3",

    "audiencias_v3",

    "briefing_audiencias_v3",

    "objetivos_campanha_v3",

    "kpis_v3",

    "inventarios_v3",

    "inventarios_objetivos_v3",

    "inventarios_kpis_v3",

    "inventarios_metricas_v3",

    "consumo_midia_v3"

]


def verificar_tabela(nome):

    try:

        dados = (

            admin

            .table(nome)

            .select("*", count="exact")

            .limit(1)

            .execute()

        )

        return True, dados.count

    except Exception as e:

        return False, str(e)


def main():

    print()

    print("=" * 80)

    print("SDM - HEALTH CHECK")

    print("=" * 80)

    total = 0

    erros = 0

    print()

    print("VERIFICAÇÃO DAS TABELAS")

    print()

    for tabela in TABELAS:

        ok, valor = verificar_tabela(

            tabela

        )

        total += 1

        if ok:

            print(

                f"[ OK ] {tabela:<35} {valor} registros"

            )

        else:

            erros += 1

            print(

                f"[ERRO] {tabela:<35} {valor}"

            )

    print()

    print("-" * 80)

    print()

    if erros == 0:

        print(

            "STATUS: AMBIENTE ÍNTEGRO"

        )

    else:

        print(

            f"STATUS: {erros} PROBLEMA(S) ENCONTRADO(S)"

        )

    print()

    print(

        f"Tabelas verificadas : {total}"

    )

    print(

        f"Erros encontrados   : {erros}"

    )

    print()

    print("=" * 80)


if __name__ == "__main__":

    main()