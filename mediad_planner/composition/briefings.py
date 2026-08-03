from collections.abc import Callable
from datetime import datetime
from uuid import UUID

from mediad_planner.application.dto.briefing import ContextoAcessoBriefings
from mediad_planner.application.ports.repositorio_briefings import (
    RepositorioBriefings,
)
from mediad_planner.application.ports.repositorio_campanhas import (
    RepositorioCampanhas,
)
from mediad_planner.application.services.aplicacao_briefings import (
    AplicacaoBriefings,
)
from mediad_planner.application.use_cases.briefings import (
    AbrirBriefingCampanha,
    AdicionarRegistroSituacaoMercadologica,
    ListarAspectosSituacaoMercadologica,
    RemoverRegistroSituacaoMercadologica,
)


def construir_aplicacao_briefings(
    repositorio_campanhas: RepositorioCampanhas,
    repositorio_briefings: RepositorioBriefings,
    contexto: ContextoAcessoBriefings,
    relogio: Callable[[], datetime],
    gerador_uuid: Callable[[], UUID],
) -> AplicacaoBriefings:
    abrir = AbrirBriefingCampanha(
        repositorio_campanhas=repositorio_campanhas,
        repositorio_briefings=repositorio_briefings,
        contexto_acesso=contexto,
        relogio=relogio,
        gerador_uuid=gerador_uuid,
    )
    return AplicacaoBriefings(
        abrir=abrir,
        listar_aspectos=ListarAspectosSituacaoMercadologica(),
        adicionar=AdicionarRegistroSituacaoMercadologica(
            repositorio=repositorio_briefings,
            contexto_acesso=contexto,
            relogio=relogio,
            gerador_uuid=gerador_uuid,
        ),
        remover=RemoverRegistroSituacaoMercadologica(
            repositorio=repositorio_briefings,
            contexto_acesso=contexto,
            relogio=relogio,
        ),
    )
