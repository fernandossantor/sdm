import streamlit as st

from application.services.workflow_service import (
    WorkflowService
)

from components.home.hero import render as hero
from components.home.workflow_card import render as workflow_card
from components.home.projects_card import render as projects_card
from components.home.knowledge_card import render as knowledge_card

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="PMAH — Planejador de Mídia Automatizado e Híbrido",

    page_icon="📊",

    layout="wide",

    initial_sidebar_state="expanded"

)

def pagina_inicial():

    workflow = WorkflowService()

    estado = workflow.estado(

        st.session_state

    )

    hero()

    workflow_card(

        estado

    )

    st.divider()

    projects_card()

    st.divider()

    knowledge_card()


navegacao = st.navigation(

    {
        "PMAH": [
            st.Page(
                pagina_inicial,
                title="Início",
                icon="🏠",
                default=True,
            ),
        ],
        "Workflow oficial": [
            st.Page("pages/00_Briefing.py", title="Briefing", icon="📋"),
            st.Page("pages/03_MCP_Papeis.py", title="Papéis de mídia", icon="🧩"),
            st.Page("pages/05_Planejamento.py", title="Planejamento", icon="🧠"),
            st.Page("pages/09_Diagnostico.py", title="Diagnóstico", icon="🩺"),
            st.Page("pages/06_Forecast.py", title="Forecast", icon="📈"),
            st.Page("pages/07_Dashboard.py", title="Painel Executivo", icon="📊"),
            st.Page("pages/08_Exportacao.py", title="Relatórios", icon="📄"),
        ],
        "Análises avançadas": [
            st.Page("pages/10_Comparador.py", title="Comparador", icon="⚖️"),
            st.Page("pages/11_Cenarios.py", title="Cenários", icon="🎛️"),
            st.Page("pages/12_Otimizador.py", title="Otimizador", icon="🎯"),
            st.Page("pages/13_Insights.py", title="Insights", icon="💡"),
        ],
        "Base de conhecimento": [
            st.Page("pages/01_Catalogos.py", title="Catálogos", icon="🗂️"),
            st.Page("pages/04_Inventarios.py", title="Inventários", icon="📦"),
            st.Page("pages/15_Universos.py", title="Universos", icon="🌎"),
            st.Page("pages/16_Segmentos.py", title="Segmentos", icon="🧭"),
            st.Page("pages/14_Publicos.py", title="Públicos", icon="👥"),
        ],
    }

)

navegacao.run()
