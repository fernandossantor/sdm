import streamlit as st

from application.services.segment_service import (
    SegmentService
)

from application.services.universe_service import (
    UniverseService
)

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Segmentos",

    page_icon="🎯",

    layout="wide"

)

st.title("🎯 Segmentos")

st.divider()

service = SegmentService()

universo_service = UniverseService()

universos = universo_service.listar()

if not universos:

    st.warning(

        "Cadastre pelo menos um Universo antes de criar Segmentos."

    )

    st.stop()

mapa_universos = {

    u["nome"]: u

    for u in universos

}

# ==========================================================
# FORMULÁRIO
# ==========================================================

with st.expander(

    "Novo Segmento",

    expanded=True

):

    universo_nome = st.selectbox(

        "Universo",

        list(

            mapa_universos.keys()

        )

    )

    universo = mapa_universos[

        universo_nome

    ]

    nome = st.text_input(

        "Nome"

    )

    col1, col2 = st.columns(2)

    with col1:

        sexo = st.selectbox(

            "Sexo",

            [

                "",

                "Masculino",

                "Feminino",

                "Ambos"

            ]

        )

        faixa = st.text_input(

            "Faixa etária"

        )

    with col2:

        classe = st.text_input(

            "Classe social"

        )

        escolaridade = st.text_input(

            "Escolaridade"

        )

    populacao = st.number_input(

        "População",

        min_value=0,

        value=0,

        step=1000

    )

    salvar = st.button(

        "Salvar Segmento",

        type="primary",

        use_container_width=True

    )

# ==========================================================
# SALVAR
# ==========================================================

if salvar:

    dados = {

        "universo_id": universo["id"],

        "nome": nome,

        "sexo": sexo if sexo else None,

        "faixa_etaria": faixa if faixa else None,

        "classe_social": classe if classe else None,

        "escolaridade": escolaridade if escolaridade else None,

        "populacao": int(

            populacao

        )

    }

    ok, retorno = service.salvar(

        dados

    )

    if ok:

        st.success(

            "Segmento salvo com sucesso."

        )

        st.rerun()

    else:

        for erro in retorno:

            st.error(

                erro

            )

# ==========================================================
# RESUMO
# ==========================================================

st.divider()

resumo = service.resumo()

c1, c2 = st.columns(2)

c1.metric(

    "Segmentos",

    resumo["total"]

)

c2.metric(

    "Universos",

    len(

        universos

    )

)

st.divider()

st.subheader(

    "Segmentos cadastrados"

)

segmentos = service.listar()

# ==========================================================
# LISTAGEM
# ==========================================================

if not segmentos:

    st.info(

        "Nenhum segmento cadastrado."

    )

else:

    for segmento in segmentos:

        universo = next(

            (

                u

                for u in universos

                if u["id"] == segmento["universo_id"]

            ),

            None

        )

        with st.container():

            col1, col2, col3, col4, col5 = st.columns(

                [4, 2, 2, 2, 1]

            )

            # ----------------------------------------------

            with col1:

                st.markdown(

                    f"### {segmento['nome']}"

                )

                if universo:

                    st.caption(

                        f"Universo: {universo['nome']}"

                    )

            # ----------------------------------------------

            with col2:

                st.write(

                    f"**Sexo:** {segmento.get('sexo') or '-'}"

                )

                st.write(

                    f"**Faixa:** {segmento.get('faixa_etaria') or '-'}"

                )

            # ----------------------------------------------

            with col3:

                st.write(

                    f"**Classe:** {segmento.get('classe_social') or '-'}"

                )

                st.write(

                    f"**Escolaridade:** {segmento.get('escolaridade') or '-'}"

                )

            # ----------------------------------------------

            with col4:

                st.metric(

                    "População",

                    f"{segmento.get('populacao',0):,}".replace(

                        ",",

                        "."

                    )

                )

            # ----------------------------------------------

            with col5:

                if st.button(

                    "🗑",

                    key=f"del_{segmento['id']}"

                ):

                    service.excluir(

                        segmento["id"]

                    )

                    st.rerun()

        st.divider()

# ==========================================================
# RODAPÉ
# ==========================================================

st.caption(

    "SDM • Cadastro Estratégico de Segmentos"

)

st.caption(
    "Segmentos refinam a classificação das audiências."
)

st.divider()