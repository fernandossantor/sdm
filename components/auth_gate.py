"""Portão de autenticação opcional para a implantação Streamlit."""

import streamlit as st

from application.services.auth_service import AuthService


def render():
    service = AuthService()

    if service.renovar_se_necessario(st.session_state):
        if not st.session_state.get("auth_trocar_senha"):
            return True

        st.title("Defina uma nova senha")
        st.caption("A senha temporária deve ser substituída no primeiro acesso.")
        with st.form("troca_senha_planos"):
            nova_senha = st.text_input("Nova senha", type="password")
            confirmacao = st.text_input("Confirme a nova senha", type="password")
            alterar = st.form_submit_button("Alterar senha", type="primary")
        if alterar:
            if nova_senha != confirmacao:
                st.error("As senhas não coincidem.")
            else:
                try:
                    service.alterar_senha(nova_senha, st.session_state)
                except Exception:
                    st.error("Não foi possível alterar a senha.")
                else:
                    st.success("Senha alterada.")
                    st.rerun()
        return False

    st.title("Entrar no PlanOS")
    st.caption("O cadastro é controlado pela administração.")
    with st.form("login_planos"):
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        enviar = st.form_submit_button("Entrar", type="primary")

    if enviar:
        try:
            service.entrar(email, senha, st.session_state)
        except Exception:
            st.error("Não foi possível entrar. Confira suas credenciais.")
        else:
            st.rerun()

    return False
