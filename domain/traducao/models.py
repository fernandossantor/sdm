"""Primeiro contrato estratégico, paramétrico e rastreável."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

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
    pontuacao_contextual: float | None = Field(default=None, ge=0, le=100)
    ordem_contextual: int | None = Field(default=None, ge=1)
    prioridade_calculada: str | None = None
    explicacao_decisoria: str | None = None


class ContribuicaoRelacao(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    dimensao: str
    valor: float = Field(ge=0, le=100)
    peso: float = Field(gt=0, le=1)
    contribuicao: float = Field(ge=0, le=100)
    explicacao: str


class PenalizacaoRelacao(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    dimensao: str
    valor: float = Field(gt=0, le=100)
    explicacao: str


class FatorDiagnostico(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    dimensao: str
    valor: str
    origem: str
    influencia_em: tuple[str, ...] = ()


class RelacaoEstrategica(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    origem_nivel: str
    origem: str
    destino_nivel: str
    destino: str
    tipo: str
    estado: str = "QUALITATIVA_SEM_FORMULA"
    justificativa: str
    regra: str
    forca_padrao: float | None = Field(default=None, ge=0, le=100)
    pontuacao_contextual: float | None = Field(default=None, ge=0, le=100)
    ordem_contextual: int | None = Field(default=None, ge=1)
    condicao: str | None = None
    contribuicoes: tuple[ContribuicaoRelacao, ...] = ()
    penalizacoes: tuple[PenalizacaoRelacao, ...] = ()
    confianca: Confianca | None = None
    explicacao_decisoria: str | None = None
    efeito_etapa_seguinte: str | None = None


class ContextoPriorizado(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    dimensao: str
    valor: str
    prioridade: str
    origem: str
    influencia_em: tuple[str, ...]


class ResultadoIndicadorEstrategico(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    objetivo_midia: str
    resultado_pretendido: str
    indicador_codigo: str | None = None
    indicador_nome: str | None = None
    estado_mensuracao: str = "META_E_LINHA_DE_BASE_PENDENTES"


class CriterioArquitetura(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    criterio: str
    condicao: str
    prioridade: str
    origens: tuple[str, ...]
    limita_decisoes: bool = False


class TensaoEstrategica(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    tensao: str
    gravidade: str
    evidencias: tuple[str, ...]
    decisao_requerida: str


class ConfiancaDetalhada(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    nivel: Confianca
    fatores_positivos: tuple[str, ...] = ()
    fatores_redutores: tuple[str, ...] = ()


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
    natureza: str = "CALCULADO"
    pontuacao_contextual: float | None = Field(default=None, ge=0, le=100)
    prioridade_calculada: str | None = None
    peso_calculado: float | None = Field(default=None, ge=0, le=1)
    peso_ajustado: float | None = Field(default=None, ge=0, le=1)
    peso_efetivo: float | None = Field(default=None, ge=0, le=1)
    intensidade_requerida: str | None = None
    efeito_na_arquitetura: str | None = None
    confianca: Confianca | None = None
    explicacao_peso: str | None = None


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
    diagnostico: tuple[FatorDiagnostico, ...] = ()
    relacoes_estrategicas: tuple[RelacaoEstrategica, ...] = ()
    contexto_priorizado: tuple[ContextoPriorizado, ...] = ()
    resultados_indicadores: tuple[ResultadoIndicadorEstrategico, ...] = ()
    criterios_arquitetura: tuple[CriterioArquitetura, ...] = ()
    tensoes: tuple[TensaoEstrategica, ...] = ()
    confianca_detalhada: ConfiancaDetalhada | None = None
    versao_composicao: str | None = None


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
    criado_por: UUID, criado_em: datetime, catalogo,
) -> ContratoEstrategico:
    justificativa = justificativa.strip()
    if not justificativa:
        raise ValueError("a justificativa da revisão é obrigatória")
    calculadas = {item.categoria for item in anterior.objetivos_midia_derivados}
    aceitas = set(categorias_aceitas)
    disponiveis = {item.nome for item in catalogo.objetivos_midia()}
    if not aceitas.issubset(disponiveis):
        raise ValueError("a revisão contém objetivo fora da Biblioteca 15")
    anteriores = {item.categoria for item in objetivos_midia_efetivos(anterior)}
    adicionadas = aceitas - calculadas
    novos_objetivos = []
    novas_referencias = list(anterior.referencias_bibliotecas)
    novas_dependencias = list(anterior.dependencias_estrategicas)
    for categoria in sorted(adicionadas):
        objetivo = catalogo.objetivo_midia(categoria)
        indicador = catalogo.indicador(objetivo.indicador_codigo)
        novos_objetivos.append(ObjetivoMidiaDerivado(
            categoria=categoria, origem_comunicacao="INTERVENCAO_HUMANA",
            regra="AJUSTE_HUMANO_JUSTIFICADO",
            ordem=len(anterior.objetivos_midia_derivados) + len(novos_objetivos) + 1,
            indicador_codigo=objetivo.indicador_codigo,
            indicador_nome=indicador.nome if indicador else None,
            natureza="AJUSTADO_PELO_USUARIO",
        ))
        for item in (objetivo, indicador):
            if item and not any(
                ref.codigo == item.codigo for ref in novas_referencias
            ):
                novas_referencias.append(ReferenciaBibliotecaAplicada(
                    biblioteca=item.biblioteca, codigo=item.codigo,
                    versao=item.versao,
                ))
        novas_dependencias.append(DependenciaEstrategica(
            origem="intervencao_humana",
            alvo=f"objetivo_midia:{categoria}",
            recalcular_quando=("justificativa", "contexto estratégico"),
        ))
    novas_intervencoes = tuple(
        IntervencaoHumana(
            objetivo_midia=categoria,
            valor_calculado=(
                "NAO_DERIVADO" if categoria in adicionadas else "DERIVADO"
            ),
            valor_ajustado="ACEITO" if categoria in aceitas else "REJEITADO",
            valor_efetivo="ACEITO" if categoria in aceitas else "REJEITADO",
            autor=criado_por, momento=criado_em, justificativa=justificativa,
        )
        for categoria in sorted(calculadas | adicionadas)
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
        "objetivos_midia_derivados": (
            anterior.objetivos_midia_derivados + tuple(novos_objetivos)
        ),
        "referencias_bibliotecas": tuple(novas_referencias),
        "dependencias_estrategicas": tuple(novas_dependencias),
        "criado_por": criado_por,
        "criado_em": criado_em,
    })


def _traduzir_briefing_qualitativo(
    briefing: BriefingInicial, *, contrato_id: UUID,
    criado_por: UUID, criado_em: datetime, catalogo,
) -> ContratoEstrategico:
    if briefing.estado is not EstadoBriefing.CONCLUIDO:
        raise ValueError("a tradução exige briefing concluído")
    origem_briefing = f"briefing:{briefing.id}:v{briefing.versao}"
    declarados = tuple(
        ObjetivoOperacionalizado(
            nivel=nivel, categoria=item["categoria"],
            origem=origem_briefing,
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
    for objeto in catalogo.referencias_contexto(briefing):
        referencias[(objeto.biblioteca, objeto.codigo)] = objeto
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
            objetivo_midia = catalogo.objetivo_midia(categoria)
            if indicador:
                referencias[(indicador.biblioteca, indicador.codigo)] = indicador
            if objetivo_midia:
                referencias[(
                    objetivo_midia.biblioteca, objetivo_midia.codigo
                )] = objetivo_midia
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
    relacoes_mc = []
    for marketing in briefing.conteudo.objetivos_marketing:
        origem = marketing["categoria"]
        destinos = catalogo.comunicacao_para_marketing(origem)
        for comunicacao in briefing.conteudo.objetivos_comunicacao:
            destino = comunicacao["categoria"]
            if destino.casefold() in destinos:
                relacoes_mc.append(RelacaoEstrategica(
                    origem_nivel="MARKETING", origem=origem,
                    destino_nivel="COMUNICACAO", destino=destino,
                    tipo="CONTRIBUICAO", justificativa=(
                        f"{destino} é resposta aplicável a {origem}."
                    ), regra=f"B15-MC-{origem.upper().replace(' ', '-')}",
                ))
    relacoes_cm = tuple(RelacaoEstrategica(
        origem_nivel="COMUNICACAO", origem=item.origem_comunicacao,
        destino_nivel="MIDIA", destino=item.categoria,
        tipo="DERIVACAO", justificativa=(
            f"{item.categoria} cria condição para {item.origem_comunicacao}."
        ), regra=item.regra,
    ) for item in derivados)
    if briefing.conteudo.relacoes_objetivos and not relacoes_mc:
        lacunas.append(
            "Não há relação Marketing–Comunicação validada para os objetivos declarados."
        )
    situacao = briefing.conteudo.situacao_mercadologica
    diagnostico = tuple(FatorDiagnostico(
        dimensao=dimensao, valor=str(situacao.get(campo, "não informado")),
        origem=origem_briefing, influencia_em=influencias,
    ) for dimensao, campo, influencias in (
        ("Tendência do mercado", "tendencia_mercado", ("prioridade", "continuidade")),
        ("Ciclo de vida", "ciclo_vida", ("objetivos", "resultados")),
        ("Pressão competitiva", "intensidade_competitiva", ("frequência", "impacto", "continuidade")),
    ))
    niveis = {item.get("entidade"): item.get("nivel", "não ordenada")
              for item in briefing.conteudo.prioridades}
    contexto = []
    for dimensao, itens, campo, entidade, influencia in (
        ("Praça", briefing.conteudo.pracas, "nome", "praças", ("cobertura", "presença territorial")),
        ("Segmento", briefing.conteudo.segmentos, "nome", "segmentos", ("afinidade", "alcance")),
        ("Público", briefing.conteudo.publicos, "nome", "públicos", ("alcance", "afinidade")),
        ("Jornada", briefing.conteudo.jornadas, "etapa", "jornada", ("continuidade", "resposta")),
    ):
        contexto.extend(ContextoPriorizado(
            dimensao=dimensao, valor=str(item.get(campo, "—")),
            prioridade=niveis.get(entidade, "não ordenada"),
            origem=origem_briefing, influencia_em=influencia,
        ) for item in itens)
    pretensoes = tuple(item.get("categoria", "resultado não especificado")
                       for item in briefing.conteudo.pretensoes) or ("resultado a formalizar",)
    resultados = tuple(ResultadoIndicadorEstrategico(
        objetivo_midia=item.categoria,
        resultado_pretendido=pretensoes[min(indice, len(pretensoes) - 1)],
        indicador_codigo=item.indicador_codigo,
        indicador_nome=item.indicador_nome,
    ) for indice, item in enumerate(derivados))
    criterios = [CriterioArquitetura(
        criterio=f"Favorecer {item.categoria}",
        condicao=f"Responder a {item.origem_comunicacao}",
        prioridade=f"ordem qualitativa {item.ordem}",
        origens=(f"objetivo_comunicacao:{item.origem_comunicacao}", item.regra),
    ) for item in derivados]
    criterios.extend(CriterioArquitetura(
        criterio=f"Respeitar restrição {item.get('categoria', 'declarada')}",
        condicao="Limite obrigatório para a arquitetura posterior",
        prioridade="obrigatória", origens=(origem_briefing,),
        limita_decisoes=True,
    ) for item in briefing.conteudo.restricoes)
    pressao = str(situacao.get("intensidade_competitiva", "não informado"))
    tensoes = []
    if pressao in {"alta", "muito alta"}:
        tensoes.append(TensaoEstrategica(
            tensao="Pressão competitiva exige resposta de mídia",
            gravidade="alta" if pressao == "muito alta" else "média",
            evidencias=(f"pressão competitiva:{pressao}",),
            decisao_requerida="Conciliar impacto, frequência e continuidade com a verba.",
        ))
        criterios.append(CriterioArquitetura(
            criterio="Responder à pressão competitiva",
            condicao="Elevar impacto, frequência ou continuidade sem definir canal",
            prioridade="alta", origens=("diagnostico:pressao_competitiva",),
        ))
    fatores_positivos = tuple(filter(None, (
        "objetivos declarados" if declarados else None,
        "fontes declaradas" if briefing.conteudo.fontes else None,
        "contexto identificável" if contexto else None,
    )))
    fatores_redutores = tuple(filter(None, (
        "fontes ausentes" if not briefing.conteudo.fontes else None,
        "metas e linhas de base não formalizadas" if resultados else None,
        "relação Marketing–Comunicação não validada" if not relacoes_mc else None,
    )))
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
        diagnostico=diagnostico,
        relacoes_estrategicas=tuple(relacoes_mc) + relacoes_cm,
        contexto_priorizado=tuple(contexto),
        resultados_indicadores=resultados,
        criterios_arquitetura=tuple(criterios),
        tensoes=tuple(tensoes),
        confianca_detalhada=ConfiancaDetalhada(
            nivel=Confianca.MEDIA if briefing.conteudo.fontes else Confianca.BAIXA,
            fatores_positivos=fatores_positivos,
            fatores_redutores=fatores_redutores,
        ),
    )


def traduzir_briefing(
    briefing: BriefingInicial, *, contrato_id: UUID,
    criado_por: UUID, criado_em: datetime, catalogo,
) -> ContratoEstrategico:
    from .pontuacao import aplicar_pontuacao

    qualitativo = _traduzir_briefing_qualitativo(
        briefing, contrato_id=contrato_id, criado_por=criado_por,
        criado_em=criado_em, catalogo=catalogo,
    )
    return aplicar_pontuacao(qualitativo, briefing, catalogo)
