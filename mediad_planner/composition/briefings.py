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
from mediad_planner.application.use_cases.criterios_segmentacao import (
    DefinirCriteriosSegmentacao,
    ListarCriteriosSegmentacao,
)
from mediad_planner.application.use_cases.segmentos import (
    AdicionarSegmento,
    EditarSegmento,
    RemoverSegmento,
)
from mediad_planner.application.use_cases.publicos import (
    AdicionarPublico,
    EditarPublico,
    RemoverPublico,
)
from mediad_planner.application.use_cases.jornada import (
    DefinirAplicabilidadeJornada,
    AdicionarEtapaJornada,
    AdicionarJornada,
    EditarEtapaJornada,
    EditarJornada,
    ListarCategoriasEtapaJornada,
    RemoverEtapaJornada,
    RemoverJornada,
)
from mediad_planner.application.use_cases.periodo_verba import (
    DefinirPeriodoVerba,
    ListarNaturezasLimiteVerba,
)
from mediad_planner.application.use_cases.condicoes_declaradas import GerenciarCondicoesDeclaradas


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
        definir_aplicabilidade_jornada=DefinirAplicabilidadeJornada(
            repositorio_briefings, contexto, relogio,
        ),
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
        listar_criterios_segmentacao=ListarCriteriosSegmentacao(),
        definir_criterios_segmentacao=DefinirCriteriosSegmentacao(
            repositorio=repositorio_briefings,
            contexto_acesso=contexto,
            relogio=relogio,
        ),
        adicionar_segmento=AdicionarSegmento(
            repositorio_briefings, contexto, relogio, gerador_uuid
        ),
        editar_segmento=EditarSegmento(
            repositorio_briefings, contexto, relogio
        ),
        remover_segmento=RemoverSegmento(
            repositorio_briefings, contexto, relogio
        ),
        adicionar_publico=AdicionarPublico(
            repositorio_briefings, contexto, relogio, gerador_uuid
        ),
        editar_publico=EditarPublico(
            repositorio_briefings, contexto, relogio
        ),
        remover_publico=RemoverPublico(
            repositorio_briefings, contexto, relogio
        ),
        listar_categorias_etapa=ListarCategoriasEtapaJornada(),
        adicionar_jornada=AdicionarJornada(
            repositorio_briefings, contexto, relogio, gerador_uuid
        ),
        editar_jornada=EditarJornada(repositorio_briefings, contexto, relogio),
        remover_jornada=RemoverJornada(repositorio_briefings, contexto, relogio),
        adicionar_etapa_jornada=AdicionarEtapaJornada(
            repositorio_briefings, contexto, relogio, gerador_uuid
        ),
        editar_etapa_jornada=EditarEtapaJornada(
            repositorio_briefings, contexto, relogio
        ),
        remover_etapa_jornada=RemoverEtapaJornada(
            repositorio_briefings, contexto, relogio
        ),
        listar_naturezas_limite_verba=ListarNaturezasLimiteVerba(),
        definir_periodo_verba=DefinirPeriodoVerba(
            repositorio_briefings, contexto, relogio
        ),
        gerenciar_condicoes=GerenciarCondicoesDeclaradas(
            repositorio_briefings, contexto, relogio, gerador_uuid
        ),
    )
