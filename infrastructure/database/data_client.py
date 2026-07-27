"""Cliente de dados por requisição, autenticado com JWT quando disponível."""

import os
from contextvars import ContextVar
from functools import lru_cache

from dotenv import load_dotenv
from supabase import create_client

from infrastructure.database.admin_client import admin


_cliente_requisicao = ContextVar("cliente_dados_requisicao", default=None)


def _configuracao_publica():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    chave = os.getenv("SUPABASE_KEY")
    if not url or not chave:
        raise RuntimeError(
            "SUPABASE_URL e SUPABASE_KEY devem estar configuradas para "
            "operações autenticadas."
        )
    return url, chave


@lru_cache(maxsize=1)
def get_public_client():
    """Cliente anônimo compartilhado, sem estado de autenticação."""
    return create_client(*_configuracao_publica())


def create_auth_client():
    """Cria cliente isolado para não compartilhar sessão entre usuários."""
    return create_client(*_configuracao_publica())


def create_authenticated_client(access_token):
    """Cria cliente PostgREST com o JWT do usuário, sem usar service_role."""
    if not str(access_token or "").strip():
        raise ValueError("Token de acesso do usuário é obrigatório.")
    cliente = create_auth_client()
    cliente.postgrest.auth(str(access_token))
    return cliente


def bind_authenticated_client(access_token):
    cliente = create_authenticated_client(access_token)
    _cliente_requisicao.set(cliente)
    return cliente


def clear_request_client():
    _cliente_requisicao.set(None)


def get_data_client():
    """Resolve o cliente da requisição; mantém admin apenas durante transição."""
    return _cliente_requisicao.get() or admin


def using_authenticated_client():
    return _cliente_requisicao.get() is not None
