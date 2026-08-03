from dataclasses import replace
from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest

from mediad_planner.application.ports.repositorio_briefings import (
    RepositorioBriefings,
)
from mediad_planner.domain.briefing.contexto import ContextoHerdadoBriefing
from mediad_planner.domain.briefing.entidades import Briefing
from mediad_planner.domain.campanha.codigo import CodigoCampanha
from mediad_planner.domain.campanha.vinculos import (
    AnuncianteCampanha,
    ParticipanteCampanha,
)
from mediad_planner.infrastructure.repositories.briefings_em_memoria import (
    RepositorioBriefingsEmMemoria,
)


AGORA = datetime(2026, 8, 2, tzinfo=timezone.utc)


def criar_briefing(
    id_briefing: int = 1,
    id_campanha: int = 2,
    id_espaco: int = 3,
) -> Briefing:
    contexto = ContextoHerdadoBriefing(
        codigo_campanha=CodigoCampanha("MP-202608-0001"),
        nome_campanha="Campanha",
        anunciante=AnuncianteCampanha(UUID(int=4), "Anunciante"),
        marca=None,
        produto_servico=None,
        planejador_responsavel=ParticipanteCampanha(UUID(int=5), "Pessoa"),
        equipe=(),
    )
    return Briefing.criar_versao_inicial(
        id_briefing=UUID(int=id_briefing),
        id_campanha=UUID(int=id_campanha),
        id_espaco_trabalho=UUID(int=id_espaco),
        contexto_herdado=contexto,
        criado_por=UUID(int=6),
        criado_em=AGORA,
        atualizado_por=UUID(int=6),
        atualizado_em=AGORA,
    )


def test_armazena_recupera_isola_e_implementa_protocolo() -> None:
    repositorio = RepositorioBriefingsEmMemoria()
    briefing = criar_briefing()
    repositorio.salvar(briefing)
    assert isinstance(repositorio, RepositorioBriefings)
    assert repositorio.obter_por_campanha(UUID(int=3), UUID(int=2)) == briefing
    assert repositorio.obter_por_campanha(UUID(int=99), UUID(int=2)) is None
    assert not hasattr(repositorio, "briefings")


def test_rejeita_segundo_briefing_e_id_compartilhado() -> None:
    repositorio = RepositorioBriefingsEmMemoria()
    repositorio.salvar(criar_briefing())
    with pytest.raises(ValueError, match="já possui"):
        repositorio.salvar(criar_briefing(id_briefing=9))
    with pytest.raises(ValueError, match="outra Campanha"):
        repositorio.salvar(criar_briefing(id_briefing=1, id_campanha=9))


def test_rejeita_mudancas_estruturais_e_regressao_temporal() -> None:
    repositorio = RepositorioBriefingsEmMemoria()
    briefing = replace(
        criar_briefing(),
        atualizado_em=AGORA + timedelta(seconds=2),
    )
    repositorio.salvar(briefing)
    with pytest.raises(ValueError, match="numero_versao"):
        repositorio.salvar(replace(briefing, numero_versao=2))
    with pytest.raises(ValueError, match="regredir"):
        repositorio.salvar(
            replace(briefing, atualizado_em=AGORA + timedelta(seconds=1))
        )
    with pytest.raises(ValueError):
        repositorio.salvar(replace(briefing, id_espaco_trabalho=UUID(int=8)))
