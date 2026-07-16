from infrastructure.database.admin_client import admin


tabelas = [

    "plataformas_v3",

    "ambientes_v3",

    "formatos_v3",

    "estruturas_v3",

    "modelos_comerciais_v3",

    "modalidades_compra_v3",

    "unidades_compra_v3"

]


for t in tabelas:

    print("\n===================")

    print(t)

    print("===================\n")


    r = (

        admin

        .table(t)

        .select("nome")

        .order("nome")

        .execute()

    )


    for x in r.data:

        print(x["nome"])