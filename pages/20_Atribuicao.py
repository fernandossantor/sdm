import pandas as pd
import streamlit as st

from application.services.attribution_service import AttributionService
from application.services.planejamento_service import PlanejamentoService
from application.services.workflow_artifact_service import WorkflowArtifactService
from components.artifact_manager import render as gerenciar_artefatos
from components.page_config import PAGE_ICON, titulo_pagina
from components.planning_selector import selecionar_planejamento
from components.workflow_guard import exigir


st.set_page_config(
    page_title=titulo_pagina("Atribuição"),
    page_icon=PAGE_ICON,
    layout="wide",
)
exigir("diagnostico")
st.title("🔗 Atribuição")
st.write(
    "Distribua o crédito de conversões entre pontos de contato observados. "
    "Atribuição não demonstra incrementalidade."
)

origem = selecionar_planejamento(
    PlanejamentoService(),
    key="atribuicao_planejamento",
)
artefatos = WorkflowArtifactService()
gerenciar_artefatos(artefatos, "ATRIBUICAO", "Análises de atribuição")

c1, c2 = st.columns(2)
modelo = c1.selectbox(
    "Modelo",
    ["LINEAR", "PRIMEIRO_TOQUE", "ULTIMO_TOQUE", "POSICIONAL"],
    format_func=lambda valor: valor.replace("_", " ").title(),
)
janela = c2.number_input(
    "Janela de atribuição (dias)",
    min_value=1,
    value=30,
)
st.caption(
    "Cada linha representa um toque ligado a uma conversão. Repita o ID, "
    "a data da conversão e a receita quando houver mais de um toque."
)
eventos = st.data_editor(
    pd.DataFrame(columns=[
        "conversao_id",
        "instante_conversao",
        "receita",
        "canal",
        "instante_toque",
    ]),
    num_rows="dynamic",
    width="stretch",
    key="eventos_atribuicao",
)

if st.button("Calcular atribuição", type="primary"):
    try:
        st.session_state["resultado_atribuicao"] = AttributionService().calcular(
            eventos.to_dict("records"),
            modelo,
            janela,
        )
    except ValueError as erro:
        st.error(str(erro))

if "resultado_atribuicao" in st.session_state:
    resultado = st.session_state["resultado_atribuicao"]
    m1, m2, m3 = st.columns(3)
    m1.metric("Conversões elegíveis", resultado["conversoes_elegiveis"])
    m2.metric("Diretas", resultado["conversoes_diretas"])
    m3.metric("Assistidas", resultado["conversoes_assistidas"])
    if resultado["todos_creditos_reconciliados"]:
        st.success("O crédito fecha em 100% para cada conversão elegível.")
    else:
        st.error("Há conversões cujo crédito não fecha em 100%.")
    st.subheader("Crédito por canal")
    st.dataframe(resultado["por_canal"], hide_index=True, width="stretch")
    st.subheader("Trilha auditável por conversão")
    st.dataframe(resultado["creditos"], hide_index=True, width="stretch")
    if resultado["conversoes_excluidas"]:
        st.warning("Há conversões excluídas por falta de dados elegíveis.")
        st.dataframe(
            resultado["conversoes_excluidas"],
            hide_index=True,
            width="stretch",
        )
    for limitacao in resultado["limitacoes"]:
        st.caption(f"• {limitacao}")
    if st.button("Salvar análise de atribuição"):
        artefatos.salvar_no_projeto(
            "ATRIBUICAO",
            f"Atribuição — {origem['plano'].campanha}",
            resultado,
            st.session_state,
            origem["id"],
        )
        st.success("Análise de atribuição salva no projeto.")
