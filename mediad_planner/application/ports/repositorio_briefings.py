from typing import Protocol, runtime_checkable
from uuid import UUID

from mediad_planner.domain.briefing.entidades import Briefing


@runtime_checkable
class RepositorioBriefings(Protocol):
    def salvar(self, briefing: Briefing) -> None:
        ...

    def obter_por_campanha(
        self,
        id_espaco_trabalho: UUID,
        id_campanha: UUID,
    ) -> Briefing | None:
        ...
