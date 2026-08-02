"""Verificacao remota somente leitura, habilitada explicitamente."""

from __future__ import annotations

import os

import pytest


HABILITADO = os.getenv("RUN_TRADUCAO_SUPABASE_INTEGRATION") == "1"
VARIAVEIS_PRESENTES = bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY"))

pytestmark = pytest.mark.skipif(
    not (HABILITADO and VARIAVEIS_PRESENTES),
    reason="integracao Supabase nao habilitada ou ambiente incompleto",
)


def test_tabelas_versionadas_estao_acessiveis_por_leitura() -> None:
    from supabase import create_client

    cliente = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    tabelas = (
        "traducao_v1_campanhas",
        "traducao_v1_briefing_snapshots",
        "traducao_v1_comandos",
        "traducao_v1_execucoes",
        "traducao_v1_contratos_estrategicos",
        "traducao_v1_rastreabilidade",
    )

    for tabela in tabelas:
        resposta = cliente.table(tabela).select("id").limit(1).execute()
        assert isinstance(resposta.data, list)
