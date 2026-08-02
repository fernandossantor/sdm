from dataclasses import FrozenInstanceError

import pytest

from mediad_planner.application.dto.diagnostico_fundacao import DiagnosticoFundacao
from mediad_planner.application.use_cases.obter_diagnostico_fundacao import (
    obter_diagnostico_fundacao,
)


def test_diagnostico_verifica_fundacao_real_e_e_imutavel() -> None:
    diagnostico = obter_diagnostico_fundacao()

    assert diagnostico.backend_operacional is True
    assert diagnostico.versao_contrato == "1.0.0"
    assert diagnostico.motores_previstos == (
        "TRADUCAO_ESTRATEGICA",
        "DECISAO_ARQUITETURA_CENARIOS",
        "SIMULACAO_TECNICA_E_ECONOMICA",
    )
    assert diagnostico.camadas_verificadas == (
        "domain",
        "application",
        "engines",
    )
    assert diagnostico.erros == ()
    with pytest.raises(FrozenInstanceError):
        diagnostico.backend_operacional = False


def test_diagnostico_normaliza_todas_as_colecoes_para_tuplas() -> None:
    diagnostico = DiagnosticoFundacao(
        backend_operacional=False,
        versao_contrato="1.0.0",
        motores_previstos=["motor"],
        camadas_verificadas=["domain"],
        mensagem="teste",
        erros=["erro"],
    )

    assert diagnostico.motores_previstos == ("motor",)
    assert diagnostico.camadas_verificadas == ("domain",)
    assert diagnostico.erros == ("erro",)
