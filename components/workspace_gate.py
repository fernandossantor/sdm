import streamlit as st

from application.services.workspace_service import WorkspaceService


def render():
    service = WorkspaceService()
    espacos = service.listar(
        st.session_state.get("auth_user_id"),
        administrador=(
            st.session_state.get("auth_papel_global") == "ADMINISTRADOR"
        ),
    )
    if not espacos:
        st.error("Sua conta ainda não possui um espaço de trabalho ativo.")
        return False

    atual = st.session_state.get("espaco_id")
    autorizados = {item["id"] for item in espacos}
    if atual not in autorizados:
        atual = espacos[0]["id"] if len(espacos) == 1 else None

    with st.sidebar:
        selecionado = st.selectbox(
            "Espaço de trabalho",
            [None, *espacos],
            index=next(
                (
                    indice
                    for indice, item in enumerate([None, *espacos])
                    if item and item["id"] == atual
                ),
                0,
            ),
            format_func=lambda item: (
                "Selecione…" if item is None else item["nome"]
            ),
            key="seletor_espaco_trabalho",
        )

    if not selecionado:
        st.info("Selecione um espaço de trabalho para continuar.")
        return False

    service.selecionar(selecionado["id"], espacos, st.session_state)
    return True
