from dataclasses import dataclass
from uuid import UUID

from mediad_planner.application.dto.briefing import BriefingResumo
from mediad_planner.application.dto.campanha import CampanhaResumo
from mediad_planner.domain.common.enums import PapelAcesso


@dataclass(frozen=True, slots=True)
class ContextoAcessoEspacoTrabalho:
    id_usuario: UUID
    id_espaco_trabalho: UUID
    papel: PapelAcesso


@dataclass(frozen=True, slots=True)
class ModuloEspacoTrabalhoResumo:
    codigo: str
    rotulo: str
    descricao: str
    disponivel: bool
    estado: str
    motivo_bloqueio: str | None


@dataclass(frozen=True, slots=True)
class EspacoTrabalhoCampanhaResumo:
    campanha: CampanhaResumo
    briefing: BriefingResumo | None
    modulos: tuple[ModuloEspacoTrabalhoResumo, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "modulos", tuple(self.modulos))
