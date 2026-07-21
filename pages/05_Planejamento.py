import pandas as pd
import streamlit as st

from application.services.briefing_service import (
    BriefingService
)

from application.services.planejamento_service import (
    PlanejamentoService
)

from application.services.context_service import (
    ContextService
)
from application.services.workflow_service import WorkflowService


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Planejamento",

    page_icon="📋",

    layout="wide"

)

st.title("📋 Planejamento Estratégico")

st.divider()

contexto_service = ContextService()

planejamento = PlanejamentoService()

briefing_service = BriefingService()

workflow_service = WorkflowService()


# ==========================================================
# ESCOLHA DO BRIEFING
# ==========================================================

tem_sessao = briefing_service.existe(

    st.session_state

)

briefings_salvos = contexto_service.listar_briefings()

opcoes = []

if tem_sessao:

    opcoes.append(

        "Briefing da Sessão"

    )

if briefings_salvos:

    opcoes.append(

        "Briefing Salvo"

    )

if not opcoes:

    st.warning(

        "Nenhum briefing disponível."

    )

    st.stop()

modo = st.radio(

    "Origem do Briefing",

    opcoes,

    horizontal=True

)


# ==========================================================
# BRIEFING DA SESSÃO
# ==========================================================

if modo == "Briefing da Sessão":

    briefing = briefing_service.recuperar(

        st.session_state

    )

    st.success(

        "Utilizando Briefing da Sessão."

    )

    st.info(

        f"""
**Cliente:** {briefing.cliente}

**Campanha:** {briefing.campanha}

**Objetivo:** {briefing.objetivo}

**KPI:** {briefing.kpi}

**Orçamento:** R$ {briefing.orcamento:,.2f}
"""
    )


# ==========================================================
# BRIEFING SALVO
# ==========================================================

else:

    nomes = [

        b["nome"]

        for b in briefings_salvos

    ]

    nome_briefing = st.selectbox(

        "Briefing",

        nomes

    )

    st.success(

        "Utilizando Briefing salvo."

    )


st.divider()

gerar = st.button(

    "Gerar Plano",

    type="primary",

    width="stretch"

)


# ==========================================================
# GERAÇÃO
# ==========================================================

if gerar:

    with st.spinner(

        "Gerando plano..."

    ):

        if modo == "Briefing da Sessão":

            plano = planejamento.gerar(

                briefing=briefing

            )

        else:

            plano = planejamento.gerar(

                nome_briefing=nome_briefing

            )

    if modo == "Briefing Salvo":
        workflow_service.registrar_briefing(st.session_state, nome_briefing)

    workflow_service.concluir(st.session_state, "planejamento", plano)


# ==========================================================
# EXIBIÇÃO
# ==========================================================

if "plano" in st.session_state:

    plano = st.session_state["plano"]

    abas = st.tabs(

        [

            "🎯 Estratégia",

            "📊 Resumo",

            "💬 Justificativas"

        ]

    )

    with abas[0]:

        df = pd.DataFrame(

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

            df,

            hide_index=True,

            width="stretch"

        )

    with abas[1]:

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(

            "Inventários",

            len(plano.itens)

        )

        c2.metric(

            "Principais",

            plano.principal

        )

        c3.metric(

            "Complementares",

            plano.complementar

        )

        c4.metric(

            "Verba",

            f"R$ {plano.verba_total:,.2f}"

        )

        st.divider()

        st.write(

            f"**Cliente:** {plano.cliente}"

        )

        st.write(

            f"**Campanha:** {plano.campanha}"

        )

        st.write(

            f"**Objetivo:** {plano.objetivo}"

        )

    with abas[2]:

        for item in plano.itens:

            with st.expander(

                item.inventario

            ):

                for texto in item.justificativas:

                    st.markdown(

                        f"- {texto}"

                    )
