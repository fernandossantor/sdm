import calendar
from datetime import date

import streamlit as st

from application.services.base_conhecimento_service import BaseConhecimentoService
from components.formatters import moeda_ptbr


st.set_page_config(page_title="Cadastro de Inventários", page_icon="📦", layout="wide")
st.title("📦 Cadastro de Inventários")
st.write(
    "Cadastre as oportunidades comerciais disponíveis nos meios e mantenha "
    "preços e vigências atualizados para o Plano de Mídia."
)

service = BaseConhecimentoService()
catalogos = service.catalogos_inventario()
tecnologias = catalogos["tecnologias"]
canais = catalogos["canais"]
ambientes = catalogos["ambientes"]
estruturas = catalogos["estruturas"]
formatos = catalogos["formatos"]
modelos = catalogos["modelos_comerciais"]
modalidades = catalogos["modalidades"]
unidades = catalogos["unidades"]
plataformas = catalogos["plataformas"]
kpis = catalogos["kpis"]

st.subheader("Base de conhecimento disponível")
resumo = {
    "Tecnologias": len(tecnologias), "Canais": len(canais),
    "Ambientes": len(ambientes), "Estruturas": len(estruturas),
    "Formatos": len(formatos), "Modelos comerciais": len(modelos),
    "Modalidades": len(modalidades), "Unidades": len(unidades),
    "Meios": len(plataformas), "KPIs": len(kpis),
}
st.write(" · ".join(f"**{nome}:** {total}" for nome, total in resumo.items()))

try:
    cadastrados = service.listar_inventarios()
except Exception as erro:
    st.error(f"Não foi possível listar os inventários: {erro}")
    cadastrados = []

st.divider()
modo = st.radio(
    "O que deseja fazer?",
    ["Cadastrar novo inventário", "Editar inventário salvo"],
    horizontal=True,
)


def indice_por_id(opcoes, valor):
    return next((i for i, item in enumerate(opcoes) if item["id"] == valor), 0)


def selecionar_mes(prefixo, valor=None):
    valor = valor or date.today()
    meses = list(range(1, 13))
    anos = list(range(date.today().year - 5, date.today().year + 11))
    c_mes, c_ano = st.columns(2)
    mes = c_mes.selectbox(
        "Mês", meses, index=valor.month - 1,
        format_func=lambda item: f"{item:02d}", key=f"{prefixo}_mes",
    )
    ano = c_ano.selectbox(
        "Ano", anos,
        index=anos.index(valor.year) if valor.year in anos else 5,
        key=f"{prefixo}_ano",
    )
    return mes, ano


def formulario(prefixo, inventario=None, preco=None, kpi_atual=None):
    inventario = inventario or {}
    preco = preco or {}

    ambiente_atual = next(
        (item for item in ambientes if item["id"] == inventario.get("ambiente_id")),
        ambientes[0],
    )
    canal_atual = next(
        (item for item in canais if item["id"] == ambiente_atual.get("canal_id")),
        canais[0],
    )
    tecnologia_atual = next(
        (item for item in tecnologias if item["id"] == canal_atual.get("tecnologia_id")),
        tecnologias[0],
    )

    tecnologia = st.selectbox(
        "Tecnologia", tecnologias,
        index=indice_por_id(tecnologias, tecnologia_atual["id"]),
        format_func=lambda item: item["nome"], key=f"{prefixo}_tecnologia",
    )
    canais_filtrados = [
        item for item in canais if item.get("tecnologia_id") == tecnologia["id"]
    ]
    if not canais_filtrados:
        st.error("A tecnologia selecionada não possui canais relacionados no Catálogo.")
        st.stop()
    canal = st.selectbox(
        "Canal", canais_filtrados,
        index=indice_por_id(canais_filtrados, canal_atual["id"]),
        format_func=lambda item: item["nome"], key=f"{prefixo}_canal",
    )
    ambientes_filtrados = [
        item for item in ambientes if item.get("canal_id") == canal["id"]
    ]
    if not ambientes_filtrados:
        st.error("O canal selecionado não possui ambientes relacionados no Catálogo.")
        st.stop()
    ambiente = st.selectbox(
        "Ambiente", ambientes_filtrados,
        index=indice_por_id(ambientes_filtrados, inventario.get("ambiente_id")),
        format_func=lambda item: item["nome"], key=f"{prefixo}_ambiente",
    )
    estrutura = st.selectbox(
        "Estrutura", estruturas,
        index=indice_por_id(estruturas, inventario.get("estrutura_id")),
        format_func=lambda item: item["nome"], key=f"{prefixo}_estrutura",
    )
    formato = st.selectbox(
        "Formato", formatos,
        index=indice_por_id(formatos, inventario.get("formato_id")),
        format_func=lambda item: item["nome"], key=f"{prefixo}_formato",
    )
    modelo = st.selectbox(
        "Modelo comercial", modelos,
        index=indice_por_id(modelos, inventario.get("modelo_comercial_id")),
        format_func=lambda item: item["nome"], key=f"{prefixo}_modelo",
    )
    modalidade = st.selectbox(
        "Modalidade de compra", modalidades,
        index=indice_por_id(modalidades, inventario.get("modalidade_compra_id")),
        format_func=lambda item: item["nome"], key=f"{prefixo}_modalidade",
    )
    unidade = st.selectbox(
        "Unidade de compra", unidades,
        index=indice_por_id(unidades, inventario.get("unidade_compra_id")),
        format_func=lambda item: item["nome"], key=f"{prefixo}_unidade",
    )
    meio = st.selectbox(
        "Meio (plataforma/empresa)", plataformas,
        index=indice_por_id(plataformas, inventario.get("plataforma_id")),
        format_func=lambda item: " — ".join(
            parte for parte in [item["nome"], item.get("empresa")] if parte
        ), key=f"{prefixo}_meio",
    )
    kpi = st.selectbox(
        "KPI", kpis, index=indice_por_id(kpis, kpi_atual),
        format_func=lambda item: item["nome"], key=f"{prefixo}_kpi",
    )
    nome = st.text_input(
        "Nome", value=inventario.get("nome", ""), key=f"{prefixo}_nome"
    )
    valor = st.number_input(
        "Preço bruto por unidade", min_value=0.0,
        value=float(preco.get("valor_bruto") or 0), key=f"{prefixo}_valor",
    )
    desconto = st.number_input(
        "Desconto negociado (%)", min_value=0.0, max_value=100.0,
        value=float(preco.get("desconto_percentual") or 0), key=f"{prefixo}_desconto",
    )
    st.markdown("**Vigência inicial (MM/AAAA)**")
    inicio_data = date.fromisoformat(preco["inicio_vigencia"][:10]) if preco.get("inicio_vigencia") else date.today()
    inicio_mes, inicio_ano = selecionar_mes(f"{prefixo}_inicio", inicio_data)
    st.markdown("**Vigência final (MM/AAAA)**")
    fim_data = date.fromisoformat(preco["fim_vigencia"][:10]) if preco.get("fim_vigencia") else date.today()
    fim_mes, fim_ano = selecionar_mes(f"{prefixo}_fim", fim_data)

    dados = {
        "nome": nome, "plataforma_id": meio["id"], "ambiente_id": ambiente["id"],
        "estrutura_id": estrutura["id"], "formato_id": formato["id"],
        "modelo_comercial_id": modelo["id"],
        "modalidade_compra_id": modalidade["id"],
        "unidade_compra_id": unidade["id"], "kpi_principal_id": kpi["id"],
        "ativo": inventario.get("ativo", True),
    }
    inicio = date(inicio_ano, inicio_mes, 1)
    fim = date(fim_ano, fim_mes, calendar.monthrange(fim_ano, fim_mes)[1])
    preco_dados = {
        "unidade": unidade["nome"], "valor_bruto": float(valor),
        "desconto_percentual": float(desconto),
        "inicio_vigencia": inicio.isoformat(), "fim_vigencia": fim.isoformat(),
    }
    return dados, preco_dados, kpi


