import pandas as pd
import streamlit as st

from application.services.base_conhecimento_service import (
    BaseConhecimentoService
)

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Catálogos",

    page_icon="📚",

    layout="wide"

)

st.title("📚 Catálogos")

st.divider()

with st.expander("Contexto do mercado brasileiro", expanded=True):
    st.markdown(
        "Em 2024, o painel Cenp-Meios registrou **R$ 26,3 bilhões** em "
        "investimentos feitos por 339 agências, crescimento de **12,17%**. "
        "TV aberta respondeu por **42,4%**, internet por **39,8%** e OOH por "
        "**11,8%**. Use esses dados como referência de mercado — não como "
        "distribuição automática de verba, que deve seguir público, objetivo, "
        "cobertura, frequência e disponibilidade de inventário."
    )
    st.markdown(
        "Fontes: [Cenp-Meios — consolidado 2024]"
        "(https://www.cenp.com.br/post/investimento-em-publicidade-no-mercado-brasileiro-cresce-12-17-em-2024-de-acordo-com-painel-cenp-m) "
        "e [IAB Brasil — Digital AdSpend]"
        "(https://iabbrasil.com.br/internas/pesquisas/adspend/)."
    )

service = BaseConhecimentoService()

dados = service.carregar_catalogos()

abas = st.tabs(

    [

        "Canais",

        "Ambientes",

        "Estruturas",

        "Formatos",

        "Tecnologias",

        "Modalidades",

        "Unidades",

        "Plataformas",

        "KPIs"

    ]

)

# ==========================================================
# FUNÇÃO AUXILIAR
# ==========================================================

DESCRICOES = {
    "Canais": "Avaliar contribuição para alcance incremental, frequência, custo e papel no mix.",
    "Ambientes": "Considerar contexto de exposição, atenção, brand safety e disponibilidade regional.",
    "Estruturas": "Define como a entrega é organizada e quais combinações comerciais são possíveis.",
    "Formatos": "Comparar duração, área, interação, atenção e compatibilidade com a criação.",
    "Tecnologias": "Verificar segmentação, mensuração, interoperabilidade e transparência da entrega.",
    "Modalidades": "Relacionar o modelo de compra ao risco, à previsibilidade e ao KPI contratado.",
    "Unidades": "Base operacional para calcular quantidade, preço, entrega e comparação de eficiência.",
    "Plataformas": "Avaliar cobertura, qualidade do inventário, dados disponíveis e sobreposição de público.",
    "KPIs": "Vincular a uma fonte de dados, fórmula, periodicidade e meta antes da veiculação.",
}


def mostrar(df, categoria):

    if not df:

        st.info("Nenhum registro encontrado.")

        return

    tabela = pd.DataFrame(df).fillna("")
    ocultas = {
        coluna for coluna in tabela.columns
        if coluna == "id" or coluna.endswith("_id")
        or coluna in {"criado_em", "atualizado_em", "ativo"}
    }
    tabela = tabela.drop(columns=list(ocultas), errors="ignore")
    if "descricao" in tabela.columns:
        tabela["descricao"] = tabela.apply(
            lambda linha: linha["descricao"] or DESCRICOES[categoria].format(
                nome=linha.get("nome", "")
            ),
            axis=1,
        )
    nomes = {
        "nome": "Nome", "descricao": "Descrição", "empresa": "Empresa",
        "site": "Site", "sigla": "Sigla", "tipo": "Tipo",
    }
    tabela = tabela.rename(columns=nomes)

    st.dataframe(

        tabela,

        hide_index=True,

        width="stretch"

    )

# ==========================================================
# ABAS
# ==========================================================

with abas[0]:

    mostrar(

        dados["canais"], "Canais"

    )

with abas[1]:

    mostrar(

        dados["ambientes"], "Ambientes"

    )

with abas[2]:

    mostrar(

        dados["estruturas"], "Estruturas"

    )

with abas[3]:

    mostrar(

        dados["formatos"], "Formatos"

    )

with abas[4]:

    mostrar(

        dados["tecnologias"], "Tecnologias"

    )

with abas[5]:

    mostrar(

        dados["modalidades"], "Modalidades"

    )

with abas[6]:

    mostrar(

        dados["unidades"], "Unidades"

    )

with abas[7]:

    mostrar(

        dados["plataformas"], "Plataformas"

    )

with abas[8]:

    mostrar(

        dados["kpis"], "KPIs"

    )
