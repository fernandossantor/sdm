"""Primeiro contrato estratégico, paramétrico e rastreável."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from domain.briefing import BriefingInicial, EstadoBriefing
from domain.contracts import Confianca


class EstadoContratoEstrategico(str, Enum):
    PROVISORIO = "PROVISORIO"
    PARCIAL = "PARCIAL"
    INSUFICIENTE = "INSUFICIENTE"
    DEFINITIVO = "DEFINITIVO"
    SUPERADO = "SUPERADO"


class ObjetivoOperacionalizado(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    nivel: str
    categoria: str
    estado: str = "QUALITATIVO_ESTRUTURADO"
    origem: str


class ObjetivoMidiaDerivado(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    categoria: str
    origem_comunicacao: str
    regra: str
    ordem: int


class ContratoEstrategico(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    id: UUID
    campanha_id: UUID
    briefing_id: UUID
    briefing_versao: int
    versao: int = 1
    estado: EstadoContratoEstrategico
    objetivos_declarados: tuple[ObjetivoOperacionalizado, ...]
    objetivos_midia_derivados: tuple[ObjetivoMidiaDerivado, ...]
    lacunas: tuple[str, ...]
    confianca: Confianca
    versao_regras: str
    criado_por: UUID
    criado_em: datetime


MAPA_COMUNICACAO_MIDIA = {
    "notoriedade": ("construir alcance", "produzir impacto"),
    "conhecimento": ("construir alcance", "ampliar cobertura"),
    "lembrança": ("gerar frequência", "sustentar continuidade"),
    "consideração": ("gerar frequência", "ampliar cobertura"),
    "engajamento": ("gerar tráfego ou resposta",),
    "experimentação": ("apoiar conversão mensurável",),
    "ação": ("gerar tráfego ou resposta", "apoiar conversão mensurável"),
}


def traduzir_briefing(
    briefing: BriefingInicial, *, contrato_id: UUID,
    criado_por: UUID, criado_em: datetime,
) -> ContratoEstrategico:
    if briefing.estado is not EstadoBriefing.CONCLUIDO:
        raise ValueError("a tradução exige briefing concluído")
    declarados = tuple(
        ObjetivoOperacionalizado(
            nivel=nivel, categoria=item["categoria"],
            origem=f"briefing:{briefing.id}:v{briefing.versao}",
        )
        for nivel, itens in (
            ("MARKETING", briefing.conteudo.objetivos_marketing),
            ("COMUNICACAO", briefing.conteudo.objetivos_comunicacao),
        )
        for item in itens
    )
    derivados = []
    vistos = set()
    for objetivo in briefing.conteudo.objetivos_comunicacao:
        origem = objetivo["categoria"]
        for categoria in MAPA_COMUNICACAO_MIDIA.get(origem, ()):
            if categoria in vistos:
                continue
            vistos.add(categoria)
            derivados.append(ObjetivoMidiaDerivado(
                categoria=categoria, origem_comunicacao=origem,
                regra=f"MAPA_COMUNICACAO_MIDIA:{origem}",
                ordem=len(derivados) + 1,
            ))
    lacunas = []
    if not derivados:
        lacunas.append(
            "Objetivos de comunicação ainda não possuem regra de derivação versionada."
        )
    if not briefing.conteudo.fontes:
        lacunas.append("Fontes não informadas reduzem a confiança da tradução.")
    estado = (
        EstadoContratoEstrategico.PROVISORIO
        if derivados else EstadoContratoEstrategico.PARCIAL
    )
    return ContratoEstrategico(
        id=contrato_id, campanha_id=briefing.campanha_id,
        briefing_id=briefing.id, briefing_versao=briefing.versao,
        estado=estado, objetivos_declarados=declarados,
        objetivos_midia_derivados=tuple(derivados), lacunas=tuple(lacunas),
        confianca=Confianca.MEDIA if briefing.conteudo.fontes else Confianca.BAIXA,
        versao_regras="traducao-inicial-2026-08-02",
        criado_por=criado_por, criado_em=criado_em,
    )
