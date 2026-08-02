"""Primeiro contrato estratégico, paramétrico e rastreável."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from domain.briefing import BriefingInicial, EstadoBriefing
from domain.contracts import Confianca, SaidaMotor


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
    indicador_codigo: str | None = None
    indicador_nome: str | None = None
    conhecimento_aplicado: str | None = None
    problema_atendido: str | None = None


class ReferenciaBibliotecaAplicada(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    biblioteca: int
    codigo: str
    versao: str


class ProblemaEstrategicoIdentificado(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    codigo: str
    estado: str
    mensagem: str


class DependenciaEstrategica(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    origem: str
    alvo: str
    recalcular_quando: tuple[str, ...]


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
    referencias_bibliotecas: tuple[ReferenciaBibliotecaAplicada, ...] = ()
    problemas_identificados: tuple[ProblemaEstrategicoIdentificado, ...] = ()
    dependencias_estrategicas: tuple[DependenciaEstrategica, ...] = ()
    execucao_motor: SaidaMotor | None = None


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


def traduzir_briefing(
    briefing: BriefingInicial, *, contrato_id: UUID,
    criado_por: UUID, criado_em: datetime, catalogo,
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
    referencias = {}
    dependencias = []
    objetivos_sem_regra = []
    for objetivo in briefing.conteudo.objetivos_comunicacao:
        origem = objetivo["categoria"]
        regra = catalogo.regra_para(origem)
        if regra is None:
            objetivos_sem_regra.append(origem)
            continue
        referencias[(regra.biblioteca, regra.codigo)] = regra
        for codigo in (regra.conhecimento_aplicado, regra.problema_atendido):
            objeto = catalogo.objeto(codigo)
            if objeto:
                referencias[(objeto.biblioteca, objeto.codigo)] = objeto
        for categoria, indicador_codigo in zip(
            regra.objetivos_midia, regra.indicadores, strict=True
        ):
            if categoria in vistos:
                continue
            vistos.add(categoria)
            indicador = catalogo.indicador(indicador_codigo)
            if indicador:
                referencias[(indicador.biblioteca, indicador.codigo)] = indicador
            derivados.append(ObjetivoMidiaDerivado(
                categoria=categoria, origem_comunicacao=origem,
                regra=regra.codigo,
                ordem=len(derivados) + 1,
                indicador_codigo=indicador_codigo,
                indicador_nome=indicador.nome if indicador else None,
                conhecimento_aplicado=regra.conhecimento_aplicado,
                problema_atendido=regra.problema_atendido,
            ))
            dependencias.append(DependenciaEstrategica(
                origem=f"objetivo_comunicacao:{origem}",
                alvo=f"objetivo_midia:{categoria}",
                recalcular_quando=(
                    "objetivo de comunicação", "público", "praça", "jornada",
                ),
            ))
    lacunas = []
    if objetivos_sem_regra:
        lacunas.append(
            "Objetivos sem regra de derivação versionada: "
            + ", ".join(objetivos_sem_regra) + "."
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
        versao_regras=catalogo.versao,
        criado_por=criado_por, criado_em=criado_em,
        referencias_bibliotecas=tuple(
            ReferenciaBibliotecaAplicada(
                biblioteca=item.biblioteca, codigo=item.codigo,
                versao=item.versao,
            ) for item in referencias.values()
        ),
        problemas_identificados=(
            (ProblemaEstrategicoIdentificado(
                codigo="B18-DERIVAR-OBJETIVO-MIDIA",
                estado="PARCIAL" if objetivos_sem_regra else "CONCLUIDO",
                mensagem=(
                    "Derivação incompleta para parte dos objetivos."
                    if objetivos_sem_regra else
                    "Objetivos de mídia derivados com regra versionada."
                ),
            ),) if briefing.conteudo.objetivos_comunicacao else ()
        ),
        dependencias_estrategicas=tuple(dependencias),
    )
