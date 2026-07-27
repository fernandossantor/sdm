import streamlit as st

from application.services.auth_service import autenticacao_habilitada
from application.services.project_service import ProjectService
from application.services.project_sharing_service import ProjectSharingService
from components.page_config import PAGE_ICON, titulo_pagina


st.set_page_config(
    page_title=titulo_pagina("Colaboração"),
    page_icon=PAGE_ICON,
    layout="wide",
)

if not autenticacao_habilitada() or not st.session_state.get(
    "auth_access_token"
):
    st.error("É necessário entrar para administrar colaborações.")
    st.stop()

st.title("🤝 Colaboração em projetos")
st.caption(
    "O projeto é compartilhado sem duplicação. Leitores consultam, "
    "editores alteram e proprietários também gerenciam participantes."
)

projetos = ProjectService().listar()
if not projetos:
    st.info("Não há projetos disponíveis no espaço selecionado.")
    st.stop()

projeto = st.selectbox(
    "Projeto",
    projetos,
    format_func=lambda item: item.get("nome") or item["id"],
)
service = ProjectSharingService.from_access_token(
    st.session_state["auth_access_token"]
)

try:
    participantes = service.listar(projeto["id"])
    pode_gerenciar = True
except Exception:
    participantes = []
    pode_gerenciar = False

if not pode_gerenciar:
    st.info(
        "Você possui acesso ao projeto, mas somente o proprietário ou um "
        "administrador pode gerenciar participantes."
    )
    st.stop()

st.subheader("Participantes")
st.dataframe(
    [
        {
            "Nome": item.get("nome") or "—",
            "E-mail": item.get("email") or "—",
            "Papel": item.get("papel") or "—",
        }
        for item in participantes
    ],
    hide_index=True,
    width="stretch",
)

with st.expander("Conceder ou alterar acesso"):
    with st.form("compartilhar_projeto"):
        email = st.text_input("E-mail da conta já cadastrada")
        papel = st.selectbox(
            "Papel",
            ("LEITOR", "EDITOR", "PROPRIETARIO"),
            format_func=lambda valor: {
                "LEITOR": "Leitor",
                "EDITOR": "Editor",
                "PROPRIETARIO": "Transferir propriedade",
            }[valor],
        )
        confirmar_transferencia = st.checkbox(
            "Confirmo a transferência definitiva da propriedade.",
            disabled=papel != "PROPRIETARIO",
        )
        enviar = st.form_submit_button("Salvar acesso", type="primary")

    if enviar:
        if papel == "PROPRIETARIO" and not confirmar_transferencia:
            st.error("Confirme explicitamente a transferência.")
        else:
            try:
                service.compartilhar(projeto["id"], email, papel)
            except Exception:
                st.error(
                    "Não foi possível compartilhar. Confirme se a conta "
                    "está ativa e cadastrada."
                )
            else:
                st.success("Acesso atualizado.")
                st.rerun()

revogaveis = [
    item for item in participantes if item.get("papel") != "PROPRIETARIO"
]
if revogaveis:
    with st.expander("Revogar acesso"):
        with st.form("revogar_compartilhamento"):
            alvo = st.selectbox(
                "Participante",
                revogaveis,
                format_func=lambda item: (
                    f"{item.get('nome') or item.get('email')} · "
                    f"{item.get('papel')}"
                ),
            )
            confirmar = st.checkbox(
                "Confirmo a revogação imediata deste acesso."
            )
            revogar = st.form_submit_button("Revogar acesso")
        if revogar:
            if not confirmar:
                st.error("Confirme a revogação.")
            else:
                try:
                    service.revogar(projeto["id"], alvo["usuario_id"])
                except Exception:
                    st.error("Não foi possível revogar o acesso.")
                else:
                    st.success("Acesso revogado.")
                    st.rerun()
