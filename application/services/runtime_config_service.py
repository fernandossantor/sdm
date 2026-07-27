"""Validação fail-closed da configuração de execução."""

import os

from application.services.auth_service import autenticacao_habilitada


class RuntimeConfigService:
    PRODUCAO = {"production", "producao", "produção"}

    @classmethod
    def validar(cls):
        ambiente = os.getenv("PLANOS_ENV", "development").strip().lower()
        if ambiente not in cls.PRODUCAO:
            return {"ambiente": ambiente, "autenticacao": autenticacao_habilitada()}

        if not autenticacao_habilitada():
            raise RuntimeError(
                "Produção exige PLANOS_AUTH_ENABLED=true."
            )
        obrigatorias = (
            "SUPABASE_URL",
            "SUPABASE_KEY",
            "SUPABASE_SERVICE_KEY",
        )
        ausentes = [
            nome for nome in obrigatorias
            if not os.getenv(nome, "").strip()
        ]
        if ausentes:
            raise RuntimeError(
                "Configuração de produção incompleta: "
                + ", ".join(ausentes)
                + "."
            )
        if os.getenv("SUPABASE_KEY") == os.getenv("SUPABASE_SERVICE_KEY"):
            raise RuntimeError(
                "A chave pública não pode ser a chave service_role."
            )
        return {"ambiente": ambiente, "autenticacao": True}
