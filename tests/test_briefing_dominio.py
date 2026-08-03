from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest

from mediad_planner.domain.briefing.contexto import ContextoHerdadoBriefing
from mediad_planner.domain.briefing.entidades import Briefing
from mediad_planner.domain.briefing.enums import EstadoBriefing
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
            criado_por=UUID(int=4),
            criado_em=AGORA,
            atualizado_por=UUID(int=4),
            atualizado_em=AGORA,
        )
