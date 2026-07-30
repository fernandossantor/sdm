"""Raiz mínima do Briefing criada ao concluir a abertura da Campanha."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from domain.campanha.models import exigir_fuso


class EstadoBriefing(str, Enum):
    RASCUNHO = "RASCUNHO"


class BriefingInicial(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID
    campanha_id: UUID
    versao: int = Field(default=1, ge=1)
    estado: EstadoBriefing = EstadoBriefing.RASCUNHO
    criado_por: UUID
    criado_em: datetime

    _timestamp_com_fuso = field_validator("criado_em")(exigir_fuso)
