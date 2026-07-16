import pandas as pd
import streamlit as st

from infrastructure.repositories.catalog_repository import (
    CatalogRepository
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

repo = CatalogRepository()

dados = repo.carregar_todos()

abas = st.tabs(

    [

        "Canais",

        "Ambientes",

        "Estruturas",

        "Formatos",

        "Tecnologias",

        "Perfis",

        "Modalidades",

        "Unidades",

        "Plataformas",

        "KPIs"

    ]

)

# ==========================================================
# FUNÇÃO AUXILIAR
# ==========================================================

def mostrar(df):

    if not df:

        st.info("Nenhum registro encontrado.")

        return

    tabela = (

        pd.DataFrame(df)

        .fillna("")

    )

    st.dataframe(

        tabela,

        hide_index=True,

        use_container_width=True

    )

# ==========================================================
# ABAS
# ==========================================================

with abas[0]:

    mostrar(

        dados["canais"]

    )

with abas[1]:

    mostrar(

        dados["ambientes"]

    )

with abas[2]:

    mostrar(

        dados["estruturas"]

    )

with abas[3]:

    mostrar(

        dados["formatos"]

    )

with abas[4]:

    mostrar(

        dados["tecnologias"]

    )

with abas[5]:

    mostrar(

        dados["perfis"]

    )

with abas[6]:

    mostrar(

        dados["modalidades"]

    )

with abas[7]:

    mostrar(

        dados["unidades"]

    )

with abas[8]:

    mostrar(

        dados["plataformas"]

    )

with abas[9]:

    mostrar(

        dados["kpis"]

    )