import streamlit as st

from application.services.planejamento_service import (
    PlanejamentoService
)

from application.services.insights_service import (
    InsightsService
)

from engine.forecast_engine import (
    ForecastEngine
)

from infrastructure.repositories.decision_repository import (
    DecisionRepository
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Insights",

    page_icon="💡",

    layout="wide"

)

st.title("💡 Insights Estratégicos")

st.divider()

repo = DecisionRepository()

planejamento = PlanejamentoService()

forecast_engine = ForecastEngine()

insights_service = InsightsService()

briefings = repo.listar_briefings()

nomes = [

    b["nome"]

    for b in briefings

]

briefing = st.selectbox(

    "Briefing",

    nomes

)

executar = st.button(

    "Gerar Insights",

    type="primary",

    use_container_width=True

)

# ==========================================================
# PROCESSAMENTO
# ==========================================================

if executar:

    plano = planejamento.gerar(

        briefing

    )

    forecast = forecast_engine.calcular(

        plano,

        repo.metricas()

    )

    st.session_state["plano"] = plano

    st.session_state["forecast"] = forecast

# ==========================================================
# RESULTADOS
# ==========================================================

if (

    "plano" in st.session_state

    and

    "forecast" in st.session_state

):

    plano = st.session_state["plano"]

    forecast = st.session_state["forecast"]

    relatorio = insights_service.relatorio(

        plano,

        forecast

    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Cliente",

        plano.cliente

    )

    c2.metric(

        "Campanha",

        plano.campanha

    )

    c3.metric(

        "Inventários",

        len(plano.itens)

    )

    c4.metric(

        "Investimento",

        f"R$ {plano.verba_total:,.2f}"

    )

    st.divider()

    st.subheader(

        "Resumo Executivo"

    )

    for insight in insights_service.resumo(

        plano,

        forecast

    ):

        st.success(

            insight

        )

    st.divider()

    st.subheader(

        "Insights Estratégicos"

    )

    for insight in relatorio["insights"]:

        st.markdown(

            f"- {insight}"

        )

    st.divider()

    st.subheader(

        "Relatório"

    )

    st.text(

        insights_service.texto(

            plano,

            forecast

        )

    )