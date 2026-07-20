import streamlit as st

from components.workspace.ui_state import show_workspace_notice

from application.session import Session


def render():

    if not Session.has_campaign():

        st.info("Nenhuma campanha selecionada.")

        return

    campaign_id = Session.current_campaign()

    st.sidebar.divider()

    st.sidebar.markdown("## 📁 Workspace")

    st.sidebar.caption(campaign_id)

    modules = [

        ("dashboard", "📊 Dashboard"),

        ("briefing", "📝 Briefing"),

        ("publico", "🎯 Público"),

        ("objetivos", "🎯 Objetivos"),

        ("estrategia", "🧭 Estratégia"),






        ("relatorios", "📄 Relatórios")

    ]

    if "workspace_module" not in st.session_state:

        st.session_state.workspace_module = "dashboard"

    for key, label in modules:

        if st.sidebar.button(

            label,

            use_container_width=True,

            key=f"workspace_{key}"

        ):

            st.session_state.workspace_module = key

            st.rerun()


show_workspace_notice()
