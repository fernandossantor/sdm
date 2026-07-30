"""DTOs da primeira fatia de Campanha/Briefing."""

from dataclasses import dataclass
from uuid import UUID

from domain.briefing import BriefingInicial
from domain.campanha import Campanha


@dataclass(frozen=True)
class AbrirCampanhaEntrada:
    nome: str
    anunciante_id: UUID
    nome_anunciante: str
    planejador_responsavel_id: UUID
    identificacao_planejador: str
    criado_por: UUID
    marca_id: UUID | None = None
    nome_marca: str | None = None
    produto_servico_id: UUID | None = None
    nome_produto_servico: str | None = None
    equipe_ids: tuple[UUID, ...] = ()
    observacao_inicial: str | None = None
    campanha_derivada_de_id: UUID | None = None


@dataclass(frozen=True)
class AberturaCampanhaSaida:
    campanha: Campanha
    habilita_inicio_briefing: bool = True


@dataclass(frozen=True)
class IniciarBriefingEntrada:
    campanha_id: UUID
    usuario_id: UUID


@dataclass(frozen=True)
class InicioBriefingSaida:
    campanha: Campanha
    briefing: BriefingInicial
