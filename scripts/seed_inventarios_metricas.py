import pandas as pd

from infrastructure.database.admin_client import admin



def buscar_id_inventario(nome):

    r = (

        admin

        .table("inventarios_v3")

        .select("id,nome")

        .eq("nome", nome)

        .execute()

    )


    if not r.data:

        raise Exception(

            f"Inventário não encontrado: {nome}"

        )


    return r.data[0]["id"]



df = pd.read_csv(

    "data/inventarios_metricas_seed.csv"

)



for _, row in df.iterrows():


    payload = {

        "inventario_id":

            buscar_id_inventario(

                row["inventario"]

            ),

        "cpm":

            None if pd.isna(row["cpm"])

            else float(row["cpm"]),

        "cpc":

            None if pd.isna(row["cpc"])

            else float(row["cpc"]),

        "cpv":

            None if pd.isna(row["cpv"])

            else float(row["cpv"]),

        "ctr":

            None if pd.isna(row["ctr"])

            else float(row["ctr"]),

        "viewability":

            None if pd.isna(row["viewability"])

            else float(row["viewability"]),

        "alcance_estimado":

            None if pd.isna(row["alcance_estimado"])

            else float(row["alcance_estimado"]),

        "frequencia_media":

            None if pd.isna(row["frequencia_media"])

            else float(row["frequencia_media"]),

        "capacidade_investimento":

            None if pd.isna(

                row["capacidade_investimento"]

            )

            else float(

                row["capacidade_investimento"]

            ),

        "ativo": True

    }


    print()

    print("Inserindo:")

    print(row["inventario"])


    admin.table(

        "inventarios_metricas_v3"

    ).insert(

        payload

    ).execute()


    print("✓ OK")



print()

print("======================")

print("IMPORTAÇÃO CONCLUÍDA")

print("======================")