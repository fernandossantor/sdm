"""Portas tipadas da fachada comum; não são motores adicionais."""

from typing import Any, Protocol, TypeVar

from domain.contracts import ComandoMotor, SaidaMotor

ComandoT = TypeVar("ComandoT", bound=ComandoMotor, contravariant=True)
SaidaT = TypeVar("SaidaT", bound=SaidaMotor, covariant=True)


class Motor(Protocol[ComandoT, SaidaT]):
    def executar(self, comando: ComandoT) -> SaidaT: ...


class ContextResolver(Protocol):
    def resolver(self, comando: ComandoMotor) -> Any: ...


class ProblemIdentifier(Protocol):
    def identificar(self, contexto: Any) -> tuple[Any, ...]: ...


class ProcedureSelector(Protocol):
    def selecionar(
        self, contexto: Any, problemas: tuple[Any, ...]
    ) -> tuple[Any, ...]: ...


class ProcedureExecutor(Protocol):
    def executar(self, procedimento: Any, contexto: Any) -> Any: ...


class ConfidenceEvaluator(Protocol):
    def avaliar(self, contexto: Any, resultados: tuple[Any, ...]) -> Any: ...


class ExplanationBuilder(Protocol):
    def construir(
        self, contexto: Any, resultados: tuple[Any, ...]
    ) -> dict[str, Any]: ...


class TraceabilityRecorder(Protocol):
    def registrar(
        self, comando: ComandoMotor, contexto: Any, resultados: tuple[Any, ...]
    ) -> Any: ...


class DependencyPlanner(Protocol):
    def planejar(self, contexto: Any, resultados: tuple[Any, ...]) -> Any: ...


class KnowledgeProvider(Protocol):
    def obter(self, codigo: str, versao: str | None = None) -> Any: ...


class ProblemCatalogProvider(Protocol):
    def obter(self, codigo: str, versao: str | None = None) -> Any: ...
