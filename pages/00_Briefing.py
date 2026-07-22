import streamlit as st

from application.services.briefing_service import (
    BriefingService
)

from application.services.public_service import (
    PublicService
)

from application.services.base_conhecimento_service import (
    BaseConhecimentoService
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

base_conhecimento = BaseConhecimentoService()

briefing_service = BriefingService()

public_service = PublicService()


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

        "Data inicial",

        format="DD/MM/YYYY"

    )

with c2:

    fim = st.date_input(

        "Data final",

        format="DD/MM/YYYY"

    )

with c3:

    tipo_flight = st.selectbox(

        "Tipo",

        [

            "LINEAR",

            "ONDA",

            "CONCENTRADO"

        ]

    )


frequencia = st.selectbox(

    "Frequência desejada",

    [

        "BAIXA",

        "MEDIA",

        "ALTA"

    ],

    format_func=lambda valor: {
        "BAIXA": "Baixa (1–3)",
        "MEDIA": "Média (4–7)",
        "ALTA": "Alta (8+)",
    }[valor]

)

limites_frequencia = {
    "BAIXA": (1, 3, 2),
    "MEDIA": (4, 7, 5),
    "ALTA": (8, 30, 8),
}

freq_min, freq_max, freq_padrao = limites_frequencia[frequencia]

frequencia_alvo = st.number_input(
    "Frequência alvo",
    min_value=freq_min,
    max_value=freq_max,
    value=freq_padrao,
    help="Valor numérico usado nas projeções de alcance e orçamento.",
)

st.subheader("Alcance da campanha")

alcance_objetivo = st.selectbox(
    "Faixa de alcance",
    ["BAIXO", "MEDIO", "ALTO"],
    index=1,
    format_func=lambda valor: {
        "BAIXO": "Baixo (até 50% do público)",
        "MEDIO": "Médio (51% a 69% do público)",
        "ALTO": "Alto (70% a 100% do público)",
    }[valor],
)

limites_alcance = {
    "BAIXO": (0, 50, 40),
    "MEDIO": (51, 69, 60),
    "ALTO": (70, 100, 80),
}
alcance_min, alcance_max, alcance_padrao = limites_alcance[alcance_objetivo]
alcance_percentual = st.number_input(
    "Percentual de alcance desejado",
    min_value=alcance_min,
    max_value=alcance_max,
    value=alcance_padrao,
    format="%d%%",
    help="Percentual do público estimado que a campanha deve alcançar.",
)


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
    )

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

        frequencia_alvo=int(frequencia_alvo),

        alcance_objetivo=alcance_objetivo,

        alcance_percentual=int(alcance_percentual),

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

            f"**Alcance:** {briefing.alcance_objetivo} "
            f"({briefing.alcance_percentual}%)"

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
