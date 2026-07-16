import streamlit as st

from application.services.briefing_service import (
    BriefingService
)

from application.services.public_service import (
    PublicService
)

from infrastructure.repositories.decision_repository import (
    DecisionRepository
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Novo Briefing",

    page_icon="📝",

    layout="wide"

)

st.title("📝 Briefing Inteligente")

st.divider()

repo = DecisionRepository()

briefing_service = BriefingService()

public_service = PublicService()


# ==========================================================
# CATÁLOGOS
# ==========================================================

objetivos = repo.all(

    "objetivos_campanha_v3"

)

kpis = repo.kpis()

publicos = public_service.listar()


# ==========================================================
# IDENTIFICAÇÃO
# ==========================================================

st.header(

    "Identificação da Campanha"

)

col1, col2 = st.columns(2)

with col1:

    cliente = st.text_input(

        "Cliente"

    )

    marca = st.text_input(

        "Marca"

    )

    campanha = st.text_input(

        "Campanha"

    )

with col2:

    produto = st.text_input(

        "Produto"

    )

    orcamento = st.number_input(

        "Orçamento",

        min_value=0.0,

        value=100000.0,

        step=1000.0

    )

    objetivo_nome = st.selectbox(

        "Objetivo Principal",

        [

            o["nome"]

            for o in objetivos

        ]

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

    ]

)

if not kpis_escolhidos:

    st.info(

        "Caso nenhum KPI seja selecionado, será utilizado o KPI principal."

    )

kpi_principal = st.selectbox(

    "KPI Principal",

    [

        k["nome"]

        for k in kpis

    ]

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

        "Data inicial"

    )

with c2:

    fim = st.date_input(

        "Data final"

    )

with c3:

    tipo_flight = st.selectbox(

        "Tipo",

        [

            "CONTINUO",

            "PULSADO",

            "SAZONAL",

            "ALWAYS_ON"

        ]

    )


frequencia = st.selectbox(

    "Frequência desejada",

    [

        "LIVRE",

        "1-2",

        "3-5",

        "6+"

    ]

)


# ==========================================================
# PÚBLICOS
# ==========================================================

st.divider()

st.header(

    "Públicos"

)

nomes_publicos = [

    p["nome"]

    for p in publicos

]

publicos_escolhidos = st.multiselect(

    "Biblioteca de Públicos",

    nomes_publicos

)

publicos_modelo = []

for nome in publicos_escolhidos:

    publico = next(

        p

        for p in publicos

        if p["nome"] == nome

    )

    publicos_modelo.append(

        {

            "id": publico["id"],

            "nome": publico["nome"],

            "peso": 100

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

    height=120

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

        f"R$ {orcamento:,.2f}"

    )


# ==========================================================
# SALVAR
# ==========================================================

st.divider()

salvar = st.button(

    "Salvar Briefing",

    type="primary",

    use_container_width=True

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

            "Briefing salvo na sessão."

        )

        st.info(

            "Agora acesse Planejamento."

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

            f"**Frequência:** {briefing.frequencia_objetivo}"

        )

    st.write(

        f"**Orçamento:** R$ {briefing.orcamento:,.2f}"

    )

    if briefing.observacoes:

        st.info(

            briefing.observacoes

        )

# ==========================================================
# FIM DO ARQUIVO
# ==========================================================