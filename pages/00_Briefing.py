import streamlit as st
from components.formatters import moeda_ptbr

from application.services.briefing_service import (
    BriefingService
)

from application.services.public_service import (
    PublicService
)

from application.services.base_conhecimento_service import (
    BaseConhecimentoService
)
from application.services.project_service import ProjectService
from components.grp_fields import render as render_grp
from application.services.identifier_service import IdentifierService


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Briefing de Mídia",

    page_icon="📝",

    layout="wide"

)

st.title("📝 Briefing de Mídia")

st.divider()

base_conhecimento = BaseConhecimentoService()

briefing_service = BriefingService()

public_service = PublicService()
project_service = ProjectService()

if not st.session_state.get("projeto_id"):
    st.warning("Crie ou selecione um projeto antes de preencher o briefing.")
    projetos = project_service.listar()
    nomes_projetos = [item["nome"] for item in projetos]
    if nomes_projetos:
        projeto_nome = st.selectbox("Projeto existente", nomes_projetos)
        if st.button("Selecionar projeto"):
            projeto = next(item for item in projetos if item["nome"] == projeto_nome)
            project_service.selecionar(projeto, st.session_state)
            st.rerun()
    novo_nome = st.text_input("Ou nomeie um novo projeto")
    if st.button("Criar projeto", type="primary"):
        project_service.criar(novo_nome, st.session_state)
        st.rerun()
    st.stop()

st.caption(
    f"Projeto: **{st.session_state.get('projeto_codigo') or ''} · "
    f"{st.session_state['projeto_nome']}**"
)
if st.session_state.get("briefing_codigo"):
    st.caption(f"Briefing ativo: **{st.session_state['briefing_codigo']}**")

with st.expander("Briefings salvos", expanded=False):
    registros_briefing = briefing_service.listar(st.session_state["projeto_id"])
    if not registros_briefing:
        st.info("Nenhum briefing salvo.")
    for registro in registros_briefing:
        a, b, copia, c = st.columns([4, 1, 1, 1])
        a.write(IdentifierService.rotulo(registro))
        if b.button("Editar", key=f"editar_briefing_{registro['id']}"):
            briefing_service.carregar(registro, st.session_state)
            st.rerun()
        if copia.button("Duplicar", key=f"duplicar_briefing_{registro['id']}"):
            briefing_service.duplicar(registro, st.session_state)
            st.rerun()
        if c.button("Excluir", key=f"excluir_briefing_{registro['id']}"):
            briefing_service.excluir(registro["id"], st.session_state)
            st.rerun()

edicao = st.session_state.get("briefing")


# ==========================================================
# CATÁLOGOS
# ==========================================================

objetivos = base_conhecimento.objetivos()

kpis = base_conhecimento.kpis()

publicos = public_service.listar_detalhados()


# ==========================================================
# IDENTIFICAÇÃO
# ==========================================================

st.header(

    "Identificação da Campanha"

)

col1, col2 = st.columns(2)

with col1:

    cliente = st.text_input(

        "Cliente", value=getattr(edicao, "cliente", "")

    )

    marca = st.text_input(

        "Marca", value=getattr(edicao, "marca", "")

    )

    campanha = st.text_input(

        "Campanha", value=getattr(edicao, "campanha", "")

    )

with col2:

    produto = st.text_input(

        "Produto", value=getattr(edicao, "produto", "")

    )

    orcamento = st.number_input(

        "Orçamento",

        min_value=0.0,

        value=float(getattr(edicao, "orcamento", 100000.0)),

        step=1000.0

    )

    nomes_objetivos = [o["nome"] for o in objetivos]
    objetivo_atual = getattr(edicao, "objetivo", nomes_objetivos[0])
    objetivo_nome = st.selectbox(

        "Objetivo Principal",

        nomes_objetivos,
        index=nomes_objetivos.index(objetivo_atual) if objetivo_atual in nomes_objetivos else 0,

    )

objetivo = next(

    o

    for o in objetivos

    if o["nome"] == objetivo_nome

)


# ==========================================================
# KPIs
# ==========================================================

st.divider()

st.header(

    "KPIs"

)

kpis_escolhidos = st.multiselect(

    "Selecione um ou mais KPIs",

    [

        k["nome"]

        for k in kpis

    ],
    default=[item.get("nome") for item in getattr(edicao, "kpis", []) if item.get("nome")]

)

if not kpis_escolhidos:

    st.info(

        "Caso nenhum KPI seja selecionado, será utilizado o KPI principal."

    )

nomes_kpis = [k["nome"] for k in kpis]
kpi_atual = getattr(edicao, "kpi", nomes_kpis[0])
kpi_principal = st.selectbox(

    "KPI Principal",

    nomes_kpis,
    index=nomes_kpis.index(kpi_atual) if kpi_atual in nomes_kpis else 0,

)

lista_kpis = []

for nome in kpis_escolhidos:

    lista_kpis.append(

        {

            "nome": nome,

            "peso": 100

        }

    )


# ==========================================================
# FLIGHT
# ==========================================================

st.divider()

st.header(

    "Flight"

)

c1, c2, c3 = st.columns(3)

with c1:

    inicio = st.date_input(

        "Data inicial",

        value=getattr(edicao, "inicio", None) or "today",
        format="DD/MM/YYYY"

    )

with c2:

    fim = st.date_input(

        "Data final",

        value=getattr(edicao, "fim", None) or "today",
        format="DD/MM/YYYY"

    )

