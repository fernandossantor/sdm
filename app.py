import streamlit as st

from application.services.workflow_service import (
    WorkflowService
)

from components.home.hero import render as hero
from components.home.workflow_card import render as workflow_card
from components.home.projects_card import render as projects_card
from components.home.knowledge_card import render as knowledge_card
from components.active_context import render as active_context
from components.page_config import PAGE_ICON


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="PlanOS — Plataforma Inteligente de Planejamento Híbrido de Mídia",

    page_icon=PAGE_ICON,

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
pagina_guia = st.Page("pages/02_Guia.py", title="Guia de Uso", icon="📖")
workflow_links = [
    (st.Page("pages/00_Briefing.py", title="Briefing de Mídia", icon="📋"), "Briefing de Mídia", "📋"),
    (st.Page("pages/03_MCP_Papeis.py", title="Papéis dos Meios", icon="🧩"), "Papéis dos Meios", "🧩"),
    (st.Page("pages/05_Planejamento.py", title="Plano de Mídia", icon="🧠"), "Plano de Mídia", "🧠"),
    (st.Page("pages/17_Cronograma.py", title="Cronograma de Inserções", icon="🗓️"), "Cronograma de Inserções", "🗓️"),
    (st.Page("pages/09_Diagnostico.py", title="Diagnóstico do Plano", icon="🩺"), "Diagnóstico do Plano", "🩺"),
    (st.Page("pages/06_Forecast.py", title="Projeção de Resultados", icon="📈"), "Projeção de Resultados", "📈"),
    (st.Page("pages/07_Dashboard.py", title="Painel de Resultados", icon="📊"), "Painel de Resultados", "📊"),
    (st.Page("pages/08_Exportacao.py", title="Relatório de Mídia", icon="📄"), "Relatório de Mídia", "📄"),
]
analise_links = [
    (st.Page("pages/10_Comparador.py", title="Comparação de Planos", icon="⚖️"), "Comparação de Planos", "⚖️"),
    (st.Page("pages/11_Cenarios.py", title="Simulação de Cenários", icon="🎛️"), "Simulação de Cenários", "🎛️"),
    (st.Page("pages/12_Otimizador.py", title="Otimização de Verba", icon="🎯"), "Otimização de Verba", "🎯"),
    (st.Page("pages/13_Insights.py", title="Insights de Mídia", icon="💡"), "Insights de Mídia", "💡"),
]
base_links = [
    (st.Page("pages/01_Catalogos.py", title="Catálogo de Mídia", icon="🗂️"), "Catálogo de Mídia", "🗂️"),
    (st.Page("pages/04_Inventarios.py", title="Cadastro de Inventários", icon="📦"), "Cadastro de Inventários", "📦"),
    (st.Page("pages/15_Universos.py", title="Universos de Mercado", icon="🌎"), "Universos de Mercado", "🌎"),
    (st.Page("pages/16_Segmentos.py", title="Segmentos de Público", icon="🧭"), "Segmentos de Público", "🧭"),
    (st.Page("pages/14_Publicos.py", title="Públicos", icon="👥"), "Públicos", "👥"),
]
navegacao = st.navigation(
    [
        pagina_home,
        pagina_guia,
        *[item[0] for item in workflow_links],
        *[item[0] for item in analise_links],
        *[item[0] for item in base_links],
    ],
    position="hidden",
)

with st.sidebar:
    st.markdown("## PlanOS")
    st.caption("Plataforma Inteligente de Planejamento Híbrido de Mídia")
    active_context()
    if st.session_state.get("projeto_nome"):
        st.caption(f"Projeto ativo: {st.session_state['projeto_nome']}")
    st.page_link(pagina_home, label="Início", icon="🏠")
    st.page_link(pagina_guia, label="Guia de Uso", icon="📖")
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
    st.caption("Versão 2.0.0")
    st.caption("Tecnologias: Supabase · Streamlit · Codex · GitHub Codespaces")

navegacao.run()
