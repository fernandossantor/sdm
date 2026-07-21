import pandas as pd
import streamlit as st

from application.services.budget_optimizer_service import (
    BudgetOptimizerService
)
from application.services.context_service import (
    ContextService
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Otimizador",

    page_icon="💰",

    layout="wide"

)

st.title("💰 Otimizador de Orçamento")

st.divider()

contexto_service = ContextService()

briefings = contexto_service.listar_briefings()

nomes = [

    b["nome"]

    for b in briefings

]

briefing = st.selectbox(

    "Briefing",

    nomes

)

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

    "Otimizar",

    type="primary",

    width="stretch"

)

# ==========================================================
# EXECUÇÃO
# ==========================================================

if executar:

    contexto, ranking = contexto_service.ranking(briefing)

    verba = contexto["briefing"]["orcamento"]

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

    resultado = BudgetOptimizerService().otimizar(

        ranking=ranking,

        verba_total=verba,

        minimo_ambiente=minimo_ambiente,

        maximo_ambiente=maximo_ambiente,

        percentual_teste=percentual_teste / 100

    )

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

        "Investimento",

        f'R$ {resumo["verba_total"]:,.2f}'

    )

    c3.metric(

        "Distribuído",

        f'R$ {resumo["verba_distribuida"]:,.2f}'

    )

    c4.metric(

        "Reserva",

        f'R$ {resumo["reserva_testes"]:,.2f}'

    )

    st.divider()

    df = pd.DataFrame(

        resultado["itens"]

    )

    st.dataframe(

        df,

        hide_index=True,

        width="stretch",

        column_config={

            "score":

                st.column_config.ProgressColumn(

                    "Score",

                    min_value=0,

                    max_value=100

                ),

            "percentual":

                st.column_config.NumberColumn(

                    "Percentual",

                    format="%.2f %%"

                ),

            "verba":

                st.column_config.NumberColumn(

                    "Verba",

                    format="R$ %.2f"

                )

        }

    )

    st.divider()

    st.subheader("Distribuição por Ambiente")

    ambiente = BudgetOptimizerService().ambiente(

        resultado

    )

    st.dataframe(

        pd.DataFrame(

            [

                {

                    "Ambiente": k,

                    "Verba": v

                }

                for k, v in ambiente.items()

            ]

        ),

        hide_index=True,

        width="stretch",

        column_config={

            "Verba":

                st.column_config.NumberColumn(

                    "Verba",

                    format="R$ %.2f"

                )

        }

    )

    st.subheader("Distribuição por Plataforma")

    plataforma = BudgetOptimizerService().plataforma(

        resultado

    )

    st.dataframe(

        pd.DataFrame(

            [

                {

                    "Plataforma": k,

                    "Verba": v

                }

                for k, v in plataforma.items()

            ]

        ),

        hide_index=True,

        width="stretch",

        column_config={

            "Verba":

                st.column_config.NumberColumn(

                    "Verba",

                    format="R$ %.2f"

                )

        }

    )

    if BudgetOptimizerService().validar(

        resultado

    ):

        st.success(

            "Plano otimizado com sucesso."

        )

    else:

        st.error(

            "A distribuição apresenta inconsistências."
        )
