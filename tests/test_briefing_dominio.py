from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID

import pytest

from mediad_planner.domain.briefing.contexto import ContextoHerdadoBriefing
from mediad_planner.domain.briefing.entidades import Briefing
from mediad_planner.domain.briefing.enums import EstadoBriefing
from mediad_planner.domain.briefing.objetivos_declarados import (
    ObjetivoComunicacaoDeclarado,
    ObjetivoMarketingDeclarado,
    ObjetivosDeclarados,
)
from mediad_planner.domain.briefing.situacao_mercadologica import (
    EscopoSituacaoMercadologica,
    NaturezaRegistroSituacao,
    RegistroSituacaoMercadologica,
    SituacaoMercadologicaCompetitiva,
)
from mediad_planner.domain.campanha.codigo import CodigoCampanha
from mediad_planner.domain.campanha.vinculos import (
    AnuncianteCampanha,
    ParticipanteCampanha,
)


AGORA = datetime(2026, 8, 2, tzinfo=timezone.utc)


def contexto(**mudancas: object) -> ContextoHerdadoBriefing:
    dados = {
        "codigo_campanha": CodigoCampanha("MP-202608-0001"),
        "nome_campanha": "Campanha",
        "anunciante": AnuncianteCampanha(UUID(int=1), "Anunciante"),
        "marca": None,
        "produto_servico": None,
        "planejador_responsavel": ParticipanteCampanha(UUID(int=2), "Pessoa"),
        "equipe": [],
    }
    dados.update(mudancas)
    return ContextoHerdadoBriefing(**dados)


def briefing(**mudancas: object) -> Briefing:
    dados = {
        "id_briefing": UUID(int=10),
        "id_campanha": UUID(int=11),
        "id_espaco_trabalho": UUID(int=12),
        "contexto_herdado": contexto(),
        "criado_por": UUID(int=13),
        "criado_em": AGORA,
        "atualizado_por": UUID(int=13),
        "atualizado_em": AGORA,
    }
    dados.update(mudancas)
    return Briefing.criar_versao_inicial(**dados)


def test_estado_briefing_tem_composicao_exata() -> None:
    assert tuple(item.value for item in EstadoBriefing) == (
        "RASCUNHO",
        "EM_PREENCHIMENTO",
        "EM_REVISAO",
        "CONCLUIDO",
        "SUBSTITUIDO",
    )


def test_cria_versao_inicial_imutavel_e_sem_transicoes_antecipadas() -> None:
    criado = briefing()
    assert criado.numero_versao == 1
    assert criado.estado is EstadoBriefing.RASCUNHO
    assert criado.contexto_herdado.marca is None
    assert criado.contexto_herdado.produto_servico is None
    with pytest.raises(FrozenInstanceError):
        criado.numero_versao = 2
    assert not hasattr(criado, "concluir")
    assert not hasattr(criado, "traduzir")
    assert not hasattr(criado, "criar_nova_versao")


def test_contexto_valida_obrigatorios_e_normaliza_equipe() -> None:
    pessoa = ParticipanteCampanha(UUID(int=20), "Equipe")
    criado = contexto(equipe=[pessoa])
    assert criado.equipe == (pessoa,)
    for campo in ("codigo_campanha", "anunciante", "planejador_responsavel"):
        with pytest.raises(ValueError):
            contexto(**{campo: None})
    with pytest.raises(ValueError, match="nome_campanha"):
        contexto(nome_campanha=" ")
    with pytest.raises(ValueError, match="duplicados"):
        contexto(equipe=[pessoa, pessoa])


def test_briefing_valida_contexto_datas_versao_e_uuids() -> None:
    with pytest.raises(ValueError, match="contexto"):
        briefing(contexto_herdado=None)
    with pytest.raises(ValueError, match="fuso"):
        briefing(criado_em=datetime.now())
    with pytest.raises(ValueError, match="fuso"):
        briefing(atualizado_em=datetime.now())
    with pytest.raises(ValueError, match="anteceder"):
        briefing(atualizado_em=AGORA - timedelta(seconds=1))
    for campo in (
        "id_briefing",
        "id_campanha",
        "id_espaco_trabalho",
        "criado_por",
        "atualizado_por",
    ):
        with pytest.raises(TypeError, match=campo):
            briefing(**{campo: "invalido"})
    with pytest.raises(ValueError, match="numero_versao"):
        Briefing(
            id_briefing=UUID(int=1),
            id_campanha=UUID(int=2),
            id_espaco_trabalho=UUID(int=3),
            numero_versao=True,
            estado=EstadoBriefing.RASCUNHO,
                contexto_herdado=contexto(),
                situacao_mercadologica=SituacaoMercadologicaCompetitiva(()),
            objetivos_declarados=ObjetivosDeclarados((), ()),
            criado_por=UUID(int=4),
            criado_em=AGORA,
            atualizado_por=UUID(int=4),
            atualizado_em=AGORA,
        )


