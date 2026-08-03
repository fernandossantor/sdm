from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from mediad_planner.domain.briefing.contexto import ContextoHerdadoBriefing
from mediad_planner.domain.briefing.enums import EstadoBriefing


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
            criado_por=criado_por,
            criado_em=criado_em,
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )
