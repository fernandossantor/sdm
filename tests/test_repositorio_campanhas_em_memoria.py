from dataclasses import replace
from datetime import datetime, timezone
from uuid import UUID

import pytest

from mediad_planner.application.ports.repositorio_campanhas import (
    RepositorioCampanhas,
)
from mediad_planner.domain.campanha.codigo import (
    CodigoCampanha,
    gerar_codigo_campanha,
)
from mediad_planner.domain.campanha.entidades import Campanha
from mediad_planner.domain.campanha.vinculos import (
    AnuncianteCampanha,
    ParticipanteCampanha,
)
from mediad_planner.infrastructure.repositories.campanhas_em_memoria import (
    RepositorioCampanhasEmMemoria,
)


def criar_campanha(
    identificador: int,
    espaco: int,
    codigo: str,
    criado_em: datetime,
) -> Campanha:
    return Campanha.criar_rascunho(
        id_campanha=UUID(int=identificador),
        id_espaco_trabalho=UUID(int=espaco),
        codigo=CodigoCampanha(codigo),
        nome=f"Campanha {identificador}",
        anunciante=AnuncianteCampanha(UUID(int=20), "Anunciante"),
        marca=None,
        produto_servico=None,
        planejador_responsavel=ParticipanteCampanha(UUID(int=21), "Pessoa"),
        equipe=(),
        observacao_inicial=None,
        criado_por=UUID(int=22),
        criado_em=criado_em,
        atualizado_por=UUID(int=22),
        atualizado_em=criado_em,
    )


def test_sequencia_global_cresce_sem_conhecer_mes() -> None:
    repositorio = RepositorioCampanhasEmMemoria()
    julho = datetime(2026, 7, 31, tzinfo=timezone.utc)
    agosto = datetime(2026, 8, 1, tzinfo=timezone.utc)
    primeiro = repositorio.reservar_proximo_sequencial_global()
    segundo = repositorio.reservar_proximo_sequencial_global()
    terceiro = repositorio.reservar_proximo_sequencial_global()
    assert (primeiro, segundo, terceiro) == (1, 2, 3)
    assert gerar_codigo_campanha(julho, segundo).valor == "MP-202607-0002"
    assert gerar_codigo_campanha(agosto, terceiro).valor == "MP-202608-0003"


def test_armazena_atualiza_e_implementa_protocolo() -> None:
    repositorio = RepositorioCampanhasEmMemoria()
    campanha = criar_campanha(
        1,
        10,
        "MP-202607-0001",
        datetime(2026, 7, 1, tzinfo=timezone.utc),
    )
    repositorio.salvar(campanha)
    atualizada = campanha.iniciar_briefing(
        UUID(int=30),
        datetime(2026, 7, 2, tzinfo=timezone.utc),
    )
    repositorio.salvar(atualizada)
    obtida = repositorio.obter(UUID(int=10), campanha.id_campanha)
    assert isinstance(repositorio, RepositorioCampanhas)
    assert obtida == atualizada
    assert obtida.id_campanha == campanha.id_campanha
    assert obtida.codigo == campanha.codigo


def test_rejeita_codigo_alterado_e_codigo_duplicado() -> None:
    repositorio = RepositorioCampanhasEmMemoria()
    data = datetime(2026, 7, 1, tzinfo=timezone.utc)
    campanha = criar_campanha(1, 10, "MP-202607-0001", data)
    repositorio.salvar(campanha)
    com_codigo_alterado = replace(
        campanha,
        codigo=CodigoCampanha("MP-202607-0002"),
    )
    outra_com_mesmo_codigo = criar_campanha(2, 10, "MP-202607-0001", data)
    with pytest.raises(ValueError, match="alterado"):
        repositorio.salvar(com_codigo_alterado)
    with pytest.raises(ValueError, match="utilizado"):
        repositorio.salvar(outra_com_mesmo_codigo)


def test_isola_espacos_e_ordena_da_mais_recente() -> None:
    repositorio = RepositorioCampanhasEmMemoria()
    antiga = criar_campanha(
        1,
        10,
        "MP-202607-0001",
        datetime(2026, 7, 1, tzinfo=timezone.utc),
    )
    recente = criar_campanha(
        2,
        10,
        "MP-202608-0002",
        datetime(2026, 8, 1, tzinfo=timezone.utc),
    )
    outro_espaco = criar_campanha(
        3,
        11,
        "MP-202608-0003",
        datetime(2026, 8, 2, tzinfo=timezone.utc),
    )
    for campanha in (antiga, recente, outro_espaco):
        repositorio.salvar(campanha)
    listadas = repositorio.listar(UUID(int=10))
    assert isinstance(listadas, tuple)
    assert listadas == (recente, antiga)
    assert repositorio.obter(UUID(int=11), antiga.id_campanha) is None
