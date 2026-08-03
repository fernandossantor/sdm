import streamlit as st


def apresentar_guia_de_uso() -> None:
    st.header("Guia de uso e glossário")
    st.subheader("Como usar o MediAd Planner")
    st.write("O conteúdo detalhado será implementado progressivamente.")
    st.subheader("Workflow metodológico")
    st.info(
        "Campanha → Briefing → Tradução Estratégica → Arquitetura de Mídia "
        "→ Simulação → Plano Consolidado"
    )
    st.subheader("Glossário")
    st.write("As definições de apoio serão incorporadas progressivamente.")
