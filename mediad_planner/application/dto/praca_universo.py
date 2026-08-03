from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class DefinicaoTipoPracaResumo:
    codigo: str
    rotulo: str
    descricao: str


@dataclass(frozen=True, slots=True)
class DefinicaoUnidadePopulacionalResumo:
    codigo: str
    rotulo: str
    descricao: str


@dataclass(frozen=True, slots=True)
class AdicionarPracaEntrada:
    tipo: str
    nome: str
    codigo_oficial: str | None
    abrangencia: str | None
    valor_populacao_referencia: str | None
    codigo_unidade_populacional: str | None
    unidade_populacional: str | None
    fonte: str | None
    data_referencia: str | None
    observacao: str | None


@dataclass(frozen=True, slots=True)
class PracaResumo:
    id_praca: UUID
    tipo: str
    rotulo_tipo: str
    nome: str
    codigo_oficial: str | None
    abrangencia: str | None
    valor_populacao_referencia: str | None
    codigo_unidade_populacional: str | None
    unidade_populacional: str | None
    fonte: str | None
    data_referencia: str | None
    observacao: str | None


@dataclass(frozen=True, slots=True)
class AdicionarUniversoEntrada:
    nome: str
    definicao: str
    ids_pracas: tuple[UUID, ...]
    valor_populacional: str | None
    codigo_unidade: str | None
    unidade: str
    fonte: str | None
    data_referencia: str | None
    criterios_inclusao: str | None
    criterios_exclusao: str | None
    observacao: str | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "ids_pracas", tuple(self.ids_pracas))


@dataclass(frozen=True, slots=True)
class UniversoResumo:
    id_universo: UUID
    nome: str
    definicao: str
    ids_pracas: tuple[UUID, ...]
    rotulos_pracas: tuple[str, ...]
    valor_populacional: str | None
    codigo_unidade: str | None
    unidade: str
    fonte: str | None
    data_referencia: str | None
    criterios_inclusao: str | None
    criterios_exclusao: str | None
    observacao: str | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "ids_pracas", tuple(self.ids_pracas))
        object.__setattr__(self, "rotulos_pracas", tuple(self.rotulos_pracas))
