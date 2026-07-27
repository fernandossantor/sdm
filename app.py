import streamlit as st
from dotenv import load_dotenv
import os
from pathlib import Path

from application.services.workflow_service import (
    WorkflowService
)

from components.home.hero import render as hero
from components.home.workflow_card import render as workflow_card
from components.home.projects_card import render as projects_card
from components.home.knowledge_card import render as knowledge_card
from components.active_context import render as active_context
from components.page_config import PAGE_ICON, PAGE_TITLE
from components.auth_gate import render as auth_gate
from components.workspace_gate import render as workspace_gate
from application.services.auth_service import AuthService, autenticacao_habilitada
from application.services.runtime_config_service import RuntimeConfigService
from infrastructure.database.data_client import (
    bind_authenticated_client,
    clear_request_client,
)
from infrastructure.database.workspace_context import clear_workspace


LOGO_MEDIAD_PLANNER = Path(__file__).parent / "assets" / "Marca.png"
# Streamlit não carrega automaticamente o arquivo .env. Isso precisa ocorrer
# antes da validação e da decisão de renderizar o portão de autenticação.
load_dotenv()

# No Streamlit Cloud, os valores ficam em ``st.secrets`` e não em um arquivo
# .env. Espelhamos somente a configuração em memória para que os clientes
# Supabase e a validação de runtime usem a mesma fonte de configuração.
for _nome in (
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "SUPABASE_SERVICE_KEY",
    "PLANOS_ENV",
    "PLANOS_AUTH_ENABLED",
):
    if os.getenv(_nome):
        continue
    try:
        _valor = st.secrets[_nome]
    except Exception:
        _valor = None
    if _valor is not None:
        os.environ[_nome] = str(_valor)

# Um app publicado com Supabase configurado deve sempre passar pelo portão de
# autenticação, salvo quando a implantação declarar explicitamente o contrário.
if (
    not os.getenv("PLANOS_AUTH_ENABLED")
    and os.getenv("SUPABASE_URL")
    and os.getenv("SUPABASE_KEY")
):
    os.environ["PLANOS_AUTH_ENABLED"] = "true"
RuntimeConfigService.validar()

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title=PAGE_TITLE,

    page_icon=PAGE_ICON,

    layout="wide",

    initial_sidebar_state="expanded"

)

clear_request_client()
clear_workspace()

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
    (st.Page("pages/11_Cenarios.py", title="Cenários e Sensibilidade", icon="🎛️"), "Cenários e Sensibilidade", "🎛️"),
    (
        st.Page(
            "pages/12_Otimizador.py",
            title="Otimização de Verba",
            icon="🎯",
        ),
        "Otimização de Verba",
        "🎯",
    ),
    (st.Page("pages/13_Insights.py", title="Insights de Mídia", icon="💡"), "Insights de Mídia", "💡"),
    (
        st.Page("pages/20_Atribuicao.py", title="Atribuição", icon="🔗"),
        "Atribuição",
        "🔗",
    ),
    (
        st.Page(
            "pages/21_Qualidade_e_Localizacao.py",
            title="Qualidade e Localização",
            icon="🛡️",
        ),
        "Qualidade e Localização",
        "🛡️",
    ),
]
base_links = [
    (st.Page("pages/01_Catalogos.py", title="Catálogo de Mídia", icon="🗂️"), "Catálogo de Mídia", "🗂️"),
    (st.Page("pages/04_Inventarios.py", title="Cadastro de Inventários", icon="📦"), "Cadastro de Inventários", "📦"),
    (st.Page("pages/15_Universos.py", title="Universos de Mercado", icon="🌎"), "Universos de Mercado", "🌎"),
    (st.Page("pages/16_Segmentos.py", title="Segmentos de Público", icon="🧭"), "Segmentos de Público", "🧭"),
    (st.Page("pages/14_Publicos.py", title="Públicos", icon="👥"), "Públicos", "👥"),
]
collaboration_links = []
if autenticacao_habilitada():
    collaboration_links.append(
        (
            st.Page(
                "pages/19_Colaboracao.py",
                title="Colaboração",
                icon="🤝",
            ),
            "Colaboração",
            "🤝",
        )
    )
admin_links = []
if (
    autenticacao_habilitada()
    and st.session_state.get("auth_papel_global") == "ADMINISTRADOR"
):
    admin_links.append(
        (
            st.Page(
                "pages/18_Administracao.py",
                title="Administração",
                icon="🛡️",
            ),
            "Administração",
            "🛡️",
        )
    )
navegacao = st.navigation(
    [
        pagina_home,
        pagina_guia,
        *[item[0] for item in workflow_links],
        *[item[0] for item in analise_links],
        *[item[0] for item in base_links],
        *[item[0] for item in collaboration_links],
        *[item[0] for item in admin_links],
    ],
    position="hidden",
)

# A navegação precisa ser registrada antes de qualquer st.stop(). Caso
# contrário, o Streamlit usa automaticamente os arquivos de pages/ e expõe
# os links laterais mesmo quando o portão de autenticação está na tela.
if autenticacao_habilitada():
    if not auth_gate():
        st.stop()
    bind_authenticated_client(st.session_state["auth_access_token"])
    if not workspace_gate():
        st.stop()
elif st.session_state.get("auth_access_token"):
    bind_authenticated_client(st.session_state["auth_access_token"])

with st.sidebar:
    st.image(LOGO_MEDIAD_PLANNER, width="stretch")
    st.caption("Plataforma Inteligente de Planejamento Híbrido de Mídia")
    if autenticacao_habilitada():
        st.caption(st.session_state.get("auth_email") or "Usuário autenticado")
        if st.button("Sair", use_container_width=True):
            AuthService().sair(st.session_state)
            clear_request_client()
            st.rerun()
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
    if admin_links:
        st.caption("ADMINISTRAÇÃO")
        for pagina, titulo, icone in admin_links:
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
