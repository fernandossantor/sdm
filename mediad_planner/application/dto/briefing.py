from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from mediad_planner.domain.common.enums import PapelAcesso


@dataclass(frozen=True, slots=True)
class ContextoAcessoBriefings:
    id_usuario: UUID
    id_espaco_trabalho: UUID
    papel: PapelAcesso


@dataclass(frozen=True, slots=True)
class AdicionarRegistroSituacaoEntrada:
    escopo: str
    codigo_aspecto: str | None
    aspecto: str
    entidade_referencia: str | None
    natureza: str
    valor_quantitativo: str | None
    unidade: str | None
    valor_qualitativo: str | None
    fonte: str | None
    periodo_referencia: str | None
    observacao: str | None


@dataclass(frozen=True, slots=True)
class RegistroSituacaoResumo:
    id_registro: UUID
    escopo: str
    codigo_aspecto: str | None
    aspecto: str
    entidade_referencia: str | None
    natureza: str
    valor_quantitativo: str | None
    unidade: str | None
    valor_qualitativo: str | None
    fonte: str | None
    periodo_referencia: str | None
    observacao: str | None


@dataclass(frozen=True, slots=True)
class AspectoSituacaoResumo:
    codigo: str
    rotulo: str
    descricao: str
    unidades_sugeridas: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "unidades_sugeridas",
            tuple(self.unidades_sugeridas),
        )


@dataclass(frozen=True, slots=True)
class BriefingResumo:
    id_briefing: UUID
    id_campanha: UUID
    numero_versao: int
    estado: str
    codigo_campanha: str
    nome_campanha: str
    anunciante: str
    marca: str | None
    produto_servico: str | None
    planejador_responsavel: str
    equipe: tuple[str, ...]
    criado_em: datetime
    atualizado_em: datetime
    registros_situacao: tuple[RegistroSituacaoResumo, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "equipe", tuple(self.equipe))
        object.__setattr__(
            self,
            "registros_situacao",
            tuple(self.registros_situacao),
        )
