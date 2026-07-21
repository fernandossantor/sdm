import streamlit as st

from application.services.base_conhecimento_service import (
    BaseConhecimentoService
)


st.set_page_config(

    page_title="Inventários",

    layout="wide"

)


st.title("📦 Inventários")

st.markdown("---")


st.subheader("Cadastrar novo inventário")

service = BaseConhecimentoService()

catalogos = service.catalogos_inventario()

canais = catalogos["canais"]

ambientes = catalogos["ambientes"]

estruturas = catalogos["estruturas"]

modelos = catalogos["modelos_comerciais"]

formatos = catalogos["formatos"]

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

    service.salvar_inventario({

        "nome": nome,

        "canal_id": canal["id"],

        "ambiente_id": ambiente["id"],

        "estrutura_id": estrutura["id"],

        "modelo_comercial_id": modelo["id"],

        "formato_id": formato["id"]

        })

    st.success("Inventário salvo com sucesso!")
