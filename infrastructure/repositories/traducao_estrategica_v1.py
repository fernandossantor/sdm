"""Adaptador Supabase para snapshots da Traducao Estrategica v1."""

from __future__ import annotations

from typing import Any

from src.application.persistencia_traducao import RegistroPersistenciaTraducao


class RepositorioTraducaoEstrategicaSupabase:
    def __init__(self, client: Any) -> None:
        self._client = client

    def salvar(self, registro: RegistroPersistenciaTraducao) -> str:
        resposta = self._client.rpc(
            "persistir_traducao_estrategica_v1",
            {
                "p_espaco_id": registro.espaco_id,
                "p_usuario_id": registro.usuario_id,
                "p_registro": registro.conteudo_rpc(),
            },
        ).execute()
        contrato_id = resposta.data
        if not isinstance(contrato_id, str) or not contrato_id.strip():
            raise RuntimeError("Supabase nao retornou o id do contrato persistido")
        return contrato_id
