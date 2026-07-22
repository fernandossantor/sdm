import streamlit as st

from application.services.workflow_service import WorkflowService


ANTERIORES = {
    "planejamento": ("Briefing", "pages/00_Briefing.py", "📋"),
    "diagnostico": ("Planejamento", "pages/05_Planejamento.py", "🧠"),
    "forecast": ("Diagnóstico", "pages/09_Diagnostico.py", "🩺"),
    "dashboard": ("Forecast", "pages/06_Forecast.py", "📈"),
    "exportacao": ("Painel Executivo", "pages/07_Dashboard.py", "📊"),
}


def exigir(etapa):

    workflow = WorkflowService()
    if workflow.pode_acessar(st.session_state, etapa):
        return

    nome, pagina, icone = ANTERIORES[etapa]
    st.warning(
        f"Conclua a etapa {nome} antes de acessar esta parte do workflow."
    )
    st.page_link(
        pagina,
        label=f"Voltar para {nome}",
        icon=icone,
        width="stretch",
    )
    st.stop()
