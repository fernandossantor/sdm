from __future__ import annotations

from copy import deepcopy

import pytest

from infrastructure.repositories.traducao_estrategica_v1 import (
    RepositorioTraducaoEstrategicaSupabase,
)
from src.application.persistencia_traducao import RegistroPersistenciaTraducao


def _registro() -> RegistroPersistenciaTraducao:
    return RegistroPersistenciaTraducao(
        espaco_id="00000000-0000-0000-0000-000000000001",
        usuario_id="00000000-0000-0000-0000-000000000002",
        campanha={"id": "campanha-canonica", "nome": "Campanha canonica"},
        briefing_snapshot={"id": "briefing-canonico", "conteudo": {"verba": None}},
        comando={"id": "comando-canonico", "modo": "TRADUZIR_BRIEFING"},
        execucao={"id": "execucao-canonica", "confianca": 72.5},
        contrato={"id": "contrato-canonico", "conteudo": {"objetivos": []}},
        rastreabilidade=({"id": "rastro-1", "ordem": 0},),
    )


class _Resposta:
    data = "contrato-canonico"


class _Chamada:
    def execute(self) -> _Resposta:
        return _Resposta()


class _ClienteFake:
    def __init__(self) -> None:
        self.nome: str | None = None
        self.parametros: dict | None = None

    def rpc(self, nome: str, parametros: dict) -> _Chamada:
        self.nome = nome
        self.parametros = parametros
        return _Chamada()


def test_registro_preserva_ausencia_e_nao_depende_de_banco() -> None:
    registro = _registro()

    assert registro.briefing_snapshot["conteudo"]["verba"] is None
    assert registro.briefing_snapshot["conteudo"]["verba"] != 0


def test_conteudo_rpc_e_copia_previsivel() -> None:
    registro = _registro()
    esperado = deepcopy(registro.conteudo_rpc())

    assert registro.conteudo_rpc() == esperado
    assert tuple(registro.conteudo_rpc()) == (
        "campanha",
        "briefing_snapshot",
        "comando",
        "execucao",
        "contrato",
        "rastreabilidade",
    )


def test_adaptador_realiza_uma_unica_chamada_atomica() -> None:
    cliente = _ClienteFake()

    contrato_id = RepositorioTraducaoEstrategicaSupabase(cliente).salvar(_registro())

    assert contrato_id == "contrato-canonico"
    assert cliente.nome == "persistir_traducao_estrategica_v1"
    assert cliente.parametros is not None
    assert set(cliente.parametros) == {"p_espaco_id", "p_usuario_id", "p_registro"}
    assert "secret" not in repr(cliente.parametros).lower()


def test_adaptador_rejeita_resposta_sem_id() -> None:
    class ClienteSemId(_ClienteFake):
        def rpc(self, nome: str, parametros: dict) -> _Chamada:
            class ChamadaSemId:
                def execute(self):
                    return type("Resposta", (), {"data": None})()

            return ChamadaSemId()

    with pytest.raises(RuntimeError, match="id do contrato"):
        RepositorioTraducaoEstrategicaSupabase(ClienteSemId()).salvar(_registro())
