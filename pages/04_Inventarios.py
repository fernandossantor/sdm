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

plataformas = catalogos["plataformas"]

ambientes = catalogos["ambientes"]

estruturas = catalogos["estruturas"]

modelos = catalogos["modelos_comerciais"]

formatos = catalogos["formatos"]

modalidades = catalogos["modalidades"]

unidades = catalogos["unidades"]

st.write("Canais:", len(canais))

st.write("Ambientes:", len(ambientes))

st.write("Estruturas:", len(estruturas))

st.write("Modelos:", len(modelos))

st.write("Formatos:", len(formatos))

st.markdown("---")

nome = st.text_input(
    "Nome do Inventário"
)

plataforma = st.selectbox(

    "Plataforma",

    options=plataformas,

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

modalidade = st.selectbox(
    "Modalidade de compra",
    options=modalidades,
    format_func=lambda x: x["nome"],
)

unidade = st.selectbox(
    "Unidade de compra",
    options=unidades,
    format_func=lambda x: x["nome"],
)

st.subheader("Preço da mídia")

valor_bruto = st.number_input(
    "Valor bruto da unidade",
    min_value=0.0,
    value=0.0,
    step=1.0,
)

desconto = st.number_input(
    "Desconto negociado (%)",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
)

inicio_vigencia = st.date_input("Início da vigência", format="DD/MM/YYYY")
fim_vigencia = st.date_input("Fim da vigência", format="DD/MM/YYYY")

st.markdown("---")

st.write("Inventário:", nome)

st.write("Plataforma:", plataforma["nome"])

st.write("Ambiente:", ambiente["nome"])

st.write("Estrutura:", estrutura["nome"])

st.write("Modelo:", modelo["nome"])

st.write("Formato:", formato["nome"])

st.markdown("---")

if st.button("Salvar Inventário"):

    resposta = service.salvar_inventario({

        "nome": nome,

        "plataforma_id": plataforma["id"],

        "ambiente_id": ambiente["id"],

        "estrutura_id": estrutura["id"],

        "modelo_comercial_id": modelo["id"],

        "formato_id": formato["id"],

        "modalidade_compra_id": modalidade["id"],

        "unidade_compra_id": unidade["id"],

        "ativo": True,

        })

    inventario_id = resposta.data[0]["id"]

    if valor_bruto > 0:
        service.salvar_preco_inventario({
            "inventario_id": inventario_id,
            "unidade": unidade["nome"],
            "valor_bruto": float(valor_bruto),
            "desconto_percentual": float(desconto),
            "inicio_vigencia": inicio_vigencia.isoformat(),
            "fim_vigencia": fim_vigencia.isoformat(),
        })

    st.success("Inventário salvo com sucesso!")
