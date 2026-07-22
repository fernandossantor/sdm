import streamlit as st

from application.services.planejamento_service import (
    PlanejamentoService
)

from application.services.forecast_service import (
    ForecastService
)

from application.services.context_service import (
    ContextService
)
from application.services.workflow_service import WorkflowService
from components.workflow_guard import exigir
from components.planning_selector import selecionar_planejamento
from components.formatters import (
    dataframe_ptbr, moeda_ptbr, numero_ptbr, percentual_ptbr,
)
from application.services.workflow_artifact_service import WorkflowArtifactService
from components.artifact_manager import render as gerenciar_artefatos


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Projeção de Resultados",

    page_icon="📈",

    layout="wide"

)

exigir("forecast")

st.title("📈 Projeção de Resultados")

st.divider()

contexto_service = ContextService()

planejamento = PlanejamentoService()

forecast_service = ForecastService()

workflow_service = WorkflowService()
artefatos = WorkflowArtifactService()

origem = selecionar_planejamento(planejamento, "forecast_planejamento")
gerenciar_artefatos(artefatos, "FORECAST", "Projeções de resultados")

if st.button(

    "Gerar projeção de resultados",

    type="primary",

    width="stretch"

):

    plano = origem["plano"]

    forecast = forecast_service.gerar(

        plano,

        contexto_service.metricas()

    )

    workflow_service.concluir(st.session_state, "planejamento", plano)
    workflow_service.concluir(st.session_state, "forecast", forecast)

    st.session_state["forecast_plano"] = plano

    artefatos.salvar_no_projeto(
        "FORECAST", f"Projeção de Resultados — {plano.campanha}", forecast,
        st.session_state, origem["id"],
    )
    st.toast("Projeção de Resultados salva no projeto.")
    st.rerun()


# ==========================================================
# RESULTADOS
# ==========================================================

if (

    "forecast" in st.session_state

):

    plano = st.session_state["forecast_plano"]

    forecast = st.session_state["forecast"]

    resumo = forecast_service.resumo(

        forecast

    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Impressões",

        numero_ptbr(resumo["impressoes"])

    )

    c2.metric(

        "Cliques",

        numero_ptbr(resumo["cliques"])

    )

    c3.metric(

        "Conversões",

        numero_ptbr(resumo["conversoes"])

    )

    c4.metric(

        "CPA Médio",

        moeda_ptbr(resumo["cpa"])

    )

    st.divider()

    st.dataframe(

        dataframe_ptbr(
            forecast_service.dataframe(forecast),
            moedas=["Verba", "CPM", "CPC", "CPA"],
            percentuais=["CTR"],
            inteiros=["Impressões", "Alcance", "Cliques", "Conversões"],
        ),

        hide_index=True,

        width="stretch"

    )

    st.divider()

    st.subheader(

        "Resumo"

    )

    a, b = st.columns(2)

    with a:

        st.metric(

            "CTR Médio",

            percentual_ptbr(resumo["ctr"])

        )

        st.metric(

            "CPM Médio",

            moeda_ptbr(resumo["cpm"])

        )

    with b:

        st.metric(

            "CPC Médio",

            moeda_ptbr(resumo["cpc"])

        )

        st.metric(

            "Investimento",

            moeda_ptbr(resumo["verba"])

        )
