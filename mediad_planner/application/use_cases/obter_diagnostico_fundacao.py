from dataclasses import FrozenInstanceError, is_dataclass
from datetime import datetime, timezone
from uuid import UUID

from mediad_planner.application.dto.diagnostico_fundacao import DiagnosticoFundacao
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


def _verificar_dataclass_congelada(classe: type[object], nome: str) -> None:
    if not is_dataclass(classe):
        raise TypeError(f"{nome} não é dataclass")
    parametros = getattr(classe, "__dataclass_params__", None)
    if parametros is None or not parametros.frozen:
        raise TypeError(f"{nome} não está congelada")


def obter_diagnostico_fundacao() -> DiagnosticoFundacao:
    motores = tuple(motor.value for motor in MotorDestino)
    motores_esperados = (
        "TRADUCAO_ESTRATEGICA",
        "DECISAO_ARQUITETURA_CENARIOS",
        "SIMULACAO_TECNICA_E_ECONOMICA",
    )
    camadas = ("domain", "application", "engines")

    try:
        if VERSAO_CONTRATO_MOTORES != "1.0.0":
            raise ValueError("versão canônica divergente")
        if motores != motores_esperados:
            raise ValueError("motores canônicos divergentes")

        _verificar_dataclass_congelada(ComandoMotor, "ComandoMotor")
        _verificar_dataclass_congelada(SaidaMotor, "SaidaMotor")

        agora = datetime.now(timezone.utc)
        comando = ComandoMotor(
            id_comando=UUID(int=1),
            motor_destino=MotorDestino.TRADUCAO_ESTRATEGICA,
            modo_execucao="VERIFICACAO",
            nivel_execucao=NivelExecucao.PREVIA,
            id_campanha=UUID(int=2),
            id_snapshot_campanha=UUID(int=3),
            id_usuario=UUID(int=4),
            perfil_de_acesso=PapelAcesso.LEITOR,
            solicitado_em=agora,
            origem_do_comando=OrigemComando.SERVICO_APLICACAO,
            objetivo_da_execucao="Verificar contratos",
            referencias_de_entrada=(),
            parametros_locais=(),
            limites_de_execucao=LimitesExecucao(),
        )
        confianca = ConfiancaExecucao(
            metodologica=NivelConfianca.ALTA,
            dados=NivelConfianca.ALTA,
            aplicacao=NivelConfianca.ALTA,
            resultado=NivelConfianca.ALTA,
        )
        explicacao = ExplicacaoExecucao(
            conclusao_pratica="Contratos construídos",
            principais_razoes=(),
            restricoes_relevantes=(),
            alternativas_rejeitadas=(),
            trade_offs=(),
            conhecimentos_aplicados=(),
            memoria_tecnica=(),
        )
        rastreabilidade = RastreabilidadeExecucao((), (), (), (), ())
        saida = SaidaMotor(
            id_execucao=UUID(int=5),
            id_comando=comando.id_comando,
            motor=comando.motor_destino,
            modo_execucao=comando.modo_execucao,
            nivel_execucao=comando.nivel_execucao,
            estado_execucao=EstadoExecucao.CONCLUIDA,
            resultado_principal="verificado",
            resultados_secundarios=(),
            validacoes=(),
            alertas=(),
            restricoes=(),
            confianca=confianca,
            explicacao=explicacao,
            rastreabilidade=rastreabilidade,
            dependencias=(),
            reexecucao=PoliticaReexecucao.NENHUMA,
            produzido_em=agora,
            versao_do_contrato=VERSAO_CONTRATO_MOTORES,
        )

        class _MotorMinimo:
            def executar(self, comando_recebido: ComandoMotor) -> SaidaMotor[str]:
                return saida

        if not isinstance(_MotorMinimo(), MotorEspecialista):
            raise TypeError("protocolo estrutural indisponível")

        for contrato in (comando, saida):
            try:
                contrato.modo_execucao = "ALTERADO"  # type: ignore[misc]
            except (FrozenInstanceError, AttributeError):
                pass
            else:
                raise TypeError("contrato não está congelado")

        if comando.solicitado_em.utcoffset() is None:
            raise ValueError("horário do comando sem fuso")
        if saida.produzido_em.utcoffset() is None:
            raise ValueError("horário da saída sem fuso")
    except (ValueError, TypeError) as erro:
        return DiagnosticoFundacao(
            backend_operacional=False,
            versao_contrato=VERSAO_CONTRATO_MOTORES,
            motores_previstos=motores,
            camadas_verificadas=camadas,
            mensagem="A fundação requer correção.",
            erros=(str(erro),),
        )

    return DiagnosticoFundacao(
        backend_operacional=True,
        versao_contrato=VERSAO_CONTRATO_MOTORES,
        motores_previstos=motores,
        camadas_verificadas=camadas,
        mensagem="Contratos funcionais verificados pela aplicação.",
        erros=(),
    )
