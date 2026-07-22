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

    page_title="Segmentos de Público",

    page_icon="🎯",

    layout="wide"

)

st.title("🎯 Segmentos de Público")

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

CLASSES_SOCIAIS = ["A", "B", "C", "D", "E"]
FAIXAS_ETARIAS = [
    "0-3", "4-7", "8-12", "12-15", "15-18", "19-24", "25-29",
    "30-34", "35-39", "40-44", "45-49", "50-54", "55-59",
    "60-64", "65-69", "70-74", "75-79", "80+",
]
ESCOLARIDADES = [
    "Analfabeto",
    "Ensino fundamental",
    "Ensino médio",
    "Ensino superior",
]

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

    sexo = st.selectbox(

            "Sexo",

            [

                "",

                "Masculino",

                "Feminino",

                "Ambos"

            ]

        )

    c_classe, c_faixa, c_escolaridade = st.columns(3)
    with c_classe:
        todas_classes = st.checkbox("Todas as classes")
        classes_sociais = st.multiselect(
            "Classes sociais *",
            CLASSES_SOCIAIS,
            default=CLASSES_SOCIAIS if todas_classes else [],
            disabled=todas_classes,
        )
        if todas_classes:
            classes_sociais = CLASSES_SOCIAIS

    with c_faixa:
        todas_faixas = st.checkbox("Todas as faixas etárias")
        faixas_etarias = st.multiselect(
            "Faixas etárias *",
            FAIXAS_ETARIAS,
            default=FAIXAS_ETARIAS if todas_faixas else [],
            disabled=todas_faixas,
        )
        if todas_faixas:
            faixas_etarias = FAIXAS_ETARIAS

    with c_escolaridade:
        todas_escolaridades = st.checkbox("Todas as escolaridades")
        escolaridades = st.multiselect(
            "Escolaridades *",
            ESCOLARIDADES,
            default=ESCOLARIDADES if todas_escolaridades else [],
            disabled=todas_escolaridades,
        )
        if todas_escolaridades:
            escolaridades = ESCOLARIDADES

    populacao = st.number_input(

        "População",

        min_value=0,

        value=0,

        step=1000

    )

    salvar = st.button(

        "Salvar Segmento",

        type="primary",

        width="stretch"

    )

# ==========================================================
# SALVAR
# ==========================================================

if salvar:

    dados = {

        "universo_id": universo["id"],

        "nome": nome,

        "sexo": sexo if sexo else None,

        "faixa_etaria": ", ".join(faixas_etarias) or None,

        "classe_social": ", ".join(classes_sociais) or None,

        "escolaridade": ", ".join(escolaridades) or None,

        "faixas_etarias": faixas_etarias,

        "classes_sociais": classes_sociais,

        "escolaridades": escolaridades,

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

                    "**Faixas:** " + ", ".join(
                        segmento.get("faixas_etarias")
                        or ([segmento["faixa_etaria"]] if segmento.get("faixa_etaria") else ["-"])
                    )

                )

            # ----------------------------------------------

            with col3:

                st.write(

                    "**Classes:** " + ", ".join(
                        segmento.get("classes_sociais")
                        or ([segmento["classe_social"]] if segmento.get("classe_social") else ["-"])
                    )

                )

                st.write(

                    "**Escolaridades:** " + ", ".join(
                        segmento.get("escolaridades")
                        or ([segmento["escolaridade"]] if segmento.get("escolaridade") else ["-"])
                    )

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

                    _, mensagem = service.excluir(segmento["id"])
                    st.toast(mensagem)
                    st.rerun()

        st.divider()

# ==========================================================
# RODAPÉ
# ==========================================================

st.caption(

    "SDM • Cadastro Estratégico de Segmentos"

)
