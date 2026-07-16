import pandas as pd

from infrastructure.database.admin_client import admin


TABELA = "inventarios_objetivos_v3"


def limpar():

    admin.table(TABELA).delete().neq(

        "inventario_id",

        -1

    ).execute()


def validar(df):

    obrigatorias = [

        "inventario_id",

        "objetivo_id",

        "score_base",

        "peso_manual"

    ]

    faltantes = [

        coluna

        for coluna in obrigatorias

        if coluna not in df.columns

    ]

    if faltantes:

        raise Exception(

            "Colunas obrigatórias ausentes: "

            + ", ".join(faltantes)

        )

    if df.empty:

        raise Exception(

            "Arquivo CSV vazio."

        )


def inserir(df):

    registros = []

    for _, linha in df.iterrows():

        registros.append(

            {

                "inventario_id": int(

                    linha["inventario_id"]

                ),

                "objetivo_id": int(

                    linha["objetivo_id"]

                ),

                "score_base": float(

                    linha["score_base"]

                ),

                "peso_manual": float(

                    linha["peso_manual"]

                )

            }

        )

    admin.table(

        TABELA

    ).insert(

        registros

    ).execute()


def main():

    print()

    print("=" * 80)

    print("IMPORTAÇÃO INVENTÁRIO x OBJETIVO")

    print("=" * 80)

    print()

    arquivo = input(

        "Arquivo CSV: "

    ).strip()

    df = pd.read_csv(

        arquivo

    )

    validar(

        df

    )

    print()

    print(

        f"{len(df)} registros encontrados."

    )

    resposta = input(

        "Substituir tabela atual? (s/n): "

    ).strip().lower()

    if resposta != "s":

        print(

            "Operação cancelada."

        )

        return

    limpar()

    inserir(

        df

    )

    print()

    print(

        "Importação concluída com sucesso."

    )

    print()

    print("=" * 80)


if __name__ == "__main__":

    main()