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
formatos_ambientes = catalogos["formatos_ambientes"]
modalidades_unidades = catalogos["modalidades_unidades"]

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


NOVA_OPCAO_ID = "__nova_opcao__"


def escolher_catalogo(
    label,
    opcoes,
    prefixo,
    categoria,
    atual_id=None,
    parent_id=None,
    format_func=None,
):
    base_key = f"{prefixo}_{categoria}"
    revisao_key = f"{base_key}_revisao"
    pendente_key = f"{base_key}_pendente"
    revisao = st.session_state.get(revisao_key, 0)
    atual_id = st.session_state.pop(pendente_key, atual_id)
    nova_opcao = {"id": NOVA_OPCAO_ID, "nome": "Cadastrar outra opção…"}
    opcoes_exibidas = [*opcoes, nova_opcao]

    def exibir(item):
        if not isinstance(item, dict):
            return str(item)
        if format_func and item["id"] != NOVA_OPCAO_ID:
            return format_func(item)
        return item["nome"]

    selecionado = st.selectbox(
        label,
        opcoes_exibidas,
        index=indice_por_id(opcoes_exibidas, atual_id),
        format_func=exibir,
        key=f"{base_key}_selecao_{revisao}",
    )
    if selecionado["id"] != NOVA_OPCAO_ID:
        return selecionado

    st.caption(
        f'A nova opção será incorporada ao catálogo de {label.lower()} e '
        "ficará disponível nos próximos cadastros."
    )
    nome = st.text_input(f"Nome — novo {label.lower()}", key=f"{base_key}_nome")
    descricao = ""
    empresa = ""
    site = ""
    if categoria == "plataforma":
        empresa = st.text_input("Empresa", key=f"{base_key}_empresa")
        site = st.text_input("Site (opcional)", key=f"{base_key}_site")
    else:
        descricao = st.text_input(
            "Descrição (opcional)", key=f"{base_key}_descricao"
        )
    if st.button(f"Cadastrar e usar {label.lower()}", key=f"{base_key}_cadastrar"):
        try:
            novo = service.salvar_opcao_catalogo(
                categoria,
                nome,
                descricao=descricao,
                parent_id=parent_id,
                empresa=empresa,
                site=site,
            )
        except Exception as erro:
            st.error(f"Não foi possível cadastrar a opção: {erro}")
        else:
            st.session_state[pendente_key] = novo["id"]
            st.session_state[revisao_key] = revisao + 1
            st.rerun()
    st.info("Cadastre a nova opção para continuar o preenchimento.")
    return None


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

    tecnologia = escolher_catalogo(
        "Tecnologia", tecnologias, prefixo, "tecnologia", tecnologia_atual["id"]
    )
    if tecnologia is None:
        st.stop()
    canais_filtrados = [
        item for item in canais if item.get("tecnologia_id") == tecnologia["id"]
    ]
    canal = escolher_catalogo(
        "Canal", canais_filtrados, prefixo, "canal", canal_atual["id"], tecnologia["id"]
    )
    if canal is None:
        st.stop()
    ambientes_filtrados = [
        item for item in ambientes if item.get("canal_id") == canal["id"]
    ]
    ambiente = escolher_catalogo(
        "Ambiente", ambientes_filtrados, prefixo, "ambiente",
        inventario.get("ambiente_id"), canal["id"],
    )
    if ambiente is None:
        st.stop()
    estrutura = escolher_catalogo(
        "Estrutura", estruturas, prefixo, "estrutura", inventario.get("estrutura_id")
    )
    if estrutura is None:
        st.stop()

    formatos_ids = {
        item["formato_id"] for item in formatos_ambientes
        if item["ambiente_id"] == ambiente["id"]
    }
    formatos_filtrados = [item for item in formatos if item["id"] in formatos_ids]
    formato_atual = next(
        (item for item in formatos if item["id"] == inventario.get("formato_id")), None
    )
    if formato_atual and formato_atual not in formatos_filtrados:
        formatos_filtrados.append(formato_atual)
    formato = escolher_catalogo(
        "Formato", formatos_filtrados, prefixo, "formato",
        inventario.get("formato_id"), ambiente["id"],
    )
    if formato is None:
        st.stop()
    modelo = escolher_catalogo(
        "Modelo comercial", modelos, prefixo, "modelo_comercial",
        inventario.get("modelo_comercial_id"),
    )
    if modelo is None:
        st.stop()
    modalidade = escolher_catalogo(
        "Modalidade de compra", modalidades, prefixo, "modalidade",
        inventario.get("modalidade_compra_id"),
    )
    if modalidade is None:
        st.stop()

    unidades_ids = {
        item["unidade_id"] for item in modalidades_unidades
        if item["modalidade_id"] == modalidade["id"]
    }
    unidades_filtradas = [item for item in unidades if item["id"] in unidades_ids]
    unidade_atual = next(
        (item for item in unidades if item["id"] == inventario.get("unidade_compra_id")), None
    )
    if unidade_atual and unidade_atual not in unidades_filtradas:
        unidades_filtradas.append(unidade_atual)
    unidade = escolher_catalogo(
        "Unidade de compra", unidades_filtradas, prefixo, "unidade",
        inventario.get("unidade_compra_id"), modalidade["id"],
    )
    if unidade is None:
        st.stop()
    meio = escolher_catalogo(
        "Meio (plataforma/empresa)", plataformas, prefixo, "plataforma",
        inventario.get("plataforma_id"),
        format_func=lambda item: " — ".join(
            parte for parte in [item["nome"], item.get("empresa")] if parte
        ),
    )
    if meio is None:
        st.stop()
    kpi = escolher_catalogo("KPI", kpis, prefixo, "kpi", kpi_atual)
    if kpi is None:
        st.stop()

    nome = st.text_input("Nome", value=inventario.get("nome", ""), key=f"{prefixo}_nome")
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
        "modelo_comercial_id": modelo["id"], "modalidade_compra_id": modalidade["id"],
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
    return dados, preco_dados


