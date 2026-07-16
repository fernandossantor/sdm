import streamlit as st

from application.services.universe_service import (
    UniverseService
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Universos",

    page_icon="🌎",

    layout="wide"

)

st.title("🌎 Universos")

st.divider()

service = UniverseService()

# ==========================================================
# FORMULÁRIO
# ==========================================================

with st.expander(

    "Novo Universo",

    expanded=True

):

    nome = st.text_input(

    "Nome"

)

populacao = st.number_input(

    "População",

    min_value=0,

    value=0,

    step=1000

)

salvar = st.button(

    "Salvar Universo",

    type="primary",

    use_container_width=True

)

# ==========================================================
# SALVAR
# ==========================================================

if salvar:

    dados = {

    "nome": nome,

    "populacao": int(

        populacao

    ),

    #
    # Temporário até implementarmos Cenários
    #

    "cenario_id": None

    }

    ok, retorno = service.salvar(

        dados

    )

    if ok:

        st.success(

            "Universo salvo com sucesso."

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

c1, c2, c3 = st.columns(3)

c1.metric(

    "Universos",

    resumo["total"]

)

c2.metric(

    "Ativos",

    resumo["ativos"]

)

if populacao > 0:

    cobertura = round(

        (

            publico_alvo

            /

            populacao

        )

        * 100,

        2

    )

else:

    cobertura = 0

c3.metric(

    "Cobertura",

    f"{cobertura}%"

)

st.divider()

st.subheader(

    "Universos cadastrados"

)

universos = service.listar()

# ==========================================================
# LISTAGEM
# ==========================================================

if not universos:

    st.info(

        "Nenhum universo cadastrado."

    )

else:

    for universo in universos:

        with st.container():

            col1, col2, col3, col4, col5 = st.columns(

                [4, 2, 2, 2, 1]

            )

            with col1:

                st.markdown(

                    f"### {universo['nome']}"

                )

                descricao = []

                if universo.get("cidade"):

                    descricao.append(

                        universo["cidade"]

                    )

                if universo.get("estado"):

                    descricao.append(

                        universo["estado"]

                    )

                if universo.get("abrangencia"):

                    descricao.append(

                        universo["abrangencia"]

                    )

                if descricao:

                    st.caption(

                        " • ".join(descricao)

                    )

            with col2:

                st.metric(

                    "População",

                    f"{universo.get('populacao',0):,}".replace(",", ".")

                )

            with col3:

                st.metric(

                    "Público",

                    f"{universo.get('publico_alvo',0):,}".replace(",", ".")

                )

            with col4:

                pop = universo.get(

                    "populacao",

                    0

                )

                alvo = universo.get(

                    "publico_alvo",

                    0

                )

                if pop:

                    perc = round(

                        alvo / pop * 100,

                        1

                    )

                else:

                    perc = 0

                st.metric(

                    "Cobertura",

                    f"{perc}%"

                )

            with col5:

                if universo.get(

                    "ativo",

                    True

                ):

                    st.success(

                        "Ativo"

                    )

                else:

                    st.warning(

                        "Inativo"

                    )

                if st.button(

                    "🗑",

                    key=f"del_{universo['id']}"

                ):

                    service.excluir(

                        universo["id"]

                    )

                    st.rerun()

            st.divider()

# ==========================================================
# RODAPÉ
# ==========================================================

st.caption(

    "SDM • Cadastro Estratégico de Universos"

)