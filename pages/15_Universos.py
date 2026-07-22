import streamlit as st

from application.services.universe_service import (
    UniverseService
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Universos de Mercado",

    page_icon="🌎",

    layout="wide"

)

st.title("🌎 Universos de Mercado")

st.divider()

service = UniverseService()

UFS = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP", "SE", "TO",
]

# ==========================================================
# FORMULÁRIO
# ==========================================================

with st.expander(

    "Novo Universo",

    expanded=True

):
    nome = st.text_input("Nome")
    c_cidade, c_estado = st.columns([3, 1])
    with c_cidade:
        cidade = st.text_input("Cidade")
    with c_estado:
        estado = st.selectbox("Estado (UF)", UFS)
    c_populacao, _ = st.columns(2)
    with c_populacao:
        populacao = st.number_input(
            "População",
            min_value=0,
            value=0,
            step=1000,
        )
    salvar = st.button(
        "Salvar Universo",
        type="primary",
        width="stretch",
    )

# ==========================================================
# SALVAR
# ==========================================================

if salvar:

    dados = {
        "nome": nome,
        "cidade": cidade.strip(),
        "estado": estado,
        "populacao": int(populacao),
        "cenario_id": None,
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

c1, c2 = st.columns(2)

c1.metric(

    "Universos",

    resumo["total"]

)

c2.metric(

    "Ativos",

    resumo["ativos"]

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

            col1, col2, col3 = st.columns(

                [5, 2, 1]

            )

            with col1:

                st.markdown(

                    f"### {universo.get('codigo') or universo['id'][:8]} · {universo['nome']}"

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

                    "Duplicar",

                    key=f"dup_{universo['id']}"

                ):

                    service.duplicar(universo)
                    st.rerun()

                if st.button(

                    "🗑",

                    key=f"del_{universo['id']}"

                ):

                    _, mensagem = service.excluir(universo["id"])
                    st.toast(mensagem)
                    st.rerun()

            st.divider()

# ==========================================================
# RODAPÉ
# ==========================================================

st.caption(

    "SDM • Cadastro Estratégico de Universos"

)
