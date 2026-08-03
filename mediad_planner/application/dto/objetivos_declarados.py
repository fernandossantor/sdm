from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class DefinicaoObjetivoResumo:
    codigo: str
    rotulo: str
    descricao: str


@dataclass(frozen=True, slots=True)
class DimensaoCompostoMarketingResumo:
    codigo: str
    rotulo: str
    descricao: str


@dataclass(frozen=True, slots=True)
class AdicionarObjetivoMarketingEntrada:
    codigo_objetivo: str | None
    objetivo: str
    dimensoes_composto: tuple[str, ...]
    prioridade_declarada: int
    intensidade_declarada: int
    justificativa: str | None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "dimensoes_composto",
            tuple(self.dimensoes_composto),
        )


@dataclass(frozen=True, slots=True)
class AdicionarObjetivoComunicacaoEntrada:
    codigo_objetivo: str | None
    objetivo: str
    ids_objetivos_marketing_relacionados: tuple[UUID, ...]
    prioridade_declarada: int
    intensidade_declarada: int
    justificativa: str | None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "ids_objetivos_marketing_relacionados",
            tuple(self.ids_objetivos_marketing_relacionados),
        )


@dataclass(frozen=True, slots=True)
class ObjetivoMarketingResumo:
    id_objetivo: UUID
    codigo_objetivo: str | None
    objetivo: str
    dimensoes_composto: tuple[str, ...]
    rotulos_dimensoes_composto: tuple[str, ...]
    prioridade_declarada: int
    intensidade_declarada: int
    justificativa: str | None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "dimensoes_composto",
            tuple(self.dimensoes_composto),
        )
        object.__setattr__(
            self,
            "rotulos_dimensoes_composto",
            tuple(self.rotulos_dimensoes_composto),
        )


@dataclass(frozen=True, slots=True)
class ObjetivoComunicacaoResumo:
    id_objetivo: UUID
    codigo_objetivo: str | None
    objetivo: str
    ids_objetivos_marketing_relacionados: tuple[UUID, ...]
    prioridade_declarada: int
    intensidade_declarada: int
    justificativa: str | None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "ids_objetivos_marketing_relacionados",
            tuple(self.ids_objetivos_marketing_relacionados),
        )
