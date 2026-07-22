import pandas as pd
import streamlit as st

from application.services.planejamento_service import (
    PlanejamentoService
)

from application.services.insights_service import (
    InsightsService
)
from application.services.context_service import ContextService
from application.services.forecast_service import (
    ForecastService
)
from application.services.workflow_service import WorkflowService
from components.workflow_guard import exigir
from components.planning_selector import selecionar_planejamento


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Dashboard",

    page_icon="📊",

    layout="wide"

)

exigir("dashboard")

st.title("📊 Dashboard Executivo")

st.divider()

contexto_service = ContextService()

planejamento = PlanejamentoService()

forecast_service = ForecastService()

insights_service = InsightsService()

workflow_service = WorkflowService()

origem = selecionar_planejamento(planejamento, "dashboard_planejamento")

if st.button(

    "Atualizar Dashboard",

    type="primary",

    width="stretch"

):

    plano = origem["plano"]

    forecast = forecast_service.gerar_itens(plano)

    st.session_state["dashboard_plano"] = plano

    st.session_state["dashboard_forecast"] = forecast

    workflow_service.concluir(st.session_state, "planejamento", plano)
    workflow_service.concluir(st.session_state, "forecast", forecast)
    workflow_service.concluir(
        st.session_state,
        "dashboard",
        {"plano": plano, "forecast": forecast},
    )


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

        width="stretch"

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

        width="stretch",

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
