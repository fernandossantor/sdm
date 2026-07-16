from infrastructure.database.admin_client import admin


# =====================================================
# DADOS
# =====================================================

DADOS = [

    {
        "inventario": "Google Search Ads",
        "objetivo": "Conversão",
        "score_base": 5,
        "peso_manual": 1.00,
        "papel": "PRINCIPAL",
        "observacao": "Captação direta de demanda."
    },

    {
        "inventario": "Google Responsive Search Ads",
        "objetivo": "Conversão",
        "score_base": 5,
        "peso_manual": 1.10,
        "papel": "PRINCIPAL",
        "observacao": "Maior cobertura das buscas."
    },

    {
        "inventario": "Instagram Feed Ads",
        "objetivo": "Conversão",
        "score_base": 4,
        "peso_manual": 1.00,
        "papel": "COMPLEMENTAR",
        "observacao": "Excelente desempenho para tráfego qualificado."
    },

    {
        "inventario": "Instagram Stories Ads",
        "objetivo": "Conversão",
        "score_base": 3,
        "peso_manual": 1.00,
        "papel": "APOIO",
        "observacao": "Boa resposta para campanhas promocionais."
    },

    {
        "inventario": "Instagram Reels Ads",
        "objetivo": "Conversão",
        "score_base": 3,
        "peso_manual": 0.95,
        "papel": "APOIO",
        "observacao": "Favorece descoberta de produtos."
    },

    {
        "inventario": "Facebook Feed Ads",
        "objetivo": "Conversão",
        "score_base": 2,
        "peso_manual": 0.90,
        "papel": "OPCIONAL",
        "observacao": "Uso complementar."
    },

    {
        "inventario": "Mercado Livre Retail Search",
        "objetivo": "Conversão",
        "score_base": 5,
        "peso_manual": 1.10,
        "papel": "PRINCIPAL",
        "observacao": "Alta intenção de compra."
    },

    {
        "inventario": "Mercado Livre Retail Display",
        "objetivo": "Conversão",
        "score_base": 3,
        "peso_manual": 1.00,
        "papel": "COMPLEMENTAR",
        "observacao": "Complementa Retail Search."
    },

    {
        "inventario": "Mercado Livre Retail Vídeo",
        "objetivo": "Conversão",
        "score_base": 2,
        "peso_manual": 0.95,
        "papel": "APOIO",
        "observacao": "Apoio visual ao produto."
    },

    {
        "inventario": "YouTube In-stream",
        "objetivo": "Conversão",
        "score_base": 2,
        "peso_manual": 0.85,
        "papel": "OPCIONAL",
        "observacao": "Mais indicado para reforço."
    },

    {
        "inventario": "YouTube Bumper",
        "objetivo": "Conversão",
        "score_base": 1,
        "peso_manual": 0.80,
        "papel": "OPCIONAL",
        "observacao": "Baixa eficiência para conversão."
    },

    {
        "inventario": "GloboPlay AVOD",
        "objetivo": "Conversão",
        "score_base": 1,
        "peso_manual": 0.80,
        "papel": "OPCIONAL",
        "observacao": "Inventário voltado a awareness."
    },

    {
        "inventario": "Google Display Banner",
        "objetivo": "Conversão",
        "score_base": 2,
        "peso_manual": 0.95,
        "papel": "APOIO",
        "observacao": "Excelente para remarketing."
    }

]


# =====================================================
# BUSCA IDS
# =====================================================

def buscar_id(tabela, nome):

    r = (

        admin

        .table(tabela)

        .select("id")

        .eq("nome", nome)

        .execute()

    )

    if not r.data:

        raise Exception(

            f"{nome} não encontrado em {tabela}"

        )

    return r.data[0]["id"]


# =====================================================
# INSERT
# =====================================================

for item in DADOS:

    inventario_id = buscar_id(

        "inventarios_v3",

        item["inventario"]

    )

    objetivo_id = buscar_id(

        "objetivos_campanha_v3",

        item["objetivo"]

    )

    registro = {

        "inventario_id": inventario_id,

        "objetivo_id": objetivo_id,

        "score_base": item["score_base"],

        "peso_manual": item["peso_manual"],

        "papel_preferencial": item["papel"],

        "observacao": item["observacao"],

        "ativo": True

    }

    print()

    print("Inserindo:")

    print(item["inventario"])

    try:

        admin.table(

            "inventarios_objetivos_v3"

        ).insert(

            registro

        ).execute()

        print("✓ OK")

    except Exception as e:

        print(e)

print()

print("=" * 30)

print("IMPORTAÇÃO CONCLUÍDA")

print("=" * 30)