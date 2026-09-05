from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class DefinicaoCategoriaResumo:
    codigo: str
    rotulo: str


@dataclass(frozen=True, slots=True)
class SalvarPrioridadeEntrada:
    tipo_entidade: str
    id_entidade: UUID | None
    prioridade: int
    ordem: int | None
    justificativa: str | None


@dataclass(frozen=True, slots=True)
class PrioridadeResumo:
    id_prioridade: UUID
    tipo_entidade: str
    id_entidade: UUID | None
    rotulo_entidade: str
    prioridade: int
    ordem: int | None
    justificativa: str | None


@dataclass(frozen=True, slots=True)
class SalvarRestricaoEntrada:
    categoria: str
    descricao: str
    entidade_afetada: str | None
    intensidade: int
    prioridade: int
    origem: str | None
    justificativa: str | None
    documento_fonte: str | None
    observacao: str | None


@dataclass(frozen=True, slots=True)
class RestricaoResumo:
    id_restricao: UUID
    categoria: str
    rotulo_categoria: str
    descricao: str
    entidade_afetada: str | None
    intensidade: int
    prioridade: int
    origem: str | None
    justificativa: str | None
    documento_fonte: str | None
    observacao: str | None
    diagnosticos: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SalvarPretensaoEntrada:
    categoria: str
    descricao_controlada: str | None
    prioridade: int
    intensidade: int
    id_publico: UUID | None
    id_praca: UUID | None
    id_etapa_jornada: UUID | None
    periodo_associado: str | None
    flexibilidade_declarada: str | None
    justificativa: str | None


@dataclass(frozen=True, slots=True)
class PretensaoResumo:
    id_pretensao: UUID
    categoria: str
    rotulo_categoria: str
    descricao_controlada: str | None
    prioridade: int
    intensidade: int
    id_publico: UUID | None
    nome_publico: str | None
    id_praca: UUID | None
    nome_praca: str | None
    id_etapa_jornada: UUID | None
    nome_etapa_jornada: str | None
    periodo_associado: str | None
    flexibilidade_declarada: str | None
    justificativa: str | None
