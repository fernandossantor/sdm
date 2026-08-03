from dataclasses import dataclass

from mediad_planner.domain.campanha.codigo import CodigoCampanha
from mediad_planner.domain.campanha.vinculos import (
    AnuncianteCampanha,
    MarcaCampanha,
    ParticipanteCampanha,
    ProdutoServicoCampanha,
)


@dataclass(frozen=True, slots=True)
class ContextoHerdadoBriefing:
    codigo_campanha: CodigoCampanha
    nome_campanha: str
    anunciante: AnuncianteCampanha
    marca: MarcaCampanha | None
    produto_servico: ProdutoServicoCampanha | None
    planejador_responsavel: ParticipanteCampanha
    equipe: tuple[ParticipanteCampanha, ...]

    def __post_init__(self) -> None:
        if self.codigo_campanha is None:
            raise ValueError("codigo_campanha é obrigatório")
        nome = self.nome_campanha.strip()
        if not nome:
            raise ValueError("nome_campanha não pode ser vazio")
        if self.anunciante is None:
            raise ValueError("anunciante é obrigatório")
        if self.planejador_responsavel is None:
            raise ValueError("planejador_responsavel é obrigatório")
        equipe = tuple(self.equipe)
        ids = {participante.id_usuario for participante in equipe}
        if len(ids) != len(equipe):
            raise ValueError("equipe contém IDs duplicados")
        object.__setattr__(self, "nome_campanha", nome)
        object.__setattr__(self, "equipe", equipe)