def test_registro_altera_estado_e_remocao_nao_retorna_a_rascunho() -> None:
    inicial = briefing()
    registro = RegistroSituacaoMercadologica(
        id_registro=UUID(int=90),
        escopo=EscopoSituacaoMercadologica.MERCADO,
        codigo_aspecto="taxa_crescimento_mercado",
        aspecto="Taxa de crescimento do mercado",
        entidade_referencia=None,
        natureza=NaturezaRegistroSituacao.QUANTITATIVO,
        valor_quantitativo=Decimal("2.5"),
        unidade="%",
        valor_qualitativo=None,
        fonte=None,
        periodo_referencia=None,
        observacao=None,
    )
    instante = AGORA + timedelta(seconds=1)

    alterado = inicial.adicionar_registro_situacao(
        registro,
        atualizado_por=UUID(int=91),
        atualizado_em=instante,
    )
    removido = alterado.remover_registro_situacao(
        registro.id_registro,
        atualizado_por=UUID(int=92),
        atualizado_em=instante,
    )

    assert inicial.situacao_mercadologica.registros == ()
    assert alterado.estado is EstadoBriefing.EM_PREENCHIMENTO
    assert alterado.numero_versao == inicial.numero_versao
    assert alterado.contexto_herdado == inicial.contexto_herdado
    assert alterado.criado_em == inicial.criado_em
    assert removido.estado is EstadoBriefing.EM_PREENCHIMENTO
    assert removido.situacao_mercadologica.registros == ()
    with pytest.raises(ValueError, match="regredir"):
        alterado.adicionar_registro_situacao(
            registro,
            atualizado_por=UUID(int=93),
            atualizado_em=AGORA,
        )


def test_objetivos_no_agregado_preservam_contexto_situacao_e_estado() -> None:
    inicial = briefing()
    marketing = ObjetivoMarketingDeclarado(
        id_objetivo=UUID(int=201),
        codigo_objetivo="marketing_crescimento",
        objetivo="Crescimento",
        dimensoes_composto=(),
        prioridade_declarada=5,
        intensidade_declarada=4,
        justificativa=None,
    )
    instante = AGORA + timedelta(seconds=1)
    com_marketing = inicial.adicionar_objetivo_marketing(
        marketing,
        atualizado_por=UUID(int=202),
        atualizado_em=instante,
    )
    comunicacao = ObjetivoComunicacaoDeclarado(
        id_objetivo=UUID(int=203),
        codigo_objetivo="comunicacao_notoriedade",
        objetivo="Notoriedade",
        ids_objetivos_marketing_relacionados=(marketing.id_objetivo,),
        prioridade_declarada=4,
        intensidade_declarada=3,
        justificativa=None,
    )
    completo = com_marketing.adicionar_objetivo_comunicacao(
        comunicacao,
        atualizado_por=UUID(int=204),
        atualizado_em=instante,
    )
    sem_comunicacao = completo.remover_objetivo_comunicacao(
        comunicacao.id_objetivo,
        atualizado_por=UUID(int=205),
        atualizado_em=instante,
    )
    removido = sem_comunicacao.remover_objetivo_marketing(
        marketing.id_objetivo,
        atualizado_por=UUID(int=206),
        atualizado_em=instante,
    )

    assert inicial.objetivos_declarados.marketing == ()
    assert completo.estado is EstadoBriefing.EM_PREENCHIMENTO
    assert completo.numero_versao == inicial.numero_versao
    assert completo.contexto_herdado == inicial.contexto_herdado
    assert completo.situacao_mercadologica == inicial.situacao_mercadologica
    assert completo.criado_em == inicial.criado_em
    assert completo.atualizado_por == UUID(int=204)
    assert removido.estado is EstadoBriefing.EM_PREENCHIMENTO
    assert removido.objetivos_declarados == ObjetivosDeclarados((), ())
    with pytest.raises(ValueError, match="regredir"):
        completo.remover_objetivo_comunicacao(
            comunicacao.id_objetivo,
            atualizado_por=UUID(int=207),
            atualizado_em=AGORA,
        )
