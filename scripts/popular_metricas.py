import pandas as pd

from infrastructure.database.admin_client import admin


TABELA = "inventarios_metricas_v3"


def limpar():

    admin.table(TABELA).delete().neq(

        "inventario_id",

        -1

    ).execute()


def inserir(df):

    registros = []

    for _, linha in df.iterrows():

        registros.append(

            {

                "inventario_id": int(

                    linha["inventario_id"]

                ),

                "inventario": linha["inventario"],

                "ctr": float(

                    linha["ctr"]

                ),

                "cpc": float(

                    linha["cpc"]

                ),

                "cpm": float(

                    linha["cpm"]

                ),

                "cpa": float(

                    linha["cpa"]

                ),

                "cpl": float(

                    linha.get(

                        "cpl",

                        0

                    )

                ),

                "cpi": float(

                    linha.get(

                        "cpi",

                        0

                    )

                ),

                "roi": float(

                    linha.get(

                        "roi",

                        0

                    )

                ),

                "roas": float(

                    linha.get(

                        "roas",

                        0

                    )

                ),

                "viewability": float(

                    linha.get(

                        "viewability",

                        0

                    )

                ),

                "vtr": float(

                    linha.get(

                        "vtr",

                        0

                    )

                ),

                "frequencia_media": float(

                    linha.get(

                        "frequencia_media",

                        2.5

                    )

                ),

                "taxa_conversao": float(

                    linha.get(

                        "taxa_conversao",

                        0.03

                    )

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

    print("IMPORTAÇÃO DE MÉTRICAS")

    print("=" * 80)

    print()

    arquivo = input(

        "CSV: "

    )

    df = pd.read_csv(

        arquivo

    )

    print()

    print(

        f"{len(df)} registros encontrados."

    )

    confirmar = input(

        "Substituir dados atuais? (s/n): "

    )

    if confirmar.lower() != "s":

        print(

            "Operação cancelada."

        )

        return

    limpar()

    inserir(df)

    print()

    print(

        "Importação concluída."

    )

    print()

    print("=" * 80)


if __name__ == "__main__":

    main()