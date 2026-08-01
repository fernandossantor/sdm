"""Portão de autenticação opcional para a implantação Streamlit."""

import streamlit as st
from pathlib import Path

from application.services.auth_service import AuthService


MARCA = Path(__file__).parents[1] / "assets" / "Marca_nova.png"


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

    margem_esquerda, conteudo, margem_direita = st.columns([1, 1.25, 1])
    with conteudo:
        if MARCA.exists():
            st.image(MARCA, use_container_width=True)
        st.title("Entrar no MediAd Planner")
        st.caption("O cadastro é controlado pela administração.")
        with st.form("login_planos", clear_on_submit=False):
            st.text_input("E-mail", key="login_email", autocomplete="email")
            st.text_input(
                "Senha",
                type="password",
                key="login_senha",
                autocomplete="current-password",
            )
            enviar = st.form_submit_button(
                "Entrar", type="primary", use_container_width=True
            )

    if enviar:
        st.info("Validando acesso…")
        email = str(st.session_state.get("login_email") or "").strip()
        senha = st.session_state.get("login_senha") or ""
        if not email or not senha:
            st.error("Preencha o e-mail e a senha antes de entrar.")
            return False
        try:
            service.entrar(email, senha, st.session_state)
        except Exception as exc:
            st.error("Não foi possível entrar. Confira suas credenciais e a configuração do Supabase.")
            # Mantém a causa visível para diagnóstico no Streamlit Cloud sem
            # expor senha, tokens ou qualquer outro segredo da sessão.
            st.caption(f"Detalhe técnico: {type(exc).__name__}: {exc}")
        else:
            st.success("Acesso validado. Carregando o MediAd Planner…")
            # O primeiro acesso ainda precisa passar pela troca obrigatória de
            # senha, que é renderizada no próximo ciclo com a sessão salva.
            st.rerun()

    return False
