import streamlit as st

st.title("📚 Base de Conhecimento")

st.caption(
    "Gerencie os conhecimentos utilizados pelos motores do SDM."
)

st.info(
    """
Selecione uma área para visualizar ou editar os dados utilizados
no planejamento de mídia.
"""
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/02_Universo.py", label="🎯 Audiências")
    st.page_link("pages/04_Inventarios.py", label="📺 Inventários")
    st.page_link("pages/03_MCP_Papeis.py", label="👥 Papéis de Compra")

with col2:
    st.button("🎯 Objetivos", disabled=True)
    st.button("📈 Indicadores", disabled=True)
    st.button("📡 Canais", disabled=True)

with col3:
    st.button("💻 Plataformas", disabled=True)
    st.button("📰 Formatos", disabled=True)
    st.button("⚙ Tecnologias", disabled=True)

st.button("🔧 Parâmetros", disabled=True)