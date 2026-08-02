"""Porta de persistencia da primeira versao da Traducao Estrategica."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol


Snapshot = Mapping[str, Any]


@dataclass(frozen=True)
class RegistroPersistenciaTraducao:
    """Snapshot completo que deve ser gravado atomicamente."""

    espaco_id: str
    usuario_id: str
    campanha: Snapshot
    briefing_snapshot: Snapshot
    comando: Snapshot
    execucao: Snapshot
    contrato: Snapshot
    rastreabilidade: tuple[Snapshot, ...]

    def conteudo_rpc(self) -> dict[str, Any]:
        return {
            "campanha": dict(self.campanha),
            "briefing_snapshot": dict(self.briefing_snapshot),
            "comando": dict(self.comando),
            "execucao": dict(self.execucao),
            "contrato": dict(self.contrato),
            "rastreabilidade": [dict(item) for item in self.rastreabilidade],
        }


class RepositorioTraducaoEstrategica(Protocol):
    """Porta abstrata; o motor e seus modelos nao dependem do Supabase."""

    def salvar(self, registro: RegistroPersistenciaTraducao) -> str:
        """Persiste o registro atomicamente e devolve o id do contrato."""
        ...
