import pandas as pd
import streamlit as st
from components.page_config import PAGE_ICON, titulo_pagina

from application.services.base_conhecimento_service import (
    BaseConhecimentoService
)

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title=titulo_pagina("Catálogo de Mídia"),

    page_icon=PAGE_ICON,

    layout="wide"

)

st.title("📚 Catálogo de Mídia")

st.divider()

service = BaseConhecimentoService()

dados = service.catalogos_inventario()

categorias = [
    ("Tecnologias", "tecnologias"),
    ("Canais", "canais"),
    ("Ambientes", "ambientes"),
    ("Estruturas", "estruturas"),
    ("Formatos", "formatos"),
    ("Modelos comerciais", "modelos_comerciais"),
    ("Modalidades de compra", "modalidades"),
    ("Unidades de compra", "unidades"),
    ("Meios (plataformas/empresas)", "plataformas"),
    ("KPIs", "kpis"),
]

abas = st.tabs([titulo for titulo, _ in categorias])

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
    for coluna in ("nome", "descricao"):
        if coluna not in tabela.columns:
            tabela[coluna] = ""
    tabela = tabela[["nome", "descricao"]]
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
    st.caption(
        "Fontes: [Cenp-Meios](https://www.cenp.com.br/cenp-meios), "
        "[IAB Brasil — Digital AdSpend]"
        "(https://iabbrasil.com.br/internas/pesquisas/adspend/) e Base PlanOS."
    )

for aba, (titulo, chave) in zip(abas, categorias):
    with aba:
        mostrar(dados[chave], titulo)
