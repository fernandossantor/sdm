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


class IntervencaoHumana(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    objetivo_midia: str
    valor_calculado: str = "DERIVADO"
    valor_ajustado: str
    valor_efetivo: str
    autor: UUID
    momento: datetime
    justificativa: str
    escopo: str = "OBJETIVO_MIDIA"


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
    intervencoes_humanas: tuple[IntervencaoHumana, ...] = ()
    confianca: Confianca
    versao_regras: str
    criado_por: UUID
    criado_em: datetime


def objetivos_midia_efetivos(
    contrato: ContratoEstrategico,
) -> tuple[ObjetivoMidiaDerivado, ...]:
    estados = {
        item.objetivo_midia: item.valor_efetivo
        for item in contrato.intervencoes_humanas
    }
    return tuple(
        item for item in contrato.objetivos_midia_derivados
        if estados.get(item.categoria, "ACEITO") == "ACEITO"
    )


def revisar_traducao(
    anterior: ContratoEstrategico, *, contrato_id: UUID,
    categorias_aceitas: tuple[str, ...], justificativa: str,
    criado_por: UUID, criado_em: datetime,
) -> ContratoEstrategico:
    justificativa = justificativa.strip()
    if not justificativa:
        raise ValueError("a justificativa da revisão é obrigatória")
    calculadas = {item.categoria for item in anterior.objetivos_midia_derivados}
    aceitas = set(categorias_aceitas)
    if not aceitas.issubset(calculadas):
        raise ValueError("a revisão contém objetivo não derivado")
    anteriores = {item.categoria for item in objetivos_midia_efetivos(anterior)}
    novas_intervencoes = tuple(
        IntervencaoHumana(
            objetivo_midia=categoria,
            valor_ajustado="ACEITO" if categoria in aceitas else "REJEITADO",
            valor_efetivo="ACEITO" if categoria in aceitas else "REJEITADO",
            autor=criado_por, momento=criado_em, justificativa=justificativa,
        )
        for categoria in sorted(calculadas)
        if (categoria in anteriores) != (categoria in aceitas)
    )
    if not novas_intervencoes:
        raise ValueError("a revisão não altera nenhum objetivo")
    return anterior.model_copy(update={
        "id": contrato_id,
        "versao": anterior.versao + 1,
        "estado": (
            EstadoContratoEstrategico.PROVISORIO
            if aceitas else EstadoContratoEstrategico.PARCIAL
        ),
        "intervencoes_humanas": (
            anterior.intervencoes_humanas + novas_intervencoes
        ),
        "criado_por": criado_por,
        "criado_em": criado_em,
    })


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
