"""Configuração central sem criação automática de cliente ou exposição de secrets."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class SupabaseSettings:
    url: str
    anon_key: str
    service_role_key: str | None = None

    @classmethod
    def from_environment(cls, *, administrative: bool = False) -> "SupabaseSettings":
        url = os.getenv("SUPABASE_URL", "").strip()
        anon_key = os.getenv("SUPABASE_KEY", "").strip()
        service_key = os.getenv("SUPABASE_SERVICE_KEY", "").strip() or None
        ausentes = [
            nome
            for nome, valor in (("SUPABASE_URL", url), ("SUPABASE_KEY", anon_key))
            if not valor
        ]
        if administrative and not service_key:
            ausentes.append("SUPABASE_SERVICE_KEY")
        if ausentes:
            raise RuntimeError(
                "Configuração Supabase incompleta; variáveis ausentes: "
                + ", ".join(ausentes)
            )
        return cls(url=url, anon_key=anon_key, service_role_key=service_key)

    def safe_status(self) -> dict[str, bool]:
        """Retorna apenas presença, nunca os valores sensíveis."""
        return {
            "SUPABASE_URL": bool(self.url),
            "SUPABASE_KEY": bool(self.anon_key),
            "SUPABASE_SERVICE_KEY": bool(self.service_role_key),
        }
