import streamlit as st

from application.admin.account_admin_service import AccountAdminService
from application.services.auth_service import autenticacao_habilitada
from components.page_config import PAGE_ICON, titulo_pagina


st.set_page_config(
    page_title=titulo_pagina("Administração"),
    page_icon=PAGE_ICON,
    layout="wide",
)

if (
    not autenticacao_habilitada()
    or st.session_state.get("auth_papel_global") != "ADMINISTRADOR"
):
    st.error("Área restrita a administradores.")
    st.stop()

try:
    service = AccountAdminService.from_access_token(
        st.session_state.get("auth_access_token")
    )
except Exception:
    st.error("Não foi possível validar a sessão administrativa.")
    st.stop()

st.title("🛡️ Administração")
st.caption("Contas são criadas somente por administradores.")

with st.expander("Criar conta"):
    with st.form("criar_conta_admin"):
        nome = st.text_input("Nome")
        email = st.text_input("E-mail")
        papel = st.selectbox(
            "Papel global",
            ("USUARIO", "ADMINISTRADOR"),
            format_func=lambda valor: (
                "Usuário" if valor == "USUARIO" else "Administrador"
            ),
        )
        criar = st.form_submit_button("Criar conta", type="primary")

    if criar:
        try:
            resultado = service.criar(email, nome, papel)
        except Exception:
            st.error("Não foi possível criar a conta.")
        else:
            st.success("Conta criada. Copie a senha temporária agora.")
            st.code(resultado["senha_temporaria"], language=None)
            st.warning(
                "A senha não será exibida novamente e deverá ser alterada "
                "no primeiro acesso."
            )

st.subheader("Contas")
try:
    usuarios = service.listar()
except Exception:
    st.error("Não foi possível listar as contas.")
    usuarios = []

if usuarios:
    st.dataframe(
        [
            {
                "Nome": item.get("nome") or "—",
                "E-mail": item.get("email") or "—",
                "Papel": item.get("papel_global") or "—",
                "Ativa": bool(item.get("ativo")),
                "Trocar senha": bool(item.get("trocar_senha")),
                "Último acesso": item.get("ultimo_acesso_em") or "—",
            }
            for item in usuarios
        ],
        hide_index=True,
        width="stretch",
    )

    with st.expander("Ciclo de vida da conta"):
        with st.form("acao_conta_admin"):
            alvo = st.selectbox(
                "Conta",
                usuarios,
                format_func=lambda item: (
                    f"{item.get('nome') or 'Sem nome'} · {item.get('email')}"
                ),
            )
            acao = st.selectbox(
                "Ação",
                ("REDEFINIR_SENHA", "BLOQUEAR", "REATIVAR"),
                format_func=lambda valor: {
                    "REDEFINIR_SENHA": "Gerar nova senha temporária",
                    "BLOQUEAR": "Bloquear acesso",
                    "REATIVAR": "Reativar acesso",
                }[valor],
            )
            confirmado = st.checkbox(
                "Confirmo a ação sobre a conta selecionada."
            )
            executar = st.form_submit_button("Executar ação")

        if executar:
            if not confirmado:
                st.error("Confirme a ação antes de continuar.")
            else:
                try:
                    if acao == "BLOQUEAR":
                        service.bloquear(alvo["id"])
                        st.success("Conta bloqueada.")
                    elif acao == "REATIVAR":
                        service.reativar(alvo["id"])
                        st.success("Conta reativada.")
                    else:
                        senha = service.redefinir_senha(alvo["id"])
                        st.success(
                            "Senha temporária redefinida. Copie-a agora."
                        )
                        st.code(senha, language=None)
                        st.warning(
                            "A senha não será exibida novamente e deverá ser "
                            "alterada no primeiro acesso."
                        )
                except Exception:
                    st.error("A ação administrativa não pôde ser concluída.")

st.subheader("Auditoria administrativa")
st.caption(
    "Operações sensíveis são registradas sem senhas ou credenciais."
)
try:
    logs = service.listar_logs()
except Exception:
    st.error("Não foi possível consultar a auditoria.")
    logs = []

if logs:
    st.dataframe(
        [
            {
                "Data": item.get("criado_em") or "—",
                "Ação": item.get("acao") or "—",
                "Ator": item.get("ator_id") or "—",
                "Tipo": item.get("alvo_tipo") or "—",
                "Alvo": item.get("alvo_id") or "—",
                "Detalhes": item.get("detalhes") or {},
            }
            for item in logs
        ],
        hide_index=True,
        width="stretch",
    )
else:
    st.info("Ainda não há operações administrativas registradas.")
