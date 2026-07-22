import pandas as pd
import streamlit as st
from components.page_config import PAGE_ICON, titulo_pagina
from components.formatters import moeda_ptbr, numero_ptbr, percentual_ptbr

from application.services.scenario_service import (
    ScenarioService
)
from application.services.context_service import (
    ContextService
)
from application.services.planejamento_service import PlanejamentoService
from components.planning_selector import selecionar_planejamento


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title=titulo_pagina("Cenários"),

    page_icon=PAGE_ICON,

    layout="wide"

)

st.title("🎭 Simulação de Cenários")

st.divider()

contexto_service = ContextService()

service = ScenarioService()
planejamento = PlanejamentoService()

col1, col2 = st.columns(

    [3, 1]

)

with col1:

    origem = selecionar_planejamento(planejamento, "cenarios_planejamento")

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

    cenarios = service.gerar_todos_de_plano(origem["plano"])

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

                "Score médio": numero_ptbr(round(

                    sum(

                        i.score

                        for i in plano.itens

                    )

                    /

                    len(plano.itens),

                    2

                ), 2) if plano.itens else numero_ptbr(0, 2),

                "Investimento": moeda_ptbr(plano.verba_total)

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

                        "Score": numero_ptbr(item.score, 2),

                        "Percentual": percentual_ptbr(item.percentual),

                        "Verba": moeda_ptbr(item.verba)

                    }

                )

            st.dataframe(

                pd.DataFrame(

                    linhas

                ),

                hide_index=True,

                width="stretch",

            )

            st.caption(

                f"{plano.principal} canais principais • "

                f"{plano.complementar} complementares • "

                f"Verba total: {moeda_ptbr(plano.verba_total)}"

            )
