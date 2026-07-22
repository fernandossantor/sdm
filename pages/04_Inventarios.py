from datetime import date

import streamlit as st

from application.services.base_conhecimento_service import (
    BaseConhecimentoService
)


st.set_page_config(

    page_title="Inventários",

    layout="wide"

)


st.title("📦 Inventários")

st.write(
    "Os inventários e seus preços vigentes alimentam diretamente o ranking, "
    "a distribuição de verba e as estimativas do Planejamento."
)

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


def indice_por_id(opcoes, valor):
    return next(
        (indice for indice, item in enumerate(opcoes) if item["id"] == valor),
        0,
    )

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

    if fim_vigencia < inicio_vigencia:
        st.error("A data final da vigência não pode ser anterior à data inicial.")
        st.stop()

    try:
        resposta = service.salvar_inventario(
            {
                "nome": nome,
                "plataforma_id": plataforma["id"],
                "ambiente_id": ambiente["id"],
                "estrutura_id": estrutura["id"],
                "modelo_comercial_id": modelo["id"],
                "formato_id": formato["id"],
                "modalidade_compra_id": modalidade["id"],
                "unidade_compra_id": unidade["id"],
                "ativo": True,
            }
        )

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
    except Exception as erro:
        st.error(f"Não foi possível salvar o Inventário: {erro}")
    else:
        st.success("Inventário salvo e disponível para classificação e planejamento.")
        c_mcp, c_plano = st.columns(2)
        with c_mcp:
            st.page_link(
                "pages/03_MCP_Papeis.py",
                label="Classificar papel no MCP",
                icon="🧩",
                width="stretch",
            )
        with c_plano:
            st.page_link(
                "pages/05_Planejamento.py",
                label="Ir para Planejamento",
                icon="🧠",
                width="stretch",
            )

try:
    cadastrados = service.listar_inventarios()
except Exception as erro:
    st.error(f"Não foi possível listar os inventários: {erro}")
    cadastrados = []

st.divider()
st.subheader("Editar inventário")

if not cadastrados:
    st.info("Nenhum inventário disponível para edição.")
else:
    selecionado = st.selectbox(
        "Inventário cadastrado",
        cadastrados,
        format_func=lambda item: item["nome"],
        key="inventario_edicao",
    )
    precos_edicao = service.precos_inventario(selecionado["id"])
    preco_atual = next(
        (item for item in reversed(precos_edicao) if item.get("ativo", True)),
        {},
    )

    with st.form("form_editar_inventario"):
        nome_edicao = st.text_input(
            "Nome",
            value=selecionado["nome"],
        )
        e1, e2 = st.columns(2)
        with e1:
            plataforma_edicao = st.selectbox(
                "Plataforma",
                plataformas,
                index=indice_por_id(plataformas, selecionado.get("plataforma_id")),
                format_func=lambda item: item["nome"],
            )
            ambiente_edicao = st.selectbox(
                "Ambiente",
                ambientes,
                index=indice_por_id(ambientes, selecionado.get("ambiente_id")),
                format_func=lambda item: item["nome"],
            )
            estrutura_edicao = st.selectbox(
                "Estrutura",
                estruturas,
                index=indice_por_id(estruturas, selecionado.get("estrutura_id")),
                format_func=lambda item: item["nome"],
            )
            formato_edicao = st.selectbox(
                "Formato",
                formatos,
                index=indice_por_id(formatos, selecionado.get("formato_id")),
                format_func=lambda item: item["nome"],
            )
        with e2:
            modelo_edicao = st.selectbox(
                "Modelo comercial",
                modelos,
                index=indice_por_id(modelos, selecionado.get("modelo_comercial_id")),
                format_func=lambda item: item["nome"],
            )
            modalidade_edicao = st.selectbox(
                "Modalidade de compra",
                modalidades,
                index=indice_por_id(modalidades, selecionado.get("modalidade_compra_id")),
                format_func=lambda item: item["nome"],
            )
            unidade_edicao = st.selectbox(
                "Unidade de compra",
                unidades,
                index=indice_por_id(unidades, selecionado.get("unidade_compra_id")),
                format_func=lambda item: item["nome"],
            )
            ativo_edicao = st.checkbox(
                "Ativo",
                value=selecionado.get("ativo", True),
            )

        st.caption("Ao informar preço, uma nova vigência comercial será criada.")
        p1, p2 = st.columns(2)
        with p1:
            valor_edicao = st.number_input(
                "Novo valor bruto",
                min_value=0.0,
                value=float(preco_atual.get("valor_bruto") or 0),
            )
            inicio_edicao = st.date_input(
                "Início da nova vigência",
                value=date.today(),
                format="DD/MM/YYYY",
            )
        with p2:
            desconto_edicao = st.number_input(
                "Desconto (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(preco_atual.get("desconto_percentual") or 0),
            )
            fim_edicao = st.date_input(
                "Fim da nova vigência",
                value=date.today(),
                format="DD/MM/YYYY",
            )

        atualizar = st.form_submit_button(
            "Salvar alterações",
            type="primary",
            width="stretch",
        )

    if atualizar:
        if fim_edicao < inicio_edicao:
            st.error("A data final não pode ser anterior à data inicial.")
        else:
            try:
                service.atualizar_inventario(
                    selecionado["id"],
                    {
                        "nome": nome_edicao,
                        "plataforma_id": plataforma_edicao["id"],
                        "ambiente_id": ambiente_edicao["id"],
                        "estrutura_id": estrutura_edicao["id"],
                        "modelo_comercial_id": modelo_edicao["id"],
                        "formato_id": formato_edicao["id"],
                        "modalidade_compra_id": modalidade_edicao["id"],
                        "unidade_compra_id": unidade_edicao["id"],
                        "ativo": ativo_edicao,
                    },
                )
                if valor_edicao > 0:
                    service.salvar_preco_inventario(
                        {
                            "inventario_id": selecionado["id"],
                            "unidade": unidade_edicao["nome"],
                            "valor_bruto": float(valor_edicao),
                            "desconto_percentual": float(desconto_edicao),
                            "inicio_vigencia": inicio_edicao.isoformat(),
                            "fim_vigencia": fim_edicao.isoformat(),
                        }
                    )
            except Exception as erro:
                st.error(f"Não foi possível atualizar o Inventário: {erro}")
            else:
                st.success("Inventário atualizado e nova vigência registrada.")
                st.rerun()

st.divider()
st.subheader("Inventários disponíveis para o Planejamento")

if not cadastrados:
    st.info("Nenhum inventário cadastrado.")
else:
    for item in cadastrados:
        precos = service.precos_inventario(item["id"])
        vigente = next(
            (preco for preco in reversed(precos) if preco.get("ativo", True)),
            None,
        )
        c_nome, c_preco = st.columns([3, 2])
        c_nome.write(item["nome"])
        if vigente:
            liquido = float(vigente["valor_bruto"]) * (
                1 - float(vigente.get("desconto_percentual", 0)) / 100
            )
            c_preco.write(f"R$ {liquido:,.2f} / {vigente['unidade']}")
        else:
            c_preco.caption("Sem preço vigente cadastrado")
