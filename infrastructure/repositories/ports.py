"""Portas de persistência; implementações permanecem na infraestrutura."""

from typing import Any, Protocol
from uuid import UUID


class RepositorioPorId(Protocol):
    def obter(self, id_objeto: UUID) -> Any | None: ...

    def salvar(self, objeto: Any) -> Any: ...


class CampanhaRepository(RepositorioPorId, Protocol): ...


class SnapshotRepository(RepositorioPorId, Protocol): ...


class ComandoRepository(RepositorioPorId, Protocol): ...


class ExecucaoRepository(RepositorioPorId, Protocol): ...


class ResultadoRepository(RepositorioPorId, Protocol): ...


class BibliotecaVersionadaRepository(RepositorioPorId, Protocol): ...


class ConhecimentoTecnicoRepository(RepositorioPorId, Protocol): ...


class ProblemaTecnicoRepository(RepositorioPorId, Protocol): ...
