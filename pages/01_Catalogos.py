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

st.caption(
    "Fontes de referência para classificação: "
    "[Cenp-Meios](https://www.cenp.com.br/cenp-meios) e "
    "[IAB Brasil — Digital AdSpend](https://iabbrasil.com.br/internas/pesquisas/adspend/)."
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
    tabela = tabela.drop(columns=["descricao"], errors="ignore")
    tabela["Fonte"] = "Cenp-Meios / IAB Brasil / Base PMAH"
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
