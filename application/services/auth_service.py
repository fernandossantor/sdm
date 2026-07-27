"""Autenticação Supabase sem persistir senhas ou compartilhar sessões."""

import os
import time

from infrastructure.database.data_client import create_auth_client


CHAVES_AUTH = (
    "auth_access_token",
    "auth_refresh_token",
    "auth_expires_at",
    "auth_user_id",
    "auth_email",
    "auth_trocar_senha",
)


def autenticacao_habilitada():
    return os.getenv("PLANOS_AUTH_ENABLED", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "sim",
    }


class AuthService:
    def __init__(self, client_factory=create_auth_client):
        self.client_factory = client_factory

    @staticmethod
    def _salvar_sessao(session_state, sessao):
        if not sessao or not getattr(sessao, "access_token", None):
            raise RuntimeError("O provedor não retornou uma sessão válida.")

        usuario = getattr(sessao, "user", None)
        session_state["auth_access_token"] = sessao.access_token
        session_state["auth_refresh_token"] = sessao.refresh_token
        session_state["auth_expires_at"] = getattr(sessao, "expires_at", None)
        session_state["auth_user_id"] = str(getattr(usuario, "id", "") or "")
        session_state["auth_email"] = getattr(usuario, "email", "") or ""

    @staticmethod
    def limpar_sessao(session_state):
        for chave in CHAVES_AUTH:
            session_state.pop(chave, None)

    @staticmethod
    def _carregar_perfil(cliente, session_state):
        resposta = (
            cliente.table("perfis_usuarios")
            .select("ativo,trocar_senha")
            .eq("id", session_state["auth_user_id"])
            .single()
            .execute()
        )
        perfil = resposta.data or {}
        if not perfil.get("ativo"):
            raise PermissionError("A conta está inativa.")
        session_state["auth_trocar_senha"] = bool(perfil.get("trocar_senha"))

    def entrar(self, email, senha, session_state):
        if not str(email or "").strip() or not senha:
            raise ValueError("E-mail e senha são obrigatórios.")

        cliente = self.client_factory()
        resposta = cliente.auth.sign_in_with_password(
            {"email": email.strip(), "password": senha}
        )
        try:
            self._salvar_sessao(session_state, resposta.session)
            self._carregar_perfil(cliente, session_state)
        except Exception:
            self.limpar_sessao(session_state)
            raise
        return resposta.user

    def renovar_se_necessario(self, session_state, margem_segundos=60):
        token = session_state.get("auth_access_token")
        refresh_token = session_state.get("auth_refresh_token")
        expira_em = session_state.get("auth_expires_at")
        if not token or not refresh_token:
            self.limpar_sessao(session_state)
            return False

        if expira_em and float(expira_em) > time.time() + margem_segundos:
            return True

        try:
            cliente = self.client_factory()
            resposta = cliente.auth.set_session(token, refresh_token)
            self._salvar_sessao(session_state, resposta.session)
            return True
        except Exception:
            self.limpar_sessao(session_state)
            return False

    def sair(self, session_state):
        token = session_state.get("auth_access_token")
        refresh_token = session_state.get("auth_refresh_token")
        try:
            if token and refresh_token:
                cliente = self.client_factory()
                cliente.auth.set_session(token, refresh_token)
                cliente.auth.sign_out()
        finally:
            self.limpar_sessao(session_state)

    def alterar_senha(self, nova_senha, session_state):
        if len(str(nova_senha or "")) < 8:
            raise ValueError("A nova senha deve ter pelo menos 8 caracteres.")
        token = session_state.get("auth_access_token")
        refresh_token = session_state.get("auth_refresh_token")
        if not token or not refresh_token:
            raise RuntimeError("É necessário entrar novamente.")
        cliente = self.client_factory()
        cliente.auth.set_session(token, refresh_token)
        resposta = cliente.auth.update_user({"password": nova_senha})
        cliente.rpc("confirmar_troca_senha").execute()
        session_state["auth_trocar_senha"] = False
        return resposta
