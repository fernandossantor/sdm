from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CategoriaEtapaJornadaResumo:
    codigo: str
    rotulo: str


@dataclass(frozen=True, slots=True)
class SalvarJornadaEntrada:
    nome: str
    descricao: str | None
    ids_publicos: tuple[UUID, ...]
    referencia_modelo: str | None
    adaptada_localmente: bool


@dataclass(frozen=True, slots=True)
class SalvarEtapaJornadaEntrada:
    categoria: str
    ordem: int | None
    existe: bool
    relevancia: int | None
    intensidade: int | None
    prioridade: int | None
    ids_publicos: tuple[UUID, ...]
    ids_objetivos_comunicacao: tuple[UUID, ...]
    situacao_atual: str | None
    situacao_pretendida: str | None
    observacao: str | None


@dataclass(frozen=True, slots=True)
class EtapaJornadaResumo:
    id_etapa: UUID
    categoria: str
    rotulo_categoria: str
    ordem: int | None
    existe: bool
    relevancia: int | None
    intensidade: int | None
    prioridade: int | None
    ids_publicos: tuple[UUID, ...]
    nomes_publicos: tuple[str, ...]
    ids_objetivos_comunicacao: tuple[UUID, ...]
    nomes_objetivos_comunicacao: tuple[str, ...]
    situacao_atual: str | None
    situacao_pretendida: str | None
    observacao: str | None


@dataclass(frozen=True, slots=True)
class JornadaResumo:
    id_jornada: UUID
    nome: str
    descricao: str | None
    ids_publicos: tuple[UUID, ...]
    nomes_publicos: tuple[str, ...]
    referencia_modelo: str | None
    adaptada_localmente: bool
    etapas: tuple[EtapaJornadaResumo, ...]
