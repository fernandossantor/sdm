from dataclasses import dataclass, replace
from datetime import datetime
from uuid import UUID

from mediad_planner.domain.briefing.contexto import ContextoHerdadoBriefing
from mediad_planner.domain.briefing.enums import EstadoBriefing
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
    EstruturaTerritorialPopulacional,
    PracaDeclarada,
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
