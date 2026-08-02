from datetime import datetime, timezone
from uuid import UUID, uuid4

from mediad_planner.application.dto.campanha import ContextoAcessoCampanhas
from mediad_planner.application.services.aplicacao_campanhas import (
    AplicacaoCampanhas,
)
from mediad_planner.application.use_cases.campanhas import (
    CriarCampanha,
    IniciarBriefingCampanha,
    ListarCampanhas,
)
from mediad_planner.domain.common.enums import PapelAcesso
from mediad_planner.infrastructure.repositories.campanhas_em_memoria import (
    RepositorioCampanhasEmMemoria,
)


def construir_aplicacao_campanhas_em_memoria() -> AplicacaoCampanhas:
    repositorio = RepositorioCampanhasEmMemoria()
    contexto = ContextoAcessoCampanhas(
        id_usuario=UUID("00000000-0000-0000-0000-000000000001"),
        id_espaco_trabalho=UUID("00000000-0000-0000-0000-000000000002"),
        papel=PapelAcesso.EDITOR,
    )
    relogio = lambda: datetime.now(timezone.utc)
    criar = CriarCampanha(repositorio, contexto, relogio, uuid4)
    iniciar = IniciarBriefingCampanha(repositorio, contexto, relogio)
    listar = ListarCampanhas(repositorio, contexto)
    return AplicacaoCampanhas(criar, iniciar, listar)
