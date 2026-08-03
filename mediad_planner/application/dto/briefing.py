from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from mediad_planner.domain.common.enums import PapelAcesso


@dataclass(frozen=True, slots=True)
class ContextoAcessoBriefings:
    id_usuario: UUID
    id_espaco_trabalho: UUID
    papel: PapelAcesso


@dataclass(frozen=True, slots=True)
class BriefingResumo:
    id_briefing: UUID
    id_campanha: UUID
    numero_versao: int
    estado: str
    codigo_campanha: str
    nome_campanha: str
    anunciante: str
    marca: str | None
    produto_servico: str | None
    planejador_responsavel: str
    equipe: tuple[str, ...]
    criado_em: datetime
    atualizado_em: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "equipe", tuple(self.equipe))
