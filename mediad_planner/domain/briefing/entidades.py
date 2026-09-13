from dataclasses import dataclass, replace
from datetime import datetime
from uuid import UUID

from mediad_planner.domain.briefing.contexto import ContextoHerdadoBriefing
from mediad_planner.domain.briefing.enums import EstadoBriefing
from mediad_planner.domain.briefing.jornada import (
    EtapaJornadaDeclarada,
    JornadaDeclarada,
)
from mediad_planner.domain.briefing.periodo_verba import ContextoPeriodoVerba
from mediad_planner.domain.briefing.condicoes_declaradas import (
    PretensaoDeclarada,
    PrioridadeContextual,
    RestricaoDeclarada,
    TipoEntidadePrioridade,
)
from mediad_planner.domain.briefing.objetivos_declarados import (
    ObjetivoComunicacaoDeclarado,
    ObjetivoMarketingDeclarado,
    ObjetivosDeclarados,
)
from mediad_planner.domain.briefing.situacao_mercadologica import (
    RegistroSituacaoMercadologica,
    SituacaoMercadologicaCompetitiva,
)
from mediad_planner.domain.briefing.praca_universo import (
    CriterioSegmentacao,
    EstruturaTerritorialPopulacional,
    PracaDeclarada,
    SegmentoDeclarado,
    PublicoDeclarado,
    UniversoDeclarado,
)


def _validar_uuid(valor: object, campo: str) -> None:
    if not isinstance(valor, UUID):
        raise TypeError(f"{campo} deve ser UUID")


def _validar_fuso(valor: datetime, campo: str) -> None:
    if valor.tzinfo is None or valor.utcoffset() is None:
        raise ValueError(f"{campo} deve possuir fuso horário")


