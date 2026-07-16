from infrastructure.database.supabase_client import supabase


for tabela in [

    "tecnologias_v3",

    "canais_v3",

    "ambientes_v3",

    "formatos_v3",

    "plataformas_v3",

    "inventarios_v3"

]:

    try:

        r = supabase.table(tabela).select("*").limit(3).execute()

        print("\n", tabela)

        print(r.data)

    except Exception as e:

        print("\nERRO", tabela)

        print(e)