import pandas as pd

from infrastructure.database.admin_client import admin


def buscar_id(tabela, nome):

    resultado = (
        admin
        .table(tabela)
        .select("id,nome")
        .eq("nome", nome)
        .execute()
    )

    if not resultado.data:

        raise Exception(
            f"'{nome}' não encontrado em {tabela}"
        )

    return resultado.data[0]["id"]


df = pd.read_csv("data/inventarios_seed.csv")


sucessos = 0
erros = 0


for _, row in df.iterrows():

    try:

        registro = {

            "nome": row["nome"],

            "descricao": row["descricao"],

            "plataforma_id": buscar_id(
                "plataformas_v3",
                row["plataforma"]
            ),

            "ambiente_id": buscar_id(
                "ambientes_v3",
                row["ambiente"]
            ),

            "formato_id": buscar_id(
                "formatos_v3",
                row["formato"]
            ),

            "estrutura_id": buscar_id(
                "estruturas_v3",
                row["estrutura"]
            ),

            "modelo_comercial_id": buscar_id(
                "modelos_comerciais_v3",
                row["modelo_comercial"]
            ),

            "modalidade_compra_id": buscar_id(
                "modalidades_compra_v3",
                row["modalidade_compra"]
            ),

            "unidade_compra_id": buscar_id(
                "unidades_compra_v3",
                row["unidade_compra"]
            ),

            "ativo": True
        }


        print("\nInserindo:")
        print(registro)


        admin.table(
            "inventarios_v3"
        ).insert(
            registro
        ).execute()


        sucessos += 1

        print("✓ Inserido com sucesso")


    except Exception as e:

        erros += 1

        print("\n✗ Erro ao inserir:")

        print(row["nome"])

        print(e)



print("\n==============================")

print("IMPORTAÇÃO FINALIZADA")

print("==============================")

print(f"Sucessos: {sucessos}")

print(f"Erros: {erros}")

print("==============================")