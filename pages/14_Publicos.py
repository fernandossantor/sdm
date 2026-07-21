import streamlit as st

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

    page_title="Biblioteca de Públicos",

    page_icon="👥",

    layout="wide"

)

st.title("👥 Biblioteca de Públicos")

st.divider()

service = PublicService()

base_conhecimento = BaseConhecimentoService()

# ==========================================================
# CATÁLOGOS
# ==========================================================

biblioteca = base_conhecimento.biblioteca_publicos()

segmentos = biblioteca["segmentos"]

interesses = biblioteca["interesses"]

jornadas = biblioteca["jornadas"]

# ==========================================================
# FORMULÁRIO
# ==========================================================

with st.expander(

    "Novo Público",

    expanded=True

):

    nome = st.text_input(

        "Nome"

    )

    descricao = st.text_area(

        "Descrição"

    )

    ativo = st.checkbox(

        "Ativo",

        value=True

    )

    segmentos_sel = st.multiselect(

        "Segmentos",

        options=[

            s["nome"]

            for s in segmentos

        ]

    )

    interesses_sel = st.multiselect(

        "Interesses",

        options=[

            i["nome"]

            for i in interesses

        ]

    )

    jornada_nome = st.selectbox(

        "Jornada",

        [""] +

        [

            j["etapa"]

            for j in jornadas

        ]

    )

    salvar = st.button(

        "Salvar Público",

        type="primary",

        width="stretch"

    )

# ==========================================================
# SALVAR
# ==========================================================

if salvar:

    mapa_segmentos = {

        s["nome"]: s["id"]

        for s in segmentos

    }

    mapa_interesses = {

        i["nome"]: i["id"]

        for i in interesses

    }

    mapa_jornadas = {

        j["etapa"]: j["id"]

        for j in jornadas

    }

    dados = {

        "nome": nome,

        "descricao": descricao,

        "ativo": ativo

    }

    ok, retorno = service.salvar(

        dados=dados,

        segmentos=[

            mapa_segmentos[x]

            for x in segmentos_sel

        ],

        interesses=[

            mapa_interesses[x]

            for x in interesses_sel

        ],

        jornada=(

            mapa_jornadas[jornada_nome]

            if jornada_nome

            else None

        )

    )

    if ok:

        st.success(

            "Público salvo."

        )

        st.rerun()

    else:

        for erro in retorno:

            st.error(

                erro

            )

# ==========================================================
# LISTAGEM
# ==========================================================

st.divider()

st.subheader(

    "Biblioteca"

)

publicos = service.listar()

if not publicos:

    st.info(

        "Nenhum público cadastrado."

    )

else:

    for publico in publicos:

        c1, c2 = st.columns(

            [5, 1]

        )

        with c1:

            st.markdown(

                f"### {publico['nome']}"

            )

            if publico.get(

                "descricao"

            ):

                st.write(

                    publico["descricao"]

                )

        with c2:

            if st.button(

                "🗑",

                key=publico["id"]

            ):

                service.excluir(

                    publico["id"]

                )

                st.rerun()

st.divider()

resumo = service.resumo()

c1, c2 = st.columns(2)

c1.metric(

    "Total",

    resumo["total"]

)

c2.metric(

    "Ativos",

    resumo["ativos"]

)