if modo == "Cadastrar novo inventário":
    st.subheader("Cadastrar novo inventário")
    dados, preco, kpi = formulario("novo")
    if st.button("Salvar novo inventário", type="primary", width="stretch"):
        if preco["fim_vigencia"] < preco["inicio_vigencia"]:
            st.error("A vigência final não pode ser anterior à inicial.")
        else:
            try:
                resposta = service.salvar_inventario(dados)
                inventario_id = resposta.data[0]["id"]
                if preco["valor_bruto"] > 0:
                    service.salvar_preco_inventario(
                        {**preco, "inventario_id": inventario_id}
                    )
            except Exception as erro:
                st.error(f"Não foi possível salvar o inventário: {erro}")
            else:
                st.success("Inventário salvo.")
                st.rerun()
else:
    st.subheader("Editar inventário salvo")
    if not cadastrados:
        st.info("Nenhum inventário disponível para edição.")
    else:
        selecionado = st.selectbox(
            "Inventário salvo", cadastrados,
            format_func=lambda item: item["nome"], key="inventario_salvo",
        )
        precos = service.precos_inventario(selecionado["id"])
        preco_atual = next(
            (item for item in reversed(precos) if item.get("ativo", True)), {}
        )
        kpi_atual = selecionado.get("kpi_principal_id")
        dados, preco, kpi = formulario(
            f"editar_{selecionado['id']}", selecionado, preco_atual, kpi_atual
        )
        if st.button("Salvar alterações", type="primary", width="stretch"):
            if preco["fim_vigencia"] < preco["inicio_vigencia"]:
                st.error("A vigência final não pode ser anterior à inicial.")
            else:
                try:
                    service.atualizar_inventario(selecionado["id"], dados)
                    if preco["valor_bruto"] > 0:
                        service.salvar_preco_inventario(
                            {**preco, "inventario_id": selecionado["id"]}
                        )
                except Exception as erro:
                    st.error(f"Não foi possível atualizar o inventário: {erro}")
                else:
                    st.success("Inventário atualizado.")
                    st.rerun()

st.divider()
st.subheader("Inventários disponíveis para o Plano de Mídia")
for item in cadastrados:
    precos = service.precos_inventario(item["id"])
    vigente = next((p for p in reversed(precos) if p.get("ativo", True)), None)
    nome_col, preco_col = st.columns([3, 2])
    nome_col.write(item["nome"])
    if vigente:
        liquido = float(vigente["valor_bruto"]) * (
            1 - float(vigente.get("desconto_percentual", 0)) / 100
        )
        preco_col.write(f"{moeda_ptbr(liquido)} / {vigente['unidade']}")
    else:
        preco_col.caption("Sem preço vigente")
