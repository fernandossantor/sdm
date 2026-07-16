import pandas as pd

from infrastructure.database.admin_client import admin


TABELA = "inventarios_metricas_v3"


def carregar():

    return (

        admin

        .table(TABELA)

        .select("*")

        .order("inventario_id")

        .execute()

        .data

    )


def exportar(

    dados,

    arquivo

):

    df = pd.DataFrame(

        dados

    )

    df.to_csv(

        arquivo,

        index=False,

        encoding="utf-8-sig"

    )


def main():

    print()

    print("=" * 80)

    print("EXPORTAÇÃO DE MÉTRICAS")

    print("=" * 80)

    print()

    dados = carregar()

    print(

        f"{len(dados)} registros encontrados."

    )

    if len(dados) == 0:

        print()

        print(

            "Nenhuma métrica cadastrada."

        )

        return

    print()

    arquivo = input(

        "Arquivo de saída [metricas.csv]: "

    ).strip()

    if arquivo == "":

        arquivo = "metricas.csv"

    exportar(

        dados,

        arquivo

    )

    print()

    print(

        f"Arquivo salvo em: {arquivo}"

    )

    print()

    print("=" * 80)


if __name__ == "__main__":

    main()