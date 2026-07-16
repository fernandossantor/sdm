import pandas as pd
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

    page_title="Dashboard",

    page_icon="📊",

    layout="wide"

)

st.title("📊 Dashboard Executivo")

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

if st.button(

    "Atualizar Dashboard",

    type="primary",

    use_container_width=True

):

    plano = planejamento.gerar(

        briefing

    )

    forecast = forecast_engine.calcular(

        plano,

        repo.metricas()

    )

    st.session_state["dashboard_plano"] = plano

    st.session_state["dashboard_forecast"] = forecast


# ==========================================================
# DASHBOARD
# ==========================================================

if (

    "dashboard_plano" in st.session_state

    and

    "dashboard_forecast" in st.session_state

):

    plano = st.session_state["dashboard_plano"]

    forecast = st.session_state["dashboard_forecast"]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Inventários",

        len(plano.itens)

    )

    c2.metric(

        "Investimento",

        f"R$ {plano.verba_total:,.2f}"

    )

    c3.metric(

        "Conversões",

        int(

            sum(

                f.conversoes

                for f in forecast

            )

        )

    )

    c4.metric(

        "Cliques",

        int(

            sum(

                f.cliques

                for f in forecast

            )

        )

    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(

            "Distribuição da Verba"

        )

        df = pd.DataFrame(

            [

                {

                    "Inventário": i.inventario,

                    "Verba": i.verba

                }

                for i in plano.itens

            ]

        )

        st.bar_chart(

            df,

            x="Inventário",

            y="Verba"

        )

    with col2:

        st.subheader(

            "Distribuição por Papel"

        )

        df = pd.DataFrame(

            [

                {

                    "Papel": i.papel,

                    "Verba": i.verba

                }

                for i in plano.itens

            ]

        )

        st.bar_chart(

            df.groupby(

                "Papel",

                as_index=False

            ).sum(),

            x="Papel",

            y="Verba"

        )

    st.divider()

    st.subheader(

        "Forecast"

    )

    df = pd.DataFrame(

        [

            {

                "Inventário": f.inventario,

                "Impressões": f.impressoes,

                "Cliques": f.cliques,

                "Conversões": f.conversoes,

                "CPA": f.cpa

            }

            for f in forecast

        ]

    )

    st.dataframe(

        df,

        hide_index=True,

        use_container_width=True

    )

    st.divider()

    st.subheader(

        "Insights"

    )

    for insight in insights_service.gerar(

        plano,

        forecast

    ):

        st.info(

            insight

        )

    st.divider()

    st.subheader(

        "Plano Estratégico"

    )

    tabela = pd.DataFrame(

        [

            {

                "Inventário": i.inventario,

                "Plataforma": i.plataforma,

                "Ambiente": i.ambiente,

                "Papel": i.papel,

                "Score": i.score,

                "Percentual": i.percentual,

                "Verba": i.verba

            }

            for i in plano.itens

        ]

    )

    st.dataframe(

        tabela,

        hide_index=True,

        use_container_width=True,

        column_config={

            "Score":

                st.column_config.ProgressColumn(

                    "Score",

                    min_value=0,

                    max_value=100

                ),

            "Percentual":

                st.column_config.NumberColumn(

                    "Percentual",

                    format="%.2f %%"

                ),

            "Verba":

                st.column_config.NumberColumn(

                    "Verba",

                    format="R$ %.2f"

                )

        }

    )