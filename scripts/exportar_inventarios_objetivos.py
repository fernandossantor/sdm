import pandas as pd

from infrastructure.database.admin_client import admin


TABELA = "inventarios_objetivos_v3"


def carregar():

    return (

        admin

        .table(TABELA)

        .select("*")

        .order(

            "inventario_id"

        )

        .order(

            "objetivo_id"

        )

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

    df = df.sort_values(

        [

            "inventario_id",

            "objetivo_id"

        ]

    )

    df.to_csv(

        arquivo,

        index=False,

        encoding="utf-8-sig"

    )


def main():

    print()

    print("=" * 80)

    print("EXPORTAÇÃO INVENTÁRIO x OBJETIVO")

    print("=" * 80)

    print()

    dados = carregar()

    if not dados:

        print(

            "Nenhum registro encontrado."

        )

        return

    print(

        f"{len(dados)} registros encontrados."

    )

    print()

    arquivo = input(

        "Arquivo de saída [inventarios_objetivos.csv]: "

    ).strip()

    if arquivo == "":

        arquivo = "inventarios_objetivos.csv"

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