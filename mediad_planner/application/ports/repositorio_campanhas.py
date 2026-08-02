from typing import Protocol, runtime_checkable
from uuid import UUID

from mediad_planner.domain.campanha.entidades import Campanha


@runtime_checkable
class RepositorioCampanhas(Protocol):
    def reservar_proximo_sequencial_global(self) -> int:
        ...

    def salvar(self, campanha: Campanha) -> None:
        ...

    def obter(
        self,
        id_espaco_trabalho: UUID,
        id_campanha: UUID,
    ) -> Campanha | None:
        ...

    def listar(
        self,
        id_espaco_trabalho: UUID,
    ) -> tuple[Campanha, ...]:
        ...
