import streamlit as st

from application.services.public_service import (
    PublicService
)

from application.services.base_conhecimento_service import (
    BaseConhecimentoService
)
from application.services.universe_service import UniverseService
from application.services.segment_service import SegmentService


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Públicos",

    page_icon="👥",

    layout="wide"

)

st.title("👥 Públicos")

st.divider()

service = PublicService()

base_conhecimento = BaseConhecimentoService()

universo_service = UniverseService()

segmento_service = SegmentService()

# ==========================================================
# CATÁLOGOS
# ==========================================================

biblioteca = base_conhecimento.biblioteca_publicos()

universos = [u for u in universo_service.listar() if u.get("ativo", True)]

interesses = biblioteca["interesses"]

jornadas = biblioteca["jornadas"]

if not universos:
    st.warning("Cadastre pelo menos um Universo antes de criar Públicos.")
    st.stop()

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

    universo = st.selectbox(

        "Universo",

        options=universos,

        format_func=lambda item: item["nome"]

    )

    segmentos = [
        item
        for item in segmento_service.listar_por_universo(universo["id"])
        if item.get("ativo", True)
    ]

    segmentos_sel = st.multiselect(

        "Segmentos",

        options=segmentos,

        format_func=lambda item: item["nome"]

    )

    interesses_sel = st.multiselect(

        "Interesses",

        options=interesses,

        format_func=lambda item: item["nome"]

    )

    jornada_nome = st.selectbox(

        "Jornada",

        options=[None] + jornadas,

        format_func=lambda item: (
            "Selecione uma etapa"
            if item is None
            else (
                f"{item.get('ordem', '')}. {item['etapa']} "
                f"({item.get('descricao', item['etapa'])})"
            ).lstrip(". ")
        )

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

    dados = {

        "nome": nome,

        "descricao": descricao,

        "ativo": ativo

    }

    ok, retorno = service.salvar(

        dados=dados,

        segmentos=[
            item["id"] for item in segmentos_sel

        ],

        interesses=[
            item["id"] for item in interesses_sel

        ],

        jornada=(

            jornada_nome["id"]

            if jornada_nome is not None

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

publicos = service.listar_detalhados()

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

                f"### {publico.get('codigo') or publico['id'][:8]} · {publico['nome']}"

            )

            if publico.get(

                "descricao"

            ):

                st.write(

                    publico["descricao"]

                )

            trilhas = []
            for segmento in publico.get("segmentos", []):
                universo_rel = next(
                    (
                        item
                        for item in publico.get("universos", [])
                        if item["id"] == segmento.get("universo_id")
                    ),
                    None,
                )
                if universo_rel:
                    trilhas.append(f"{universo_rel['nome']} › {segmento['nome']}")

            if trilhas:
                st.caption(" | ".join(trilhas))

            if publico.get("jornada"):
                etapa = publico["jornada"]
                st.caption(
                    f"Jornada: {etapa['etapa']} "
                    f"({etapa.get('descricao', etapa['etapa'])})"
                )

            if publico.get("interesses"):
                st.caption(
                    "Interesses: "
                    + ", ".join(item["nome"] for item in publico["interesses"])
                )

        with c2:

            if st.button("Duplicar", key=f"dup_{publico['id']}"):
                service.duplicar(publico)
                st.rerun()

            if st.button(

                "🗑",

                key=f"del_{publico['id']}"

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
