from threading import RLock
from uuid import UUID

from mediad_planner.domain.campanha.entidades import Campanha


class RepositorioCampanhasEmMemoria:
    def __init__(self) -> None:
        self._campanhas: dict[UUID, Campanha] = {}
        self._proximo_sequencial = 1
        self._lock = RLock()

    def reservar_proximo_sequencial_global(self) -> int:
        with self._lock:
            sequencial = self._proximo_sequencial
            self._proximo_sequencial += 1
            return sequencial

    def salvar(self, campanha: Campanha) -> None:
        with self._lock:
            existente = self._campanhas.get(campanha.id_campanha)
            if existente is not None and existente.codigo != campanha.codigo:
                raise ValueError("Código da Campanha não pode ser alterado")
            if (
                existente is not None
                and existente.id_espaco_trabalho != campanha.id_espaco_trabalho
            ):
                raise ValueError("Campanha não pode mudar de espaço de trabalho")
            for outra in self._campanhas.values():
                if (
                    outra.id_campanha != campanha.id_campanha
                    and outra.codigo == campanha.codigo
                ):
                    raise ValueError("Código da Campanha já utilizado")
            self._campanhas[campanha.id_campanha] = campanha

    def obter(
        self,
        id_espaco_trabalho: UUID,
        id_campanha: UUID,
    ) -> Campanha | None:
        with self._lock:
            campanha = self._campanhas.get(id_campanha)
            if campanha is None:
                return None
            if campanha.id_espaco_trabalho != id_espaco_trabalho:
                return None
            return campanha

    def listar(
        self,
        id_espaco_trabalho: UUID,
    ) -> tuple[Campanha, ...]:
        with self._lock:
            campanhas = (
                campanha
                for campanha in self._campanhas.values()
                if campanha.id_espaco_trabalho == id_espaco_trabalho
            )
            return tuple(
                sorted(
                    campanhas,
                    key=lambda campanha: campanha.criado_em,
                    reverse=True,
                )
            )
