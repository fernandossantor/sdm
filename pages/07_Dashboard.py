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
from components.formatters import moeda_ptbr, numero_ptbr
from application.services.workflow_artifact_service import WorkflowArtifactService
from components.artifact_manager import render as gerenciar_artefatos


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Painel de Resultados",

    page_icon="📊",

    layout="wide"

)

exigir("dashboard")

st.title("📊 Painel de Resultados")

st.divider()

contexto_service = ContextService()

planejamento = PlanejamentoService()

forecast_service = ForecastService()

insights_service = InsightsService()

workflow_service = WorkflowService()
artefatos = WorkflowArtifactService()

origem = selecionar_planejamento(planejamento, "dashboard_planejamento")
gerenciar_artefatos(artefatos, "DASHBOARD", "Painéis executivos")

if st.button(

    "Atualizar Painel de Resultados",

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
    artefatos.salvar_no_projeto(
        "DASHBOARD",
        f"Painel Executivo — {plano.campanha}",
        {"plano": plano, "forecast": forecast},
        st.session_state,
        origem["id"],
    )
    st.toast("Painel Executivo salvo no projeto.")
    st.rerun()


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

        moeda_ptbr(plano.verba_total)

    )

    c3.metric(

        "Conversões",

        numero_ptbr(int(

            sum(

                f.conversoes

                for f in forecast

            )

        ))

    )

    c4.metric(

        "Cliques",

        numero_ptbr(int(

            sum(

                f.cliques

                for f in forecast

            )

        ))

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

        "Projeção de Resultados"

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
