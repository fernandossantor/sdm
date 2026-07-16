import streamlit as st

from application.services.diagnostico_service import (
    DiagnosticoService
)

from application.services.planejamento_service import (
    PlanejamentoService
)

from infrastructure.repositories.decision_repository import (
    DecisionRepository)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Diagnóstico",

    page_icon="🩺",

    layout="wide"

)

st.title("🩺 Diagnóstico Estratégico")

st.divider()

repo = DecisionRepository()

planejamento = PlanejamentoService()

diagnostico_service = DiagnosticoService()

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

    "Gerar Diagnóstico",

    type="primary",

    use_container_width=True

):

    plano = planejamento.gerar(

        briefing

    )

    diagnostico = diagnostico_service.gerar(

        plano

    )

    st.session_state["diagnostico"] = diagnostico


# ==========================================================
# RESULTADO
# ==========================================================

if "diagnostico" in st.session_state:

    diagnostico = st.session_state["diagnostico"]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Score Médio",

        diagnostico.score_medio

    )

    c2.metric(

        "Principais",

        diagnostico.principais

    )

    c3.metric(

        "Complementares",

        diagnostico.complementares

    )

    c4.metric(

        "Recomendações",

        diagnostico.total_recomendacoes

    )

    st.divider()

    abas = st.tabs(

        [

            "Inventários",

            "Observações"

        ]

    )

    # ======================================================
    # INVENTÁRIOS
    # ======================================================

    with abas[0]:

        for item in diagnostico.itens:

            with st.expander(

                item.inventario,

                expanded=False

            ):

                a, b, c = st.columns(3)

                a.metric(

                    "Score",

                    item.score

                )

                b.metric(

                    "Papel",

                    item.papel

                )

                c.metric(

                    "Ambiente",

                    item.ambiente

                )

                st.markdown(

                    "**Pontos Fortes**"

                )

                if item.pontos_fortes:

                    for texto in item.pontos_fortes:

                        st.success(

                            texto

                        )

                else:

                    st.caption(

                        "Nenhum."

                    )

                st.markdown(

                    "**Pontos de Atenção**"

                )

                if item.pontos_fracos:

                    for texto in item.pontos_fracos:

                        st.warning(

                            texto

                        )

                else:

                    st.caption(

                        "Nenhum."

                    )

                st.markdown(

                    "**Recomendações**"

                )

                if item.recomendacoes:

                    for texto in item.recomendacoes:

                        st.info(

                            texto

                        )

                else:

                    st.caption(

                        "Nenhuma."

                    )

    # ======================================================
    # OBSERVAÇÕES
    # ======================================================

    with abas[1]:

        for obs in diagnostico.observacoes:

            st.info(

                obs

            )