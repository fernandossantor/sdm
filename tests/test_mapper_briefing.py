from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from mediad_planner.application.mappers.briefing import resumir_briefing
from mediad_planner.domain.briefing.contexto import ContextoHerdadoBriefing
from mediad_planner.domain.briefing.entidades import Briefing
from mediad_planner.domain.briefing.objetivos_declarados import (
    DimensaoCompostoMarketing,
    ObjetivoComunicacaoDeclarado,
    ObjetivoMarketingDeclarado,
)
from mediad_planner.domain.briefing.situacao_mercadologica import (
    EscopoSituacaoMercadologica,
    NaturezaRegistroSituacao,
    RegistroSituacaoMercadologica,
)
from mediad_planner.domain.campanha.codigo import CodigoCampanha
from mediad_planner.domain.campanha.vinculos import (
    AnuncianteCampanha,
    ParticipanteCampanha,
)


def test_mapper_converte_briefing_completo_sem_expor_enums() -> None:
    agora = datetime(2026, 8, 3, tzinfo=timezone.utc)
    briefing = Briefing.criar_versao_inicial(
        id_briefing=UUID(int=1),
        id_campanha=UUID(int=2),
        id_espaco_trabalho=UUID(int=3),
        contexto_herdado=ContextoHerdadoBriefing(
            codigo_campanha=CodigoCampanha("MP-202608-0001"),
            nome_campanha="Campanha",
            anunciante=AnuncianteCampanha(UUID(int=4), "Anunciante"),
            marca=None,
            produto_servico=None,
            planejador_responsavel=ParticipanteCampanha(UUID(int=5), "Pessoa"),
            equipe=(),
        ),
        criado_por=UUID(int=6),
        criado_em=agora,
        atualizado_por=UUID(int=6),
        atualizado_em=agora,
    )
    registro = RegistroSituacaoMercadologica(
        id_registro=UUID(int=7),
        escopo=EscopoSituacaoMercadologica.MERCADO,
        codigo_aspecto="tamanho_mercado",
        aspecto="Tamanho do mercado",
        entidade_referencia=None,
        natureza=NaturezaRegistroSituacao.QUANTITATIVO,
        valor_quantitativo=Decimal("10.5"),
        unidade="R$",
        valor_qualitativo=None,
        fonte=None,
        periodo_referencia=None,
        observacao=None,
    )
    marketing = ObjetivoMarketingDeclarado(
        id_objetivo=UUID(int=8),
        codigo_objetivo="marketing_crescimento",
        objetivo="Crescimento",
        dimensoes_composto=(
            DimensaoCompostoMarketing.PRODUTO,
            DimensaoCompostoMarketing.PRACA,
        ),
        prioridade_declarada=5,
        intensidade_declarada=4,
        justificativa=None,
    )
    comunicacao = ObjetivoComunicacaoDeclarado(
        id_objetivo=UUID(int=9),
        codigo_objetivo="comunicacao_notoriedade",
        objetivo="Notoriedade",
        ids_objetivos_marketing_relacionados=(marketing.id_objetivo,),
        prioridade_declarada=4,
        intensidade_declarada=3,
        justificativa=None,
    )
    briefing = briefing.adicionar_registro_situacao(
        registro,
        atualizado_por=UUID(int=6),
        atualizado_em=agora,
    )
    briefing = briefing.adicionar_objetivo_marketing(
        marketing,
        atualizado_por=UUID(int=6),
        atualizado_em=agora,
    )
    briefing = briefing.adicionar_objetivo_comunicacao(
        comunicacao,
        atualizado_por=UUID(int=6),
        atualizado_em=agora,
    )

    resumo = resumir_briefing(briefing)

    assert resumo.registros_situacao[0].valor_quantitativo == "10.5"
    assert resumo.registros_situacao[0].escopo == "MERCADO"
    assert resumo.objetivos_marketing[0].codigo_objetivo == (
        "marketing_crescimento"
    )
    assert resumo.objetivos_marketing[0].dimensoes_composto == (
        "PRODUTO",
        "PRACA",
    )
    assert resumo.objetivos_marketing[0].rotulos_dimensoes_composto == (
        "Produto",
        "Praça (distribuição)",
    )
    assert resumo.objetivos_comunicacao[0].codigo_objetivo == (
        "comunicacao_notoriedade"
    )
    assert resumo.objetivos_comunicacao[
        0
    ].ids_objetivos_marketing_relacionados == (marketing.id_objetivo,)
    assert isinstance(resumo.objetivos_marketing[0].dimensoes_composto[0], str)
    assert isinstance(resumo.registros_situacao[0].escopo, str)
