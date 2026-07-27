import pandas as pd
import streamlit as st

from application.services.media_quality_service import MediaQualityService
from application.services.planejamento_service import PlanejamentoService
from application.services.workflow_artifact_service import WorkflowArtifactService
from components.artifact_manager import render as gerenciar_artefatos
from components.page_config import PAGE_ICON, titulo_pagina
from components.planning_selector import selecionar_planejamento
from components.workflow_guard import exigir


st.set_page_config(
    page_title=titulo_pagina("Qualidade e Localização"),
    page_icon=PAGE_ICON,
    layout="wide",
)
exigir("diagnostico")
st.title("🛡️ Qualidade programática e localização")
st.write(
    "Documente cada dimensão e sua proveniência. O PlanOS não combina esses "
    "dados em um índice opaco."
)

origem = selecionar_planejamento(
    PlanejamentoService(),
    key="qualidade_planejamento",
)
artefatos = WorkflowArtifactService()
gerenciar_artefatos(artefatos, "QUALIDADE_MIDIA", "Análises de qualidade")

inventarios = [item.inventario for item in origem["plano"].itens]
qualidade_base = pd.DataFrame([
    {
        "inventario": inventario,
        "viewability_percentual": None,
        "trafego_invalido_percentual": None,
        "fraude_percentual": None,
        "brand_safety": "NAO_AVALIADO",
        "brand_suitability": "NAO_AVALIADO",
        "fonte": "",
        "inicio": None,
        "fim": None,
        "observacoes": "",
    }
    for inventario in inventarios
])
localizacao_base = pd.DataFrame([
    {
        "inventario": inventario,
        "fonte_sinal": "",
        "precisao_metros": None,
        "raio_metros": None,
        "inicio": None,
        "fim": None,
        "finalidade": "",
        "base_legal": "",
        "metodo_associacao": "",
        "confianca_percentual": None,
        "natureza_visita": "",
    }
    for inventario in inventarios
])

st.subheader("Qualidade programática")
qualidade = st.data_editor(
    qualidade_base,
    num_rows="dynamic",
    width="stretch",
    key="grade_qualidade_programatica",
)
st.subheader("Localização")
st.caption(
    "Preencha somente quando localização fizer parte da segmentação ou medição."
)
localizacao = st.data_editor(
    localizacao_base,
    num_rows="dynamic",
    width="stretch",
    key="grade_localizacao",
)

if st.button("Avaliar documentação", type="primary"):
    try:
        st.session_state["resultado_qualidade_midia"] = (
            MediaQualityService().avaliar(
                qualidade.to_dict("records"),
                localizacao.to_dict("records"),
            )
        )
    except ValueError as erro:
        st.error(str(erro))

if "resultado_qualidade_midia" in st.session_state:
    resultado = st.session_state["resultado_qualidade_midia"]
    resumo = resultado["resumo"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Qualidade documentada", resumo["qualidade_documentada"])
    c2.metric("Qualidade incompleta", resumo["qualidade_incompleta"])
    c3.metric("Localização documentada", resumo["localizacao_documentada"])
    c4.metric("Localização incompleta", resumo["localizacao_incompleta"])
    st.info(resultado["metodologia"])
    st.dataframe(resultado["qualidade"], hide_index=True, width="stretch")
    st.dataframe(resultado["localizacao"], hide_index=True, width="stretch")
    for limitacao in resultado["limitacoes"]:
        st.caption(f"• {limitacao}")
    if st.button("Salvar análise de qualidade"):
        artefatos.salvar_no_projeto(
            "QUALIDADE_MIDIA",
            f"Qualidade e localização — {origem['plano'].campanha}",
            resultado,
            st.session_state,
            origem["id"],
        )
        st.success("Análise salva no projeto.")
