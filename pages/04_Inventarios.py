import streamlit as st

from infrastructure.database.supabase_client import supabase


st.set_page_config(

    page_title="Inventários",

    layout="wide"

)


st.title("📦 Inventários")

st.markdown("---")


st.subheader("Cadastrar novo inventário")

canais = (

    supabase

    .table("canais")

    .select("*")

    .order("nome")

    .execute()

).data


ambientes = (

    supabase

    .table("ambientes")

    .select("*")

    .order("nome")

    .execute()

).data


estruturas = (

    supabase

    .table("estruturas")

    .select("*")

    .order("nome")

    .execute()

).data


modelos = (

    supabase

    .table("modelos_comerciais")

    .select("*")

    .order("nome")

    .execute()

).data


formatos = (

    supabase

    .table("formatos")

    .select("*")

    .order("nome")

    .execute()

).data

st.write("Canais:", len(canais))

st.write("Ambientes:", len(ambientes))

st.write("Estruturas:", len(estruturas))

st.write("Modelos:", len(modelos))

st.write("Formatos:", len(formatos))

st.markdown("---")

nome = st.text_input(
    "Nome do Inventário"
)

canal = st.selectbox(

    "Canal",

    options=canais,

    format_func=lambda x: x["nome"]

)

ambiente = st.selectbox(

    "Ambiente",

    options=ambientes,

    format_func=lambda x: x["nome"]

)

estrutura = st.selectbox(

    "Estrutura",

    options=estruturas,

    format_func=lambda x: x["nome"]

)

modelo = st.selectbox(

    "Modelo Comercial",

    options=modelos,

    format_func=lambda x: x["nome"]

)

formato = st.selectbox(

    "Formato",

    options=formatos,

    format_func=lambda x: x["nome"]

)

st.markdown("---")

st.write("Inventário:", nome)

st.write("Canal:", canal["nome"])

st.write("Ambiente:", ambiente["nome"])

st.write("Estrutura:", estrutura["nome"])

st.write("Modelo:", modelo["nome"])

st.write("Formato:", formato["nome"])

st.markdown("---")

if st.button("Salvar Inventário"):
    
    supabase.table("inventarios").insert({

        "nome": nome,

        "canal_id": canal["id"],

        "ambiente_id": ambiente["id"],

        "estrutura_id": estrutura["id"],

        "modelo_comercial_id": modelo["id"],

        "formato_id": formato["id"]

        }).execute()

    st.success("Inventário salvo com sucesso!")

    st.caption(
    "Inventários representam as oportunidades de mídia disponíveis para planejamento."
)

st.divider()