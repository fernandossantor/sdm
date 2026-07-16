from infrastructure.database.admin_client import admin


# ==========================================================
# MATRIZ INVENTÁRIO x KPI
# ==========================================================

DADOS = [

    # ------------------------------------------------------
    # GOOGLE SEARCH
    # ------------------------------------------------------

    ("Google Search Ads", "Conversões", 5, 1.00,
     "Excelente para conversões."),

    ("Google Search Ads", "CPA", 5, 1.05,
     "Alta eficiência em CPA."),

    ("Google Search Ads", "CTR", 5, 1.00,
     "Elevada taxa de cliques."),

    ("Google Search Ads", "Cliques", 5, 1.00,
     "Captura demanda ativa."),

    ("Google Search Ads", "ROAS", 5, 1.10,
     "Excelente retorno."),

    ("Google Search Ads", "CPC", 5, 1.00,
     "Controle preciso do CPC."),


    # ------------------------------------------------------
    # RESPONSIVE SEARCH
    # ------------------------------------------------------

    ("Google Responsive Search Ads","Conversões",5,1.10,
     "Otimização automática."),

    ("Google Responsive Search Ads","CPA",5,1.10,
     "Excelente desempenho."),

    ("Google Responsive Search Ads","CTR",5,1.10,
     "Maior cobertura."),

    ("Google Responsive Search Ads","ROAS",5,1.10,
     "Ótimo retorno."),


    # ------------------------------------------------------
    # INSTAGRAM FEED
    # ------------------------------------------------------

    ("Instagram Feed Ads","Engajamento",5,1.00,
     "Excelente interação."),

    ("Instagram Feed Ads","Conversões",4,1.00,
     "Bom desempenho."),

    ("Instagram Feed Ads","Leads",4,1.00,
     "Boa geração de leads."),

    ("Instagram Feed Ads","CTR",4,1.00,
     "Bom CTR."),


    # ------------------------------------------------------
    # STORIES
    # ------------------------------------------------------

    ("Instagram Stories Ads","Engajamento",5,1.00,
     "Muito utilizado."),

    ("Instagram Stories Ads","Conversões",3,1.00,
     "Bom apoio."),

    ("Instagram Stories Ads","Leads",3,1.00,
     "Apoio."),


    # ------------------------------------------------------
    # REELS
    # ------------------------------------------------------

    ("Instagram Reels Ads","Engajamento",5,1.10,
     "Excelente alcance."),

    ("Instagram Reels Ads","Viewability",5,1.10,
     "Alta visualização."),

    ("Instagram Reels Ads","VTR",5,1.10,
     "Excelente retenção."),

    ("Instagram Reels Ads","Conversões",3,0.95,
     "Conversão indireta."),


    # ------------------------------------------------------
    # FACEBOOK
    # ------------------------------------------------------

    ("Facebook Feed Ads","Engajamento",3,1.00,
     "Uso complementar."),

    ("Facebook Feed Ads","Conversões",2,0.90,
     "Baixa prioridade."),


    # ------------------------------------------------------
    # DISPLAY
    # ------------------------------------------------------

    ("Google Display Banner","Viewability",5,1.10,
     "Excelente viewability."),

    ("Google Display Banner","Impressões",5,1.00,
     "Grande cobertura."),

    ("Google Display Banner","CPM",5,1.00,
     "Excelente CPM."),


    # ------------------------------------------------------
    # YOUTUBE
    # ------------------------------------------------------

    ("YouTube In-stream","VTR",5,1.10,
     "Excelente VTR."),

    ("YouTube In-stream","Viewability",5,1.05,
     "Alta visualização."),

    ("YouTube In-stream","Alcance",5,1.00,
     "Grande cobertura."),

    ("YouTube Bumper","Alcance",5,1.00,
     "Alta cobertura."),

    ("YouTube Bumper","CPM",5,1.00,
     "Excelente custo."),


    # ------------------------------------------------------
    # GLOBOPLAY
    # ------------------------------------------------------

    ("GloboPlay AVOD","Alcance",5,1.00,
     "Cobertura."),

    ("GloboPlay AVOD","Frequência",5,1.00,
     "Excelente frequência."),


    # ------------------------------------------------------
    # RETAIL
    # ------------------------------------------------------

    ("Mercado Livre Retail Search","Conversões",5,1.10,
     "Alta intenção de compra."),

    ("Mercado Livre Retail Search","ROAS",5,1.10,
     "Excelente retorno."),

    ("Mercado Livre Retail Search","CPA",5,1.10,
     "Baixo CPA."),

    ("Mercado Livre Retail Display","Conversões",3,1.00,
     "Complemento."),

    ("Mercado Livre Retail Vídeo","Viewability",4,1.00,
     "Boa exposição.")
]


# ==========================================================
# BUSCAR IDS
# ==========================================================

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


# ==========================================================
# INSERT
# ==========================================================

for inventario,kpi,score,peso,obs in DADOS:

    registro = {

        "inventario_id":

            buscar_id(

                "inventarios_v3",

                inventario

            ),

        "kpi_id":

            buscar_id(

                "kpis_v3",

                kpi

            ),

        "score_base":

            score,

        "peso_manual":

            peso,

        "observacao":

            obs,

        "ativo":

            True

    }

    print(f"Inserindo {inventario} -> {kpi}")

    admin.table(

        "inventarios_kpis_v3"

    ).insert(

        registro

    ).execute()

print()

print("="*40)

print("IMPORTAÇÃO FINALIZADA")

print("="*40)