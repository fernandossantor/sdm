from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from mediad_planner.domain.common.enums import PapelAcesso


@dataclass(frozen=True, slots=True)
class ContextoAcessoCampanhas:
    id_usuario: UUID
    id_espaco_trabalho: UUID
    papel: PapelAcesso


@dataclass(frozen=True, slots=True)
class CriarCampanhaEntrada:
    nome: str
    nome_anunciante: str
    nome_marca: str | None
    nome_produto_servico: str | None
    nome_planejador_responsavel: str
    nomes_equipe: tuple[str, ...]
    observacao_inicial: str | None
    iniciar_briefing: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "nomes_equipe", tuple(self.nomes_equipe))


@dataclass(frozen=True, slots=True)
class CampanhaResumo:
    id_campanha: UUID
    codigo: str
    nome: str
    anunciante: str
    marca: str | None
    produto_servico: str | None
    planejador_responsavel: str
    equipe: tuple[str, ...]
    observacao_inicial: str | None
    situacao: str
    etapa_atual: str
    criado_em: datetime
    atualizado_em: datetime
    identificacao_completa: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "equipe", tuple(self.equipe))
