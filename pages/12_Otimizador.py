import pandas as pd
import streamlit as st
from components.page_config import PAGE_ICON, titulo_pagina
from components.formatters import dataframe_ptbr, moeda_ptbr

from application.services.budget_optimizer_service import (
    BudgetOptimizerService
)
from application.services.context_service import (
    ContextService
)
from application.services.planejamento_service import PlanejamentoService
from components.planning_selector import selecionar_planejamento


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title=titulo_pagina("Simulação Heurística de Verba"),

    page_icon=PAGE_ICON,

    layout="wide"

)

st.title("💰 Simulação Heurística de Verba")
st.info(
    "Esta ferramenta redistribui a verba proporcionalmente ao score e aplica "
    "ajustes sequenciais. Não usa solver e não afirma encontrar um ótimo."
)

st.divider()

contexto_service = ContextService()
origem = selecionar_planejamento(PlanejamentoService(), "otimizador_planejamento")

# ==========================================================
# PARÂMETROS
# ==========================================================

st.subheader("Parâmetros")

col1, col2, col3 = st.columns(3)

with col1:

    percentual_teste = st.slider(

        "Reserva para testes (%)",

        0,

        30,

        5

    )

with col2:

    minimo = st.slider(

        "Percentual mínimo por ambiente (%)",

        0,

        30,

        5

    )

with col3:

    maximo = st.slider(

        "Percentual máximo por ambiente (%)",

        10,

        100,

        50

    )

executar = st.button(

    "Simular redistribuição",

    type="primary",

    width="stretch"

)

# ==========================================================
# EXECUÇÃO
# ==========================================================

if executar:

    plano_atual = origem["plano"]
    ranking = [
        {
            "inventario": item.inventario,
            "plataforma": item.plataforma,
            "ambiente": item.ambiente,
            "papel": item.papel,
            "score": item.score,
        }
        for item in plano_atual.itens
    ]
    verba = plano_atual.orcamento

    ambientes = {

        item["ambiente"]

        for item in ranking

    }

    minimo_ambiente = {

        ambiente:

        verba * minimo / 100

        for ambiente in ambientes

    }

    maximo_ambiente = {

        ambiente:

        verba * maximo / 100

        for ambiente in ambientes

    }

    try:
        resultado = BudgetOptimizerService().otimizar(
            ranking=ranking,
            verba_total=verba,
            minimo_ambiente=minimo_ambiente,
            maximo_ambiente=maximo_ambiente,
            percentual_teste=percentual_teste / 100,
        )
    except ValueError as erro:
        st.error(str(erro))
    else:
        st.session_state["otimizacao"] = resultado

# ==========================================================
# RESULTADO
# ==========================================================

if "otimizacao" in st.session_state:

    resultado = st.session_state["otimizacao"]

    resumo = BudgetOptimizerService().resumo(

        resultado

    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Inventários",

        resumo["inventarios"]

    )

    c2.metric(

        "Investimento (R$)",

        moeda_ptbr(resumo["verba_total"])

    )

    c3.metric(

        "Distribuído (R$)",

        moeda_ptbr(resumo["verba_distribuida"])

    )

    c4.metric(

        "Reserva (R$)",

        moeda_ptbr(resumo["reserva_testes"])

    )
    st.caption(
        f"Método: {resumo['metodo']} · versão: "
        f"{resumo['versao_metodo']} · ótimo comprovado: não · "
        f"condição: {resumo['condicao_viabilidade']}."
    )

    st.divider()

    df = pd.DataFrame(

        resultado["itens"]

    )

    st.dataframe(

        dataframe_ptbr(df, moedas=["verba"], percentuais=["percentual"], decimais=["score"]),

        hide_index=True,

        width="stretch",

    )

    st.divider()

    st.subheader("Distribuição por Ambiente")

    ambiente = BudgetOptimizerService().ambiente(

        resultado

    )

    st.dataframe(

        dataframe_ptbr(pd.DataFrame(

            [

                {

                    "Ambiente": k,

                    "Verba": v

                }

                for k, v in ambiente.items()

            ]

        ), moedas=["Verba"]),

        hide_index=True,

        width="stretch",

    )

    st.subheader("Distribuição por Plataforma")

    plataforma = BudgetOptimizerService().plataforma(

        resultado

    )

    st.dataframe(

        dataframe_ptbr(pd.DataFrame(

            [

                {

                    "Plataforma": k,

                    "Verba": v

                }

                for k, v in plataforma.items()

            ]

        ), moedas=["Verba"]),

        hide_index=True,

        width="stretch",

    )

    if BudgetOptimizerService().validar(

        resultado

    ):

        st.success(

            "Simulação heurística reconciliada com a verba."

        )

    else:

        st.error(

            "Simulação inviável com os limites informados. "
            f"Sobra/déficit: {moeda_ptbr(resumo['saldo_orcamento'])}."
        )
