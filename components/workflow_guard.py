import streamlit as st

from application.services.workflow_service import WorkflowService


ANTERIORES = {
    "mcp_papeis": ("Briefing", "pages/00_Briefing.py", "📋"),
    "planejamento": ("Papéis dos Meios", "pages/03_MCP_Papeis.py", "🧩"),
    "diagnostico": ("Plano de Mídia", "pages/05_Planejamento.py", "🧠"),
    "forecast": ("Diagnóstico", "pages/09_Diagnostico.py", "🩺"),
    "dashboard": ("Projeção de Resultados", "pages/06_Forecast.py", "📈"),
    "exportacao": ("Painel de Resultados", "pages/07_Dashboard.py", "📊"),
}


def exigir(etapa):

    workflow = WorkflowService()
    if workflow.pode_acessar(st.session_state, etapa):
        return

    nome, pagina, icone = ANTERIORES[etapa]
    st.warning(
        f"Selecione ou conclua {nome} para acessar esta parte do workflow. "
        "Se o registro já existe, escolha-o no contexto ativo da barra lateral."
    )
    st.page_link(
        pagina,
        label=f"Voltar para {nome}",
        icon=icone,
        width="stretch",
    )
    st.stop()
