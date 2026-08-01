"""Entradas dos casos de uso do Briefing canônico."""

from dataclasses import dataclass
from uuid import UUID

from domain.briefing import ConteudoBriefing


@dataclass(frozen=True)
class EditarBriefingEntrada:
    briefing_id: UUID
    usuario_id: UUID
    conteudo: ConteudoBriefing
    motivo: str


@dataclass(frozen=True)
class CriarVersaoBriefingEntrada:
    briefing_id_origem: UUID
    usuario_id: UUID
    conteudo: ConteudoBriefing
    motivo: str


@dataclass(frozen=True)
class TransicionarBriefingEntrada:
    briefing_id: UUID
    usuario_id: UUID
    motivo: str
    alertas_reconhecidos: tuple[str, ...] = ()
