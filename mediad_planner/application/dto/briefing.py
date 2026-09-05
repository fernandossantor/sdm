from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from mediad_planner.application.dto.objetivos_declarados import (
    ObjetivoComunicacaoResumo,
    ObjetivoMarketingResumo,
)
from mediad_planner.application.dto.praca_universo import PracaResumo, UniversoResumo
from mediad_planner.application.dto.segmentos import SegmentoResumo
from mediad_planner.application.dto.publicos import PublicoResumo
from mediad_planner.application.dto.jornada import JornadaResumo
from mediad_planner.application.dto.periodo_verba import PeriodoVerbaResumo
from mediad_planner.application.dto.condicoes_declaradas import (
    PretensaoResumo,
    PrioridadeResumo,
    RestricaoResumo,
)
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
    objetivos_marketing: tuple[ObjetivoMarketingResumo, ...]
    objetivos_comunicacao: tuple[ObjetivoComunicacaoResumo, ...]
    pracas: tuple[PracaResumo, ...]
    universos: tuple[UniversoResumo, ...]
    criterios_segmentacao: tuple[str, ...] = ()
    segmentos: tuple[SegmentoResumo, ...] = ()
    publicos: tuple[PublicoResumo, ...] = ()
    jornadas: tuple[JornadaResumo, ...] = ()
    periodo_verba: PeriodoVerbaResumo | None = None
    prioridades_contextuais: tuple[PrioridadeResumo, ...] = ()
    restricoes: tuple[RestricaoResumo, ...] = ()
    pretensoes: tuple[PretensaoResumo, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "equipe", tuple(self.equipe))
        object.__setattr__(
            self,
            "registros_situacao",
            tuple(self.registros_situacao),
        )
        object.__setattr__(
            self,
            "objetivos_marketing",
            tuple(self.objetivos_marketing),
        )
        object.__setattr__(
            self,
            "objetivos_comunicacao",
            tuple(self.objetivos_comunicacao),
        )
        object.__setattr__(self, "pracas", tuple(self.pracas))
        object.__setattr__(self, "universos", tuple(self.universos))
        object.__setattr__(
            self, "criterios_segmentacao", tuple(self.criterios_segmentacao)
        )
        object.__setattr__(self, "segmentos", tuple(self.segmentos))
        object.__setattr__(self, "publicos", tuple(self.publicos))
        object.__setattr__(self, "jornadas", tuple(self.jornadas))
        object.__setattr__(self, "prioridades_contextuais", tuple(self.prioridades_contextuais))
        object.__setattr__(self, "restricoes", tuple(self.restricoes))
        object.__setattr__(self, "pretensoes", tuple(self.pretensoes))
