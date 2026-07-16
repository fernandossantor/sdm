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

from infrastructure.repositories.decision_repository import (
    DecisionRepository
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Comparador",

    page_icon="⚖️",

    layout="wide"

)

st.title("⚖️ Comparador de Planos")

st.divider()

repo = DecisionRepository()

planejamento = PlanejamentoService()

forecast_service = ForecastService()

comparador = ComparadorService()

briefings = repo.listar_briefings()

nomes = [

    b["nome"]

    for b in briefings

]

col1, col2 = st.columns(2)

with col1:

    briefing1 = st.selectbox(

        "Plano A",

        nomes,

        key="plano_a"

    )

with col2:

    briefing2 = st.selectbox(

        "Plano B",

        nomes,

        index=1 if len(nomes) > 1 else 0,

        key="plano_b"

    )

if st.button(

    "Comparar",

    type="primary",

    use_container_width=True

):

    plano1 = planejamento.gerar(

        briefing1

    )

    plano2 = planejamento.gerar(

        briefing2

    )

    forecast1 = forecast_service.gerar(

        plano1,

        repo.metricas()

    )

    forecast2 = forecast_service.gerar(

        plano2,

        repo.metricas()

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

            f"{r.score_plano_1:.2f}"

        )

        st.metric(

            "Conversões Plano A",

            f"{r.conversoes_plano_1:.0f}"

        )

        st.metric(

            "Investimento Plano A",

            f"R$ {r.investimento_plano_1:,.2f}"

        )

    with c2:

        st.metric(

            "Score Plano B",

            f"{r.score_plano_2:.2f}"

        )

        st.metric(

            "Conversões Plano B",

            f"{r.conversoes_plano_2:.0f}"

        )

        st.metric(

            "Investimento Plano B",

            f"R$ {r.investimento_plano_2:,.2f}"

        )

    with c3:

        st.metric(

            "Δ Score",

            f"{r.diferenca_score:.2f}"

        )

        st.metric(

            "Δ Conversões",

            f"{r.diferenca_conversoes:.0f}"

        )

        st.metric(

            "Δ Investimento",

            f"R$ {r.diferenca_investimento:,.2f}"

        )

    st.divider()

    st.subheader(

        "Justificativa"

    )

    st.info(

        r.justificativa

    )