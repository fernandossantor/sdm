from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from mediad_planner.application.dto.briefing import ContextoAcessoBriefings
from mediad_planner.application.dto.campanha import ContextoAcessoCampanhas
from mediad_planner.application.services.aplicacao_briefings import (
    AplicacaoBriefings,
)
from mediad_planner.application.services.aplicacao_campanhas import (
    AplicacaoCampanhas,
)
from mediad_planner.application.use_cases.campanhas import (
    CriarCampanha,
    IniciarBriefingCampanha,
    ListarCampanhas,
)
from mediad_planner.composition.briefings import construir_aplicacao_briefings
from mediad_planner.domain.common.enums import PapelAcesso
from mediad_planner.infrastructure.repositories.briefings_em_memoria import (
    RepositorioBriefingsEmMemoria,
)
from mediad_planner.infrastructure.repositories.campanhas_em_memoria import (
    RepositorioCampanhasEmMemoria,
)


@dataclass(frozen=True, slots=True)
class AmbienteAplicacao:
    campanhas: AplicacaoCampanhas
    briefings: AplicacaoBriefings


def construir_ambiente_aplicacao_em_memoria() -> AmbienteAplicacao:
    repositorio_campanhas = RepositorioCampanhasEmMemoria()
    repositorio_briefings = RepositorioBriefingsEmMemoria()
    id_usuario = UUID("00000000-0000-0000-0000-000000000001")
    id_espaco = UUID("00000000-0000-0000-0000-000000000002")
    contexto_campanhas = ContextoAcessoCampanhas(
        id_usuario=id_usuario,
        id_espaco_trabalho=id_espaco,
        papel=PapelAcesso.EDITOR,
    )
    contexto_briefings = ContextoAcessoBriefings(
        id_usuario=id_usuario,
        id_espaco_trabalho=id_espaco,
        papel=PapelAcesso.EDITOR,
    )

    def relogio() -> datetime:
        return datetime.now(timezone.utc)

    campanhas = AplicacaoCampanhas(
        criar=CriarCampanha(
            repositorio_campanhas,
            contexto_campanhas,
            relogio,
            uuid4,
        ),
        iniciar_briefing=IniciarBriefingCampanha(
            repositorio_campanhas,
            contexto_campanhas,
            relogio,
        ),
        listar=ListarCampanhas(repositorio_campanhas, contexto_campanhas),
    )
    briefings = construir_aplicacao_briefings(
        repositorio_campanhas=repositorio_campanhas,
        repositorio_briefings=repositorio_briefings,
        contexto=contexto_briefings,
        relogio=relogio,
        gerador_uuid=uuid4,
    )
    return AmbienteAplicacao(campanhas=campanhas, briefings=briefings)
