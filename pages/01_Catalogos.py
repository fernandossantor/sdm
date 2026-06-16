import streamlit as st

from infrastructure.database.supabase_client import supabase

st.set_page_config(
    page_title="Catálogos",
    layout="wide"
)

st.title("📚 Catálogos")

st.markdown("---")

st.subheader("Canais")

response = (
    supabase
    .table("canais")
    .select("*")
    .execute()
)

dados = response.data

if dados:
    st.dataframe(
        dados,
        width="stretch"
    )
else:
    st.warning("Nenhum canal encontrado.")