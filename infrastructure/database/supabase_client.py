"""Compatibilidade para chamadas públicas, sem cliente criado no import."""

from infrastructure.database.data_client import get_public_client


class _ClientePublicoPreguicoso:
    def __getattr__(self, atributo):
        return getattr(get_public_client(), atributo)


supabase = _ClientePublicoPreguicoso()