@dataclass(frozen=True, slots=True)
class Briefing:
    id_briefing: UUID
    id_campanha: UUID
    id_espaco_trabalho: UUID
    numero_versao: int
    estado: EstadoBriefing
    contexto_herdado: ContextoHerdadoBriefing
    situacao_mercadologica: SituacaoMercadologicaCompetitiva
    objetivos_declarados: ObjetivosDeclarados
    estrutura_territorial_populacional: EstruturaTerritorialPopulacional
    criado_por: UUID
    criado_em: datetime
    atualizado_por: UUID
    atualizado_em: datetime
    jornadas: tuple[JornadaDeclarada, ...] = ()
    contexto_periodo_verba: ContextoPeriodoVerba | None = None
    prioridades_contextuais: tuple[PrioridadeContextual, ...] = ()
    restricoes: tuple[RestricaoDeclarada, ...] = ()
    pretensoes: tuple[PretensaoDeclarada, ...] = ()
    restricoes_inexistentes_declaradas: bool = False

    def __post_init__(self) -> None:
        for campo in (
            "id_briefing",
            "id_campanha",
            "id_espaco_trabalho",
            "criado_por",
            "atualizado_por",
        ):
            _validar_uuid(getattr(self, campo), campo)
        if type(self.numero_versao) is not int or self.numero_versao <= 0:
            raise ValueError("numero_versao deve ser inteiro positivo")
        if self.contexto_herdado is None:
            raise ValueError("contexto_herdado é obrigatório")
        if not isinstance(
            self.situacao_mercadologica,
            SituacaoMercadologicaCompetitiva,
        ):
            raise TypeError("situacao_mercadologica inválida")
        if not isinstance(self.objetivos_declarados, ObjetivosDeclarados):
            raise TypeError("objetivos_declarados inválidos")
        if not isinstance(
            self.estrutura_territorial_populacional,
            EstruturaTerritorialPopulacional,
        ):
            raise TypeError("estrutura_territorial_populacional inválida")
        _validar_fuso(self.criado_em, "criado_em")
        _validar_fuso(self.atualizado_em, "atualizado_em")
        if self.atualizado_em < self.criado_em:
            raise ValueError("atualizado_em não pode anteceder criado_em")
        jornadas = tuple(self.jornadas)
        if any(not isinstance(item, JornadaDeclarada) for item in jornadas):
            raise TypeError("jornadas contém item inválido")
        ids_jornadas = tuple(item.id_jornada for item in jornadas)
        if len(ids_jornadas) != len(set(ids_jornadas)):
            raise ValueError("IDs de jornada duplicados")
        ids_publicos = {
            item.id_publico
            for item in self.estrutura_territorial_populacional.publicos
        }
        if any(not set(item.ids_publicos) <= ids_publicos for item in jornadas):
            raise ValueError("Público da Jornada não existe no Briefing")
        nao_aplicaveis = {
            item.id_publico for item in self.estrutura_territorial_populacional.publicos
            if item.jornada_aplicavel is False
        }
        if any(nao_aplicaveis.intersection(item.ids_publicos) for item in jornadas):
            raise ValueError(
                "Público com Jornada não aplicável não pode ter Jornada vinculada. "
                "Revise os vínculos ou a declaração de aplicabilidade."
            )
        ids_objetivos = {
            item.id_objetivo for item in self.objetivos_declarados.comunicacao
        }
        if any(
            not set(etapa.ids_objetivos_comunicacao) <= ids_objetivos
            for jornada in jornadas for etapa in jornada.etapas
        ):
            raise ValueError("Objetivo de Comunicação da Etapa não existe")
        object.__setattr__(self, "jornadas", jornadas)
        if self.contexto_periodo_verba is not None and not isinstance(
            self.contexto_periodo_verba, ContextoPeriodoVerba
        ):
            raise TypeError("contexto_periodo_verba inválido")
        prioridades = tuple(self.prioridades_contextuais)
        restricoes = tuple(self.restricoes)
        pretensoes = tuple(self.pretensoes)
        if type(self.restricoes_inexistentes_declaradas) is not bool:
            raise TypeError("restricoes_inexistentes_declaradas deve ser booleano")
        if self.restricoes_inexistentes_declaradas and restricoes:
            raise ValueError(
                "A declaração de inexistência não pode coexistir com restrições registradas. "
                "Revise os registros ou retire a declaração antes de salvar."
            )
        if any(not isinstance(item, PrioridadeContextual) for item in prioridades):
            raise TypeError("prioridades_contextuais contém item inválido")
        if any(not isinstance(item, RestricaoDeclarada) for item in restricoes):
            raise TypeError("restricoes contém item inválido")
        if any(not isinstance(item, PretensaoDeclarada) for item in pretensoes):
            raise TypeError("pretensoes contém item inválido")
        alvos = tuple((item.tipo_entidade, item.id_entidade) for item in prioridades)
        if len(alvos) != len(set(alvos)):
            raise ValueError("Entidade possui prioridade contextual duplicada")
        ids_pracas = {
            item.id_praca for item in self.estrutura_territorial_populacional.pracas
        }
        for item in self.objetivos_declarados.marketing + self.objetivos_declarados.comunicacao:
            if not set(item.ids_publicos_relacionados) <= ids_publicos:
                raise ValueError("Público relacionado ao Objetivo não existe no Briefing")
            if not set(item.ids_pracas_relacionadas) <= ids_pracas:
                raise ValueError("Praça relacionada ao Objetivo não existe no Briefing")
        ids_segmentos = {
            item.id_segmento for item in self.estrutura_territorial_populacional.segmentos
        }
        ids_etapas = {
            etapa.id_etapa for jornada in jornadas for etapa in jornada.etapas
        }
        for item in prioridades:
            if item.tipo_entidade is TipoEntidadePrioridade.PRACA and item.id_entidade not in ids_pracas:
                raise ValueError("Praça priorizada não existe")
            if item.tipo_entidade is TipoEntidadePrioridade.SEGMENTO and item.id_entidade not in ids_segmentos:
                raise ValueError("Segmento priorizado não existe")
            if item.tipo_entidade is TipoEntidadePrioridade.PERIODO and self.contexto_periodo_verba is None:
                raise ValueError("Período priorizado não existe")
        for item in pretensoes:
            if item.id_publico is not None and item.id_publico not in ids_publicos:
                raise ValueError("Público da Pretensão não existe")
            if item.id_praca is not None and item.id_praca not in ids_pracas:
                raise ValueError("Praça da Pretensão não existe")
            if item.id_etapa_jornada is not None and item.id_etapa_jornada not in ids_etapas:
                raise ValueError("Etapa da Pretensão não existe")
            if item.periodo_associado and self.contexto_periodo_verba is None:
                raise ValueError("Período da Pretensão não existe")
        object.__setattr__(self, "prioridades_contextuais", prioridades)
        object.__setattr__(self, "restricoes", restricoes)
        object.__setattr__(self, "pretensoes", pretensoes)

    @classmethod
    def criar_versao_inicial(
        cls,
        *,
        id_briefing: UUID,
        id_campanha: UUID,
        id_espaco_trabalho: UUID,
        contexto_herdado: ContextoHerdadoBriefing,
        criado_por: UUID,
        criado_em: datetime,
        atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        return cls(
            id_briefing=id_briefing,
            id_campanha=id_campanha,
            id_espaco_trabalho=id_espaco_trabalho,
            numero_versao=1,
            estado=EstadoBriefing.RASCUNHO,
            contexto_herdado=contexto_herdado,
            situacao_mercadologica=SituacaoMercadologicaCompetitiva(registros=()),
            objetivos_declarados=ObjetivosDeclarados(marketing=(), comunicacao=()),
            estrutura_territorial_populacional=EstruturaTerritorialPopulacional(
                pracas=(),
                universos=(),
            ),
            criado_por=criado_por,
            criado_em=criado_em,
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def _validar_alteracao(self, atualizado_por: UUID, atualizado_em: datetime) -> None:
        if self.estado not in (
            EstadoBriefing.RASCUNHO,
            EstadoBriefing.EM_PREENCHIMENTO,
        ):
            raise ValueError("Briefing não permite alteração neste estado")
        _validar_uuid(atualizado_por, "atualizado_por")
        _validar_fuso(atualizado_em, "atualizado_em")
        if atualizado_em < self.atualizado_em:
            raise ValueError("atualizado_em não pode regredir")

    def adicionar_registro_situacao(
        self,
        registro: RegistroSituacaoMercadologica,
        atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            situacao_mercadologica=self.situacao_mercadologica.adicionar(registro),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def adicionar_objetivo_marketing(
        self,
        objetivo: ObjetivoMarketingDeclarado,
        atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            objetivos_declarados=self.objetivos_declarados.adicionar_marketing(objetivo),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def adicionar_objetivo_comunicacao(
        self,
        objetivo: ObjetivoComunicacaoDeclarado,
        atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            objetivos_declarados=self.objetivos_declarados.adicionar_comunicacao(objetivo),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def editar_prioridade_objetivo(
        self, id_objetivo: UUID, prioridade: int, intensidade: int,
        justificativa: str | None, atualizado_por: UUID, atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            objetivos_declarados=self.objetivos_declarados.editar_prioridade(
                id_objetivo, prioridade, intensidade, justificativa,
            ),
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def definir_vinculos_objetivo(
        self, id_objetivo: UUID, ids_publicos: tuple[UUID, ...],
        ids_pracas: tuple[UUID, ...], atualizado_por: UUID, atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            objetivos_declarados=self.objetivos_declarados.definir_vinculos(
                id_objetivo, ids_publicos, ids_pracas,
            ),
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def remover_objetivo_marketing(
        self,
        id_objetivo: UUID,
        atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            objetivos_declarados=self.objetivos_declarados.remover_marketing(id_objetivo),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def remover_objetivo_comunicacao(
        self,
        id_objetivo: UUID,
        atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            objetivos_declarados=self.objetivos_declarados.remover_comunicacao(id_objetivo),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def remover_registro_situacao(
        self,
        id_registro: UUID,
        atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            situacao_mercadologica=self.situacao_mercadologica.remover(id_registro),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def adicionar_praca(
        self, praca: PracaDeclarada, atualizado_por: UUID, atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            estrutura_territorial_populacional=(
                self.estrutura_territorial_populacional.adicionar_praca(praca)
            ),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def remover_praca(
        self, id_praca: UUID, atualizado_por: UUID, atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        if any(id_praca in item.ids_pracas_relacionadas
               for item in self.objetivos_declarados.marketing + self.objetivos_declarados.comunicacao):
            raise ValueError("Praça vinculada a Objetivo não pode ser removida. Retire o vínculo no Objetivo antes de remover.")
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            estrutura_territorial_populacional=(
                self.estrutura_territorial_populacional.remover_praca(id_praca)
            ),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def adicionar_universo(
        self, universo: UniversoDeclarado, atualizado_por: UUID, atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            estrutura_territorial_populacional=(
                self.estrutura_territorial_populacional.adicionar_universo(universo)
            ),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def remover_universo(
        self, id_universo: UUID, atualizado_por: UUID, atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            estrutura_territorial_populacional=(
                self.estrutura_territorial_populacional.remover_universo(id_universo)
            ),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def definir_criterios_segmentacao(
        self,
        criterios: tuple[CriterioSegmentacao, ...],
        atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            estrutura_territorial_populacional=(
                self.estrutura_territorial_populacional
                .definir_criterios_segmentacao(criterios)
            ),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def adicionar_segmento(
        self,
        segmento: SegmentoDeclarado,
        atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            estrutura_territorial_populacional=(
                self.estrutura_territorial_populacional.adicionar_segmento(segmento)
            ),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def editar_segmento(
        self,
        segmento: SegmentoDeclarado,
        atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            estrutura_territorial_populacional=(
                self.estrutura_territorial_populacional.editar_segmento(segmento)
            ),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def remover_segmento(
        self,
        id_segmento: UUID,
        atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            estrutura_territorial_populacional=(
                self.estrutura_territorial_populacional.remover_segmento(id_segmento)
            ),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def adicionar_publico(
        self, publico: PublicoDeclarado, atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            estrutura_territorial_populacional=(
                self.estrutura_territorial_populacional.adicionar_publico(publico)
            ),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def editar_publico(
        self, publico: PublicoDeclarado, atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            estrutura_territorial_populacional=(
                self.estrutura_territorial_populacional.editar_publico(publico)
            ),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def remover_publico(
        self, id_publico: UUID, atualizado_por: UUID, atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        if any(id_publico in item.ids_publicos_relacionados
               for item in self.objetivos_declarados.marketing + self.objetivos_declarados.comunicacao):
            raise ValueError("Público vinculado a Objetivo não pode ser removido. Retire o vínculo no Objetivo antes de remover.")
        if any(id_publico in item.ids_publicos for item in self.jornadas):
            raise ValueError("Público vinculado a Jornada não pode ser removido")
        return replace(
            self,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            estrutura_territorial_populacional=(
                self.estrutura_territorial_populacional.remover_publico(id_publico)
            ),
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def adicionar_jornada(
        self, jornada: JornadaDeclarada, atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self, estado=EstadoBriefing.EM_PREENCHIMENTO,
            jornadas=self.jornadas + (jornada,), atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def definir_aplicabilidade_jornada(
        self, id_publico: UUID, aplicavel: bool | None,
        atualizado_por: UUID, atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        publico = next((
            item for item in self.estrutura_territorial_populacional.publicos
            if item.id_publico == id_publico
        ), None)
        if publico is None:
            raise LookupError("Público não encontrado")
        return self.editar_publico(
            replace(publico, jornada_aplicavel=aplicavel), atualizado_por, atualizado_em,
        )

    def editar_jornada(
        self, jornada: JornadaDeclarada, atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        if not any(item.id_jornada == jornada.id_jornada for item in self.jornadas):
            raise LookupError("Jornada não encontrada")
        jornadas = tuple(
            jornada if item.id_jornada == jornada.id_jornada else item
            for item in self.jornadas
        )
        return replace(
            self, estado=EstadoBriefing.EM_PREENCHIMENTO, jornadas=jornadas,
            atualizado_por=atualizado_por, atualizado_em=atualizado_em,
        )

    def remover_jornada(
        self, id_jornada: UUID, atualizado_por: UUID, atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        if not any(item.id_jornada == id_jornada for item in self.jornadas):
            raise LookupError("Jornada não encontrada")
        return replace(
            self, estado=EstadoBriefing.EM_PREENCHIMENTO,
            jornadas=tuple(item for item in self.jornadas if item.id_jornada != id_jornada),
            atualizado_por=atualizado_por, atualizado_em=atualizado_em,
        )

    def salvar_etapa_jornada(
        self, id_jornada: UUID, etapa: EtapaJornadaDeclarada,
        editar: bool, atualizado_por: UUID, atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        jornada = next(
            (item for item in self.jornadas if item.id_jornada == id_jornada), None
        )
        if jornada is None:
            raise LookupError("Jornada não encontrada")
        atualizada = jornada.editar_etapa(etapa) if editar else jornada.adicionar_etapa(etapa)
        return self.editar_jornada(atualizada, atualizado_por, atualizado_em)

    def remover_etapa_jornada(
        self, id_jornada: UUID, id_etapa: UUID, atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        jornada = next(
            (item for item in self.jornadas if item.id_jornada == id_jornada), None
        )
        if jornada is None:
            raise LookupError("Jornada não encontrada")
        return self.editar_jornada(
            jornada.remover_etapa(id_etapa), atualizado_por, atualizado_em
        )

    def definir_contexto_periodo_verba(
        self, contexto: ContextoPeriodoVerba, atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        if not isinstance(contexto, ContextoPeriodoVerba):
            raise TypeError("contexto inválido")
        return replace(
            self, estado=EstadoBriefing.EM_PREENCHIMENTO,
            contexto_periodo_verba=contexto, atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def _salvar_item(
        self, campo: str, item: object, id_campo: str, editar: bool,
        atualizado_por: UUID, atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        atuais = tuple(getattr(self, campo))
        identificador = getattr(item, id_campo)
        existe = any(getattr(atual, id_campo) == identificador for atual in atuais)
        if editar and not existe:
            raise LookupError("Registro não encontrado")
        if not editar and existe:
            raise ValueError("Identificador duplicado")
        novos = tuple(
            item if getattr(atual, id_campo) == identificador else atual
            for atual in atuais
        ) if editar else atuais + (item,)
        return replace(
            self, estado=EstadoBriefing.EM_PREENCHIMENTO, **{campo: novos},
            atualizado_por=atualizado_por, atualizado_em=atualizado_em,
        )

    def _remover_item(
        self, campo: str, identificador: UUID, id_campo: str,
        atualizado_por: UUID, atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        atuais = tuple(getattr(self, campo))
        if not any(getattr(item, id_campo) == identificador for item in atuais):
            raise LookupError("Registro não encontrado")
        return replace(
            self, estado=EstadoBriefing.EM_PREENCHIMENTO,
            **{campo: tuple(item for item in atuais if getattr(item, id_campo) != identificador)},
            atualizado_por=atualizado_por, atualizado_em=atualizado_em,
        )

    def salvar_prioridade(self, item, editar, atualizado_por, atualizado_em):
        return self._salvar_item("prioridades_contextuais", item, "id_prioridade", editar, atualizado_por, atualizado_em)

    def remover_prioridade(self, identificador, atualizado_por, atualizado_em):
        return self._remover_item("prioridades_contextuais", identificador, "id_prioridade", atualizado_por, atualizado_em)

    def salvar_restricao(self, item, editar, atualizado_por, atualizado_em):
        return self._salvar_item("restricoes", item, "id_restricao", editar, atualizado_por, atualizado_em)

    def definir_inexistencia_restricoes(
        self, declarada: bool, atualizado_por: UUID, atualizado_em: datetime,
    ) -> "Briefing":
        self._validar_alteracao(atualizado_por, atualizado_em)
        return replace(
            self,
            restricoes_inexistentes_declaradas=declarada,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def remover_restricao(self, identificador, atualizado_por, atualizado_em):
        return self._remover_item("restricoes", identificador, "id_restricao", atualizado_por, atualizado_em)

    def salvar_pretensao(self, item, editar, atualizado_por, atualizado_em):
        return self._salvar_item("pretensoes", item, "id_pretensao", editar, atualizado_por, atualizado_em)

    def remover_pretensao(self, identificador, atualizado_por, atualizado_em):
        return self._remover_item("pretensoes", identificador, "id_pretensao", atualizado_por, atualizado_em)