with c3:

    tipo_flight = st.selectbox(

        "Tipo",

        [

            "LINEAR",

            "ONDA",

            "CONCENTRADO"

        ],
        index={"LINEAR": 0, "ONDA": 1, "CONCENTRADO": 2}.get(getattr(edicao, "tipo_flight", "LINEAR"), 0),

    )


st.subheader("Alcance, frequência média e GRP")
metricas_midia = render_grp(
    "briefing_metricas",
    alcance=getattr(edicao, "alcance_percentual", 60),
    frequencia=getattr(edicao, "frequencia_alvo", 5),
    grp=getattr(edicao, "grp", None),
)
frequencia = metricas_midia["frequencia_objetivo"]
frequencia_alvo = metricas_midia["frequencia_alvo"]
alcance_objetivo = metricas_midia["alcance_objetivo"]
alcance_percentual = metricas_midia["alcance_percentual"]
grp = metricas_midia["grp"]


# ==========================================================
# PÚBLICOS
# ==========================================================

st.divider()

st.header(

    "Públicos"

)

publicos_escolhidos = st.multiselect(

    "Biblioteca de Públicos",

    options=publicos,

    format_func=lambda publico: " / ".join(
        [
            " › ".join(
                [universo["nome"], segmento["nome"]]
            )
            for segmento in publico.get("segmentos", [])
            for universo in publico.get("universos", [])
            if universo["id"] == segmento.get("universo_id")
        ]
        + [publico["nome"]]
    ),
    default=[
        publico for publico in publicos
        if publico["id"] in {item.get("id") for item in getattr(edicao, "publicos", [])}
    ]

)

publicos_modelo = []

for publico in publicos_escolhidos:

    publicos_modelo.append(

        {

            "id": publico["id"],

            "nome": publico["nome"],

            "peso": 100

            ,"populacao_estimada": publico.get("populacao_estimada", 0)

            ,"interesses": publico.get("interesses", [])

            ,"jornada": publico.get("jornada")

        }

    )

st.caption(

    "Em breve será possível criar públicos diretamente nesta tela."

)

# ==========================
# CONTINUA NA PARTE 2
# ==========================

# ==========================================================
# OBSERVAÇÕES
# ==========================================================

st.divider()

st.header(

    "Observações"

)

observacoes = st.text_area(

    "Observações da campanha",

    height=120,
    value=getattr(edicao, "observacoes", "")

)


# ==========================================================
# RESUMO
# ==========================================================

st.divider()

st.header(

    "Resumo"

)

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(

        "KPIs",

        len(lista_kpis)

    )

with c2:

    st.metric(

        "Públicos",

        len(publicos_modelo)

    )

with c3:

    st.metric(

        "Orçamento",

        moeda_ptbr(orcamento)

    )


# ==========================================================
# SALVAR
# ==========================================================

st.divider()

salvar = st.button(

        "Atualizar Briefing" if st.session_state.get("briefing_id") else "Salvar Briefing",

    type="primary",

    width="stretch"

)


# ==========================================================
# PROCESSAMENTO
# ==========================================================

if salvar:

    briefing = briefing_service.criar(

        cliente=cliente,

        campanha=campanha,

        objetivo_id=objetivo["id"],

        objetivo=objetivo["nome"],

        kpi=kpi_principal,

        kpis=lista_kpis,

        marca=marca,

        produto=produto,

        orcamento=orcamento,

        inicio=inicio,

        fim=fim,

        tipo_flight=tipo_flight,

        frequencia_objetivo=frequencia,

        frequencia_alvo=float(frequencia_alvo),

        alcance_objetivo=alcance_objetivo,

        alcance_percentual=float(alcance_percentual),

        grp=float(grp),

        publicos=publicos_modelo,

        observacoes=observacoes

    )

    erros = briefing_service.validar(

        briefing

    )

    if erros:

        for erro in erros:

            st.error(

                erro

            )

    else:

        briefing_service.salvar(

            st.session_state,

            briefing

        )

        st.success(

            "Briefing salvo no projeto e disponível para edição."

        )

        st.info(

            "Agora acesse Papéis dos Meios."

        )


# ==========================================================
# BRIEFING DA SESSÃO
# ==========================================================

if briefing_service.existe(

    st.session_state

):

    briefing = briefing_service.recuperar(

        st.session_state

    )

    st.divider()

    st.subheader(

        "Briefing Atual"

    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(

            f"**Cliente:** {briefing.cliente}"

        )

        st.write(

            f"**Marca:** {briefing.marca}"

        )

        st.write(

            f"**Produto:** {briefing.produto}"

        )

        st.write(

            f"**Campanha:** {briefing.campanha}"

        )

        st.write(

            f"**Objetivo:** {briefing.objetivo}"

        )

    with col2:

        st.write(

            f"**KPI Principal:** {briefing.kpi}"

        )

        st.write(

            f"**KPIs Selecionados:** {len(briefing.kpis)}"

        )

        st.write(

            f"**Públicos:** {len(briefing.publicos)}"

        )

        st.write(

            f"**Flight:** {briefing.tipo_flight}"

        )

        st.write(

            f"**Frequência:** {briefing.frequencia_objetivo} "
            f"({briefing.frequencia_alvo})"

        )

        st.write(f"**GRP:** {briefing.grp}")

        st.write(

            f"**Alcance:** {briefing.alcance_objetivo} "
            f"({briefing.alcance_percentual}%)"

        )

    st.write(

        f"**Orçamento:** {moeda_ptbr(briefing.orcamento)}"

    )

    if briefing.observacoes:

        st.info(

            briefing.observacoes

        )

# ==========================================================
# FIM DO ARQUIVO
# ==========================================================
