"""Objeto contextual estruturado e versionado do Briefing de Mídia."""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from domain.campanha.models import exigir_fuso


class EstadoBriefing(str, Enum):
    RASCUNHO = "RASCUNHO"
    EM_PREENCHIMENTO = "EM_PREENCHIMENTO"
    EM_REVISAO = "EM_REVISAO"
    CONCLUIDO = "CONCLUIDO"
    SUBSTITUIDO = "SUBSTITUIDO"


class ConteudoBriefing(BaseModel):
    """Conteúdo metodológico; o contexto administrativo fica na Campanha."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    situacao_mercadologica: dict[str, Any] = Field(default_factory=dict)
    objetivos_marketing: tuple[dict[str, Any], ...] = ()
    objetivos_comunicacao: tuple[dict[str, Any], ...] = ()
    relacoes_objetivos: tuple[dict[str, Any], ...] = ()
    pracas: tuple[dict[str, Any], ...] = ()
    universos: tuple[dict[str, Any], ...] = ()
    criterios_segmentacao: tuple[str, ...] = ()
    segmentos: tuple[dict[str, Any], ...] = ()
    publicos: tuple[dict[str, Any], ...] = ()
    jornadas: tuple[dict[str, Any], ...] = ()
    periodo: dict[str, Any] = Field(default_factory=dict)
    verba: dict[str, Any] = Field(default_factory=dict)
    prioridades: tuple[dict[str, Any], ...] = ()
    restricoes: tuple[dict[str, Any], ...] = ()
    pretensoes: tuple[dict[str, Any], ...] = ()
    fontes: tuple[dict[str, Any], ...] = ()


class BriefingInicial(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID
    campanha_id: UUID
    versao: int = Field(default=1, ge=1)
    estado: EstadoBriefing = EstadoBriefing.RASCUNHO
    criado_por: UUID
    criado_em: datetime
    conteudo: ConteudoBriefing = Field(default_factory=ConteudoBriefing)
    atualizado_por: UUID | None = None
    atualizado_em: datetime | None = None
    motivo_ultima_alteracao: str | None = None

    _timestamp_com_fuso = field_validator("criado_em")(exigir_fuso)

    @field_validator("atualizado_em")
    @classmethod
    def _atualizacao_com_fuso(cls, valor):
        return exigir_fuso(valor) if valor is not None else valor
