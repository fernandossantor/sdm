import streamlit as st


def render():

    st.subheader(

        "Projetos"

    )

    st.info(

        "Nenhum projeto iniciado."

    )

    if st.button(

        "➕ Novo Briefing",

        width="stretch"

    ):

        st.switch_page(

            "pages/00_Briefing.py"

        )