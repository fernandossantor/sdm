from mediad_planner.application.dto.espaco_trabalho import (
    ContextoAcessoEspacoTrabalho,
)
from mediad_planner.application.ports.repositorio_briefings import (
    RepositorioBriefings,
)
from mediad_planner.application.ports.repositorio_campanhas import (
    RepositorioCampanhas,
)
from mediad_planner.application.services.aplicacao_espaco_trabalho import (
    AplicacaoEspacoTrabalho,
)
from mediad_planner.application.use_cases.espaco_trabalho import (
    ObterEspacoTrabalhoCampanha,
    PrepararBriefingCampanha,
)
from mediad_planner.application.use_cases.briefings import AbrirBriefingCampanha
from mediad_planner.application.use_cases.campanhas import IniciarBriefingCampanha


def construir_aplicacao_espaco_trabalho(
    repositorio_campanhas: RepositorioCampanhas,
    repositorio_briefings: RepositorioBriefings,
    contexto: ContextoAcessoEspacoTrabalho,
    iniciar_briefing: IniciarBriefingCampanha,
    abrir_briefing: AbrirBriefingCampanha,
) -> AplicacaoEspacoTrabalho:
    obter = ObterEspacoTrabalhoCampanha(
        repositorio_campanhas=repositorio_campanhas,
        repositorio_briefings=repositorio_briefings,
        contexto_acesso=contexto,
    )
    return AplicacaoEspacoTrabalho(
        obter=obter,
        preparar=PrepararBriefingCampanha(
            iniciar_briefing=iniciar_briefing,
            abrir_briefing=abrir_briefing,
            obter_espaco_trabalho=obter,
        ),
    )
