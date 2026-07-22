import streamlit as st

from application.services.comparador_service import (
    ComparadorService
)

from application.services.forecast_service import (
    ForecastService
)

from application.services.planejamento_service import (
    PlanejamentoService
)

from application.services.context_service import (
    ContextService
)
from components.planning_selector import selecionar_planejamento
from components.formatters import moeda_ptbr, numero_ptbr


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Comparação de Planos",

    page_icon="⚖️",

    layout="wide"

)

st.title("⚖️ Comparação de Planos")

st.divider()

contexto_service = ContextService()

planejamento = PlanejamentoService()

forecast_service = ForecastService()

comparador = ComparadorService()

col1, col2 = st.columns(2)

with col1:

    origem1 = selecionar_planejamento(planejamento, "plano_a")

with col2:

    origem2 = selecionar_planejamento(planejamento, "plano_b")

if st.button(

    "Comparar",

    type="primary",

    width="stretch"

):

    plano1 = origem1["plano"]
    plano2 = origem2["plano"]

    forecast1 = forecast_service.gerar(

        plano1,

        contexto_service.metricas()

    )

    forecast2 = forecast_service.gerar(

        plano2,

        contexto_service.metricas()

    )

    resultado = comparador.comparar(

        plano1,

        forecast1.itens,

        plano2,

        forecast2.itens

    )

    st.session_state["resultado"] = resultado


# ==========================================================
# RESULTADOS
# ==========================================================

if "resultado" in st.session_state:

    r = st.session_state["resultado"]

    st.success(

        f"Plano vencedor: {r.vencedor}"

    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Score Plano A",

            numero_ptbr(r.score_plano_1, 2)

        )

        st.metric(

            "Conversões Plano A",

            f"{r.conversoes_plano_1:.0f}"

        )

        st.metric(

            "Investimento Plano A",

            moeda_ptbr(r.investimento_plano_1)

        )

    with c2:

        st.metric(

            "Score Plano B",

            numero_ptbr(r.score_plano_2, 2)

        )

        st.metric(

            "Conversões Plano B",

            f"{r.conversoes_plano_2:.0f}"

        )

        st.metric(

            "Investimento Plano B",

            moeda_ptbr(r.investimento_plano_2)

        )

    with c3:

        st.metric(

            "Δ Score",

            numero_ptbr(r.diferenca_score, 2)

        )

        st.metric(

            "Δ Conversões",

            f"{r.diferenca_conversoes:.0f}"

        )

        st.metric(

            "Δ Investimento",

            moeda_ptbr(r.diferenca_investimento)

        )

    st.divider()

    st.subheader(

        "Justificativa"

    )

    st.info(

        r.justificativa

    )
