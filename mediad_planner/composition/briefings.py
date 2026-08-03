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
from mediad_planner.application.use_cases.objetivos_declarados import (
    AdicionarObjetivoComunicacao,
    AdicionarObjetivoMarketing,
    ListarDimensoesCompostoMarketing,
    ListarObjetivosComunicacaoDeclarados,
    ListarObjetivosMarketingDeclarados,
    RemoverObjetivoComunicacao,
    RemoverObjetivoMarketing,
)
from mediad_planner.application.use_cases.briefings import (
    AbrirBriefingCampanha,
    AdicionarRegistroSituacaoMercadologica,
    ListarAspectosSituacaoMercadologica,
    RemoverRegistroSituacaoMercadologica,
)
from mediad_planner.application.use_cases.praca_universo import (
    AdicionarPraca,
    AdicionarUniverso,
    ListarTiposPracaTerritorial,
    ListarUnidadesPopulacionais,
    RemoverPraca,
    RemoverUniverso,
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
        listar_marketing=ListarObjetivosMarketingDeclarados(),
        listar_comunicacao=ListarObjetivosComunicacaoDeclarados(),
        listar_dimensoes_composto=ListarDimensoesCompostoMarketing(),
        adicionar_marketing=AdicionarObjetivoMarketing(
            repositorio=repositorio_briefings,
            contexto_acesso=contexto,
            relogio=relogio,
            gerador_uuid=gerador_uuid,
        ),
        adicionar_comunicacao=AdicionarObjetivoComunicacao(
            repositorio=repositorio_briefings,
            contexto_acesso=contexto,
            relogio=relogio,
            gerador_uuid=gerador_uuid,
        ),
        remover_marketing=RemoverObjetivoMarketing(
            repositorio=repositorio_briefings,
            contexto_acesso=contexto,
            relogio=relogio,
        ),
        remover_comunicacao=RemoverObjetivoComunicacao(
            repositorio=repositorio_briefings,
            contexto_acesso=contexto,
            relogio=relogio,
        ),
        listar_tipos_praca=ListarTiposPracaTerritorial(),
        listar_unidades_populacionais=ListarUnidadesPopulacionais(),
        adicionar_praca=AdicionarPraca(
            repositorio=repositorio_briefings,
            contexto_acesso=contexto,
            relogio=relogio,
            gerador_uuid=gerador_uuid,
        ),
        remover_praca=RemoverPraca(
            repositorio=repositorio_briefings,
            contexto_acesso=contexto,
            relogio=relogio,
        ),
        adicionar_universo=AdicionarUniverso(
            repositorio=repositorio_briefings,
            contexto_acesso=contexto,
            relogio=relogio,
            gerador_uuid=gerador_uuid,
        ),
        remover_universo=RemoverUniverso(
            repositorio=repositorio_briefings,
            contexto_acesso=contexto,
            relogio=relogio,
        ),
    )
