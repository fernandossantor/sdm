import streamlit as st

from application.services.planejamento_service import (
    PlanejamentoService
)

from application.services.forecast_service import (
    ForecastService
)

from infrastructure.repositories.decision_repository import (
    DecisionRepository
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Forecast",

    page_icon="📈",

    layout="wide"

)

st.title("📈 Forecast")

st.divider()

repo = DecisionRepository()

planejamento = PlanejamentoService()

forecast_service = ForecastService()

briefings = repo.listar_briefings()

nomes = [

    b["nome"]

    for b in briefings

]

briefing = st.selectbox(

    "Briefing",

    nomes

)

if st.button(

    "Gerar Forecast",

    type="primary",

    use_container_width=True

):

    plano = planejamento.gerar(

        briefing

    )

    forecast = forecast_service.gerar(

        plano,

        repo.metricas()

    )

    st.session_state["forecast_plano"] = plano

    st.session_state["forecast"] = forecast


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

        f"{resumo['impressoes']:,}"

    )

    c2.metric(

        "Cliques",

        f"{resumo['cliques']:,}"

    )

    c3.metric(

        "Conversões",

        f"{resumo['conversoes']:,}"

    )

    c4.metric(

        "CPA Médio",

        f"R$ {resumo['cpa']:.2f}"

    )

    st.divider()

    st.dataframe(

        forecast_service.dataframe(

            forecast

        ),

        hide_index=True,

        use_container_width=True

    )

    st.divider()

    st.subheader(

        "Resumo"

    )

    a, b = st.columns(2)

    with a:

        st.metric(

            "CTR Médio",

            f"{resumo['ctr']:.2f}%"

        )

        st.metric(

            "CPM Médio",

            f"R$ {resumo['cpm']:.2f}"

        )

    with b:

        st.metric(

            "CPC Médio",

            f"R$ {resumo['cpc']:.2f}"

        )

        st.metric(

            "Investimento",

            f"R$ {resumo['verba']:,.2f}"

        )