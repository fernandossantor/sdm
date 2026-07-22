import streamlit as st


def render():

    st.subheader("🎯 Campanhas")

    st.success(
        "Comece criando uma nova campanha para que o PlanOS possa gerar um plano de mídia."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.page_link(
            "pages/00_Briefing.py",
            label="➕ Nova Campanha",
            width="stretch"
        )

    with col2:

        st.button(
            "📂 Abrir Campanha",
            disabled=True,
            width="stretch"
        )
