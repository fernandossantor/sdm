from datetime import datetime, timezone
from uuid import uuid4

from mediad_planner.domain.common.enums import (
    EstadoExecucao,
    MotorDestino,
    NivelConfianca,
    NivelExecucao,
    OrigemComando,
    PapelAcesso,
    PoliticaReexecucao,
)
from mediad_planner.domain.common.value_objects import LimitesExecucao
from mediad_planner.domain.contracts.motores import (
    VERSAO_CONTRATO_MOTORES,
    ComandoMotor,
    ConfiancaExecucao,
    ExplicacaoExecucao,
    RastreabilidadeExecucao,
    SaidaMotor,
)
from mediad_planner.engines.base.motor_especialista import MotorEspecialista


def criar_comando_minimo() -> ComandoMotor:
    return ComandoMotor(
        id_comando=uuid4(),
        motor_destino=MotorDestino.TRADUCAO_ESTRATEGICA,
        modo_execucao="TESTE",
        nivel_execucao=NivelExecucao.PREVIA,
        id_campanha=uuid4(),
        id_snapshot_campanha=uuid4(),
        id_usuario=uuid4(),
        perfil_de_acesso=PapelAcesso.EDITOR,
        solicitado_em=datetime.now(timezone.utc),
        origem_do_comando=OrigemComando.SERVICO_APLICACAO,
        objetivo_da_execucao="Testar protocolo",
        referencias_de_entrada=(),
        parametros_locais=(),
        limites_de_execucao=LimitesExecucao(),
    )


def criar_saida_minima(comando: ComandoMotor) -> SaidaMotor[str]:
    confianca = ConfiancaExecucao(*(NivelConfianca.ALTA,) * 4)
    explicacao = ExplicacaoExecucao("ok", (), (), (), (), (), ())
    rastreabilidade = RastreabilidadeExecucao((), (), (), (), ())
    return SaidaMotor(
        id_execucao=uuid4(),
        id_comando=comando.id_comando,
        motor=comando.motor_destino,
        modo_execucao=comando.modo_execucao,
        nivel_execucao=comando.nivel_execucao,
        estado_execucao=EstadoExecucao.CONCLUIDA,
        resultado_principal="ok",
        resultados_secundarios=(),
        validacoes=(),
        alertas=(),
        restricoes=(),
        confianca=confianca,
        explicacao=explicacao,
        rastreabilidade=rastreabilidade,
        dependencias=(),
        reexecucao=PoliticaReexecucao.NENHUMA,
        produzido_em=datetime.now(timezone.utc),
        versao_do_contrato=VERSAO_CONTRATO_MOTORES,
    )


class MotorFicticio:
    def executar(self, comando: ComandoMotor) -> SaidaMotor[str]:
        return criar_saida_minima(comando)


def test_protocolo_aceita_implementacao_estrutural_minima() -> None:
    comando = criar_comando_minimo()
    motor_ficticio = MotorFicticio()

    assert isinstance(motor_ficticio, MotorEspecialista)
    resultado = motor_ficticio.executar(comando)
    assert isinstance(resultado, SaidaMotor)
