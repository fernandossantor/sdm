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
    sem_restricoes_declaradas: bool = False
    pretensoes: tuple[dict[str, Any], ...] = ()
    fontes: tuple[dict[str, Any], ...] = ()
    jornada_aplicavel: bool | None = None


class AvaliacaoBriefing(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    percentual_completude: int = Field(ge=0, le=100)
    pendencias: tuple[str, ...] = ()
    alertas: tuple[str, ...] = ()

    @property
    def apto_para_revisao(self) -> bool:
        return not self.pendencias


def avaliar_briefing(conteudo: ConteudoBriefing) -> AvaliacaoBriefing:
    """Avalia suficiência mínima sem alterar declarações do usuário."""

    criterios = (
        (bool(conteudo.situacao_mercadologica.get("descricao", "").strip()),
         "Registre a situação mercadológica e competitiva."),
        (bool(conteudo.objetivos_marketing),
         "Selecione ao menos um objetivo de marketing."),
        (bool(conteudo.objetivos_comunicacao),
         "Selecione ao menos um objetivo de comunicação."),
        (bool(conteudo.relacoes_objetivos),
         "Explique a relação entre os objetivos declarados."),
        (bool(conteudo.pracas), "Registre ao menos uma praça."),
        (bool(conteudo.universos), "Registre o universo correspondente."),
        (bool(conteudo.segmentos), "Registre ao menos um segmento."),
        (bool(conteudo.publicos), "Registre ao menos um público."),
        (
            conteudo.jornada_aplicavel is False or bool(conteudo.jornadas),
            "Registre a jornada ou declare que ela não é aplicável.",
        ),
        (
            bool(conteudo.periodo.get("inicio"))
            and bool(conteudo.periodo.get("fim")),
            "Informe o período pretendido.",
        ),
        (
            conteudo.verba.get("natureza") == "ainda não definido"
            or float(conteudo.verba.get("valor_total") or 0) > 0,
            "Informe a verba ou declare que ainda não está definida.",
        ),
        (bool(conteudo.prioridades), "Registre as prioridades mínimas."),
        (
            conteudo.sem_restricoes_declaradas or bool(conteudo.restricoes),
            "Registre restrições ou declare que não existem.",
        ),
        (bool(conteudo.pretensoes), "Registre ao menos uma pretensão."),
    )
    pendencias = tuple(mensagem for valido, mensagem in criterios if not valido)
    alertas = []
    if conteudo.objetivos_marketing and conteudo.objetivos_comunicacao:
        if not conteudo.relacoes_objetivos:
            alertas.append("Objetivos ainda não possuem relação explícita.")
    if conteudo.verba.get("natureza") == "ainda não definido":
        alertas.append("A verba ainda não está definida.")
    percentual = round(
        100 * (len(criterios) - len(pendencias)) / len(criterios)
    )
    return AvaliacaoBriefing(
        percentual_completude=percentual,
        pendencias=pendencias,
        alertas=tuple(alertas),
    )


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
