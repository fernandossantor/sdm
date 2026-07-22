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
    "Canais": "Meio de distribuição de mídia: {nome}.",
    "Ambientes": "Contexto em que ocorre o consumo de mídia: {nome}.",
    "Estruturas": "Estrutura de entrega do inventário: {nome}.",
    "Formatos": "Formato publicitário disponível: {nome}.",
    "Tecnologias": "Tecnologia utilizada na distribuição ou mensuração: {nome}.",
    "Modalidades": "Modalidade de contratação de mídia: {nome}.",
    "Unidades": "Unidade usada para compra e precificação: {nome}.",
    "Plataformas": "Plataforma ou veículo que disponibiliza inventário: {nome}.",
    "KPIs": "Indicador usado para avaliar o resultado da campanha: {nome}.",
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
