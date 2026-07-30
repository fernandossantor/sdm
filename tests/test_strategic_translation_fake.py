from datetime import datetime, timezone
from uuid import uuid4

import pytest

from domain.contracts import (
    ComandoMotor,
    EstadoExecucao,
    NivelExecucao,
    PoliticaReexecucao,
    ReferenciaVersionada,
)
from engines.base import Motor
from engines.traducao_estrategica import (
    MOTOR_TRADUCAO_ESTRATEGICA,
    ContratoEstrategicoFundacao,
    EstadoContratoEstrategico,
    ModoTraducaoEstrategica,
    MotorTraducaoEstrategicaFake,
)


class RelogioFixo:
    instante = datetime(2026, 7, 30, 15, tzinfo=timezone.utc)

    def agora(self):
        return self.instante


def comando(**ajustes):
    dados = {
        "motor_destino": MOTOR_TRADUCAO_ESTRATEGICA,
        "modo_execucao": ModoTraducaoEstrategica.TRADUZIR_BRIEFING.value,
        "nivel_execucao": NivelExecucao.PREVIA,
        "id_campanha": uuid4(),
        "id_snapshot_campanha": uuid4(),
        "id_usuario": uuid4(),
        "perfil_de_acesso": "PLANEJADOR",
        "solicitado_em": datetime.now(timezone.utc),
        "origem_do_comando": "teste",
        "objetivo_da_execucao": "Traduzir briefing sem inventar informação.",
    }
    dados.update(ajustes)
    return ComandoMotor(**dados)


@pytest.mark.parametrize("modo", list(ModoTraducaoEstrategica))
def test_aceita_os_quatro_modos_normativos_sem_executar_regras(modo):
    motor: Motor = MotorTraducaoEstrategicaFake(RelogioFixo())
    saida = motor.executar(comando(modo_execucao=modo.value))
    assert saida.estado_execucao is EstadoExecucao.PARCIAL
    assert saida.modo_execucao == modo.value
    assert saida.alertas[0].codigo == "MOTOR_EM_FUNDACAO"
    assert saida.explicacao["memoria_tecnica"]["procedimentos_executados"] == ()


def test_preserva_referencias_e_objetivo_original_na_rastreabilidade():
    referencia = ReferenciaVersionada(
        id="briefing-1",
        tipo="BRIEFING",
        versao="1",
        origem="campanha",
    )
    saida = MotorTraducaoEstrategicaFake(RelogioFixo()).executar(
        comando(referencias_de_entrada=(referencia,))
    )
    principal = saida.resultado_principal
    assert isinstance(principal, ContratoEstrategicoFundacao)
    assert principal.estado_estrategico is EstadoContratoEstrategico.PARCIAL
    assert principal.objetivo_original == "Traduzir briefing sem inventar informação."
    assert saida.rastreabilidade.entradas_utilizadas == (referencia,)
    assert saida.produzido_em == RelogioFixo.instante


def test_sem_referencia_declara_contrato_insuficiente_sem_criar_defaults():
    saida = MotorTraducaoEstrategicaFake(RelogioFixo()).executar(comando())
    principal = saida.resultado_principal
    assert principal.estado_estrategico is EstadoContratoEstrategico.INSUFICIENTE
    assert principal.referencias_consumidas == ()
    assert "pesos" not in principal.model_fields_set
    assert saida.reexecucao.politica is PoliticaReexecucao.REEXECUTAR_MOTOR


def test_rejeita_destino_e_modo_invalidos():
    motor = MotorTraducaoEstrategicaFake(RelogioFixo())
    with pytest.raises(ValueError, match="outro motor"):
        motor.executar(comando(motor_destino="SIMULACAO_TECNICA_ECONOMICA"))
    with pytest.raises(ValueError, match="modo"):
        motor.executar(comando(modo_execucao="INVENTAR_ESTRATEGIA"))