if modo == "Cadastrar novo inventário":
    st.subheader("Cadastrar novo inventário")
    dados, preco = formulario("novo")
    if st.button("Salvar novo inventário", type="primary", width="stretch"):
        if preco["fim_vigencia"] < preco["inicio_vigencia"]:
            st.error("A vigência final não pode ser anterior à inicial.")
        else:
            try:
                resposta = service.salvar_inventario(dados)
                inventario_id = resposta.data[0]["id"]
                if preco["valor_bruto"] > 0:
                    service.salvar_preco_inventario({**preco, "inventario_id": inventario_id})
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
        preco_atual = next((item for item in reversed(precos) if item.get("ativo", True)), {})
        dados, preco = formulario(
            f"editar_{selecionado['id']}", selecionado, preco_atual,
            selecionado.get("kpi_principal_id"),
        )
        st.caption(f"Código: {selecionado.get('codigo') or selecionado['id'][:8]}")
        if st.button("Duplicar inventário", width="stretch"):
            try:
                service.duplicar_inventario(selecionado)
            except Exception as erro:
                st.error(f"Não foi possível duplicar: {erro}")
            else:
                st.success("Inventário duplicado com preços e vigências.")
                st.rerun()
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
    nome_col.write(f"{item.get('codigo') or item['id'][:8]} · {item['nome']}")
    if vigente:
        liquido = float(vigente["valor_bruto"]) * (
            1 - float(vigente.get("desconto_percentual", 0)) / 100
        )
        preco_col.write(f"{moeda_ptbr(liquido)} / {vigente['unidade']}")
    else:
        preco_col.caption("Sem preço vigente")
    with st.expander(f"Medições e correspondências — {item['nome']}"):
        medicoes = service.medicoes_inventario(item["id"])
        for medicao in reversed(medicoes):
            st.caption(
                f"{medicao['tipo_original']}: {medicao['valor_original']} "
                f"{medicao['unidade_original']} · fonte: {medicao['fonte']}"
            )
        m1, m2, m3 = st.columns(3)
        tipo_original = m1.text_input("Tipo original", key=f"mtipo_{item['id']}")
        valor_original = m2.number_input("Valor original", min_value=0.0, key=f"mvalor_{item['id']}")
        unidade_original = m3.text_input("Unidade original", key=f"munidade_{item['id']}")
        m4, m5, m6 = st.columns(3)
        audiencia_medida = m4.number_input("Equivalência: audiência (%)", 0.0, 100.0, key=f"maud_{item['id']}")
        alcance_medido = m5.number_input("Equivalência: alcance (%)", 0.0, 100.0, key=f"malc_{item['id']}")
        frequencia_medida = m6.number_input("Frequência observada", min_value=0.0, key=f"mfreq_{item['id']}")
        fonte_medicao = st.text_input("Fonte da medição", key=f"mfonte_{item['id']}")
        metodologia = st.text_area("Metodologia/correspondência", key=f"mmetodo_{item['id']}")
        confianca_medicao = st.selectbox(
            "Natureza", ["MEDIDO", "INFORMADO", "ESTIMADO"], key=f"mconf_{item['id']}"
        )
        if st.button("Salvar medição", key=f"msalvar_{item['id']}"):
            try:
                service.salvar_medicao_inventario({
                    "inventario_id": item["id"], "tipo_original": tipo_original,
                    "valor_original": valor_original, "unidade_original": unidade_original,
                    "audiencia_percentual": audiencia_medida or None,
                    "alcance_percentual": alcance_medido or None,
                    "frequencia": frequencia_medida or None, "fonte": fonte_medicao,
                    "metodologia": metodologia or None, "confianca": confianca_medicao,
                    "ativo": True,
                })
            except Exception as erro:
                st.error(str(erro))
            else:
                st.success("Medição salva.")
                st.rerun()
