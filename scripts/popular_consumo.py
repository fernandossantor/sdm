import pandas as pd

from infrastructure.database.admin_client import admin


TABELA = "consumo_midia_v3"


def limpar():

    admin.table(TABELA).delete().neq(

        "audiencia_id",

        -1

    ).execute()


def inserir(df):

    registros = []

    for _, linha in df.iterrows():

        registros.append(

            {

                "audiencia_id": int(

                    linha["audiencia_id"]

                ),

                "ambiente_id": int(

                    linha["ambiente_id"]

                ),

                "score": float(

                    linha["score"]

                )

            }

        )

    admin.table(

        TABELA

    ).insert(

        registros

    ).execute()


def validar(df):

    obrigatorias = [

        "audiencia_id",

        "ambiente_id",

        "score"

    ]

    faltantes = [

        c

        for c in obrigatorias

        if c not in df.columns

    ]

    if faltantes:

        raise Exception(

            f"Colunas ausentes: {', '.join(faltantes)}"

        )

    if df.empty:

        raise Exception(

            "Arquivo vazio."

        )


def main():

    print()

    print("=" * 80)

    print("IMPORTAÇÃO DE CONSUMO DE MÍDIA")

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

    confirmar = input(

        "Substituir base atual? (s/n): "

    )

    if confirmar.lower() != "s":

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

        "Base de consumo atualizada com sucesso."

    )

    print()

    print("=" * 80)


if __name__ == "__main__":

    main()