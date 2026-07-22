import streamlit as st
from components.page_config import PAGE_ICON
from components.formatters import numero_ptbr

from application.services.diagnostico_service import (
    DiagnosticoService
)

from application.services.planejamento_service import (
    PlanejamentoService
)

from application.services.workflow_service import WorkflowService
from components.workflow_guard import exigir
from components.planning_selector import selecionar_planejamento
from application.services.workflow_artifact_service import WorkflowArtifactService
from components.artifact_manager import render as gerenciar_artefatos


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Diagnóstico do Plano",

    page_icon=PAGE_ICON,

    layout="wide"

)

exigir("diagnostico")

st.title("🩺 Diagnóstico do Plano")

st.divider()

planejamento = PlanejamentoService()

diagnostico_service = DiagnosticoService()

workflow_service = WorkflowService()
artefatos = WorkflowArtifactService()

origem = selecionar_planejamento(planejamento, "diagnostico_planejamento")
gerenciar_artefatos(artefatos, "DIAGNOSTICO", "Diagnósticos")

if st.button(

    "Gerar Diagnóstico",

    type="primary",

    width="stretch"

):

    plano = origem["plano"]

    diagnostico = diagnostico_service.gerar(

        plano

    )

    workflow_service.concluir(st.session_state, "planejamento", plano)
    workflow_service.concluir(st.session_state, "diagnostico", diagnostico)


# ==========================================================
# RESULTADO
# ==========================================================

if "diagnostico" in st.session_state:

    diagnostico = st.session_state["diagnostico"]

    with st.expander("Salvar diagnóstico", expanded=False):
        nome_diagnostico = st.text_input(
            "Nome do diagnóstico",
            value=f"Diagnóstico — {diagnostico.campanha}",
        )
        if st.button("Salvar diagnóstico", type="primary"):
            artefatos.salvar_no_projeto(
                "DIAGNOSTICO",
                nome_diagnostico,
                diagnostico,
                st.session_state,
                origem["id"],
            )
            st.success("Diagnóstico salvo.")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Score médio (%)",

        numero_ptbr(diagnostico.score_medio, 2)

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

                    "Score (%)",

                    numero_ptbr(item.score, 2)

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
