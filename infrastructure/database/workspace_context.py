"""Contexto do espaço ativo, isolado por execução da sessão."""

from contextvars import ContextVar


_espaco_ativo = ContextVar("espaco_ativo", default=None)


def bind_workspace(espaco_id):
    valor = str(espaco_id or "").strip()
    if not valor:
        raise ValueError("Espaço de trabalho é obrigatório.")
    _espaco_ativo.set(valor)
    return valor


def clear_workspace():
    _espaco_ativo.set(None)


def get_workspace():
    return _espaco_ativo.get()


def require_workspace():
    espaco_id = get_workspace()
    if not espaco_id:
        raise RuntimeError("Selecione um espaço de trabalho.")
    return espaco_id
