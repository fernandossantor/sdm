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


pagina_home = st.Page(pagina_inicial, title="Início", icon="🏠", default=True)
workflow_links = [
    (st.Page("pages/00_Briefing.py", title="Briefing", icon="📋"), "Briefing", "📋"),
    (st.Page("pages/03_MCP_Papeis.py", title="Papéis de mídia", icon="🧩"), "Papéis de mídia", "🧩"),
    (st.Page("pages/05_Planejamento.py", title="Planejamento", icon="🧠"), "Planejamento", "🧠"),
    (st.Page("pages/09_Diagnostico.py", title="Diagnóstico", icon="🩺"), "Diagnóstico", "🩺"),
    (st.Page("pages/06_Forecast.py", title="Forecast", icon="📈"), "Forecast", "📈"),
    (st.Page("pages/07_Dashboard.py", title="Painel Executivo", icon="📊"), "Painel Executivo", "📊"),
    (st.Page("pages/08_Exportacao.py", title="Relatórios", icon="📄"), "Relatórios", "📄"),
]
analise_links = [
    (st.Page("pages/10_Comparador.py", title="Comparador", icon="⚖️"), "Comparador", "⚖️"),
    (st.Page("pages/11_Cenarios.py", title="Cenários", icon="🎛️"), "Cenários", "🎛️"),
    (st.Page("pages/12_Otimizador.py", title="Otimizador", icon="🎯"), "Otimizador", "🎯"),
    (st.Page("pages/13_Insights.py", title="Insights", icon="💡"), "Insights", "💡"),
]
base_links = [
    (st.Page("pages/01_Catalogos.py", title="Catálogos", icon="🗂️"), "Catálogos", "🗂️"),
    (st.Page("pages/04_Inventarios.py", title="Inventários", icon="📦"), "Inventários", "📦"),
    (st.Page("pages/15_Universos.py", title="Universos", icon="🌎"), "Universos", "🌎"),
    (st.Page("pages/16_Segmentos.py", title="Segmentos", icon="🧭"), "Segmentos", "🧭"),
    (st.Page("pages/14_Publicos.py", title="Públicos", icon="👥"), "Públicos", "👥"),
]
navegacao = st.navigation(
    [
        pagina_home,
        *[item[0] for item in workflow_links],
        *[item[0] for item in analise_links],
        *[item[0] for item in base_links],
    ],
    position="hidden",
)

with st.sidebar:
    st.markdown("## PMAH — Planejador de Mídia Automatizado e Híbrido")
    if st.session_state.get("projeto_nome"):
        st.caption(f"Projeto ativo: {st.session_state['projeto_nome']}")
    st.page_link(pagina_home, label="Início", icon="🏠")
    st.caption("WORKFLOW OFICIAL")
    for pagina, titulo, icone in workflow_links:
        st.page_link(pagina, label=titulo, icon=icone)
    st.caption("ANÁLISES AVANÇADAS")
    for pagina, titulo, icone in analise_links:
        st.page_link(pagina, label=titulo, icon=icone)
    st.caption("BASE DE CONHECIMENTO")
    for pagina, titulo, icone in base_links:
        st.page_link(pagina, label=titulo, icon=icone)
    st.divider()
    st.caption(
        "Desenvolvido por Fernando Silva Santor, professor de Planejamento "
        "de Mídia do Curso de Publicidade e Propaganda da Universidade "
        "Federal do Pampa, campus São Borja, RS. Contato: "
        "fernandosantor@unipampa.edu.br"
    )
    st.caption("Versão 1.2.0")
    st.caption("Tecnologias: Supabase · Streamlit · Codex · GitHub Codespaces")

navegacao.run()
