import pandas as pd
import streamlit as st

from application.services.scenario_service import (
    ScenarioService
)
from application.services.context_service import (
    ContextService
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Cenários",

    page_icon="🎭",

    layout="wide"

)

st.title("🎭 Simulação de Cenários")

st.divider()

contexto_service = ContextService()

service = ScenarioService()

briefings = contexto_service.listar_briefings()

nomes = [

    b["nome"]

    for b in briefings

]

col1, col2 = st.columns(

    [3, 1]

)

with col1:

    briefing = st.selectbox(

        "Briefing",

        nomes

    )

with col2:

    st.write("")

    st.write("")

    gerar = st.button(

        "Simular",

        type="primary",

        width="stretch"

    )

# ==========================================================
# GERAÇÃO
# ==========================================================

if gerar:

    cenarios = service.gerar_todos(

        briefing

    )

    st.session_state["cenarios"] = cenarios

# ==========================================================
# RESULTADOS
# ==========================================================

if "cenarios" in st.session_state:

    cenarios = st.session_state["cenarios"]

    resumo = []

    for nome, plano in cenarios.items():

        resumo.append(

            {

                "Cenário": nome,

                "Inventários": len(

                    plano.itens

                ),

                "Principais": plano.principal,

                "Complementares": plano.complementar,

                "Score Médio": round(

                    sum(

                        i.score

                        for i in plano.itens

                    )

                    /

                    len(plano.itens),

                    2

                ),

                "Investimento": plano.verba_total

            }

        )

    st.subheader(

        "Resumo dos Cenários"

    )

    st.dataframe(

        pd.DataFrame(

            resumo

        ),

        hide_index=True,

        width="stretch",

        column_config={

            "Investimento":

                st.column_config.NumberColumn(

                    "Investimento",

                    format="R$ %.2f"

                )

        }

    )

    st.divider()

    abas = st.tabs(

        list(

            cenarios.keys()

        )

    )

    for aba, nome in zip(

        abas,

        cenarios.keys()

    ):

        with aba:

            plano = cenarios[nome]

            linhas = []

            for item in plano.itens:

                linhas.append(

                    {

                        "Inventário": item.inventario,

                        "Plataforma": item.plataforma,

                        "Ambiente": item.ambiente,

                        "Papel": item.papel,

                        "Score": item.score,

                        "Percentual": item.percentual,

                        "Verba": item.verba

                    }

                )

            st.dataframe(

                pd.DataFrame(

                    linhas

                ),

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

            st.caption(

                f"{plano.principal} canais principais • "

                f"{plano.complementar} complementares • "

                f"Verba total: R$ {plano.verba_total:,.2f}"

            )
