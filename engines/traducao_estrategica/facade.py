"""Fachada contratual sem regras estratégicas da implementação futura."""

from datetime import datetime
from enum import Enum
from typing import Protocol

from pydantic import BaseModel, ConfigDict

from domain.contracts import (
    Alerta,
    ComandoMotor,
    Confianca,
    EstadoExecucao,
    PlanoReexecucao,
    PoliticaReexecucao,
    Rastreabilidade,
    ResultadoValidacao,
    SaidaMotor,
    Severidade,
    ValidacaoLocal,
)

MOTOR_TRADUCAO_ESTRATEGICA = "TRADUCAO_ESTRATEGICA"


class ModoTraducaoEstrategica(str, Enum):
    TRADUZIR_BRIEFING = "TRADUZIR_BRIEFING"
    REVISAR_TRADUCAO = "REVISAR_TRADUCAO"
    VALIDAR_SUFICIENCIA_ESTRATEGICA = "VALIDAR_SUFICIENCIA_ESTRATEGICA"
    RECALCULAR_DEPENDENCIAS_ESTRATEGICAS = "RECALCULAR_DEPENDENCIAS_ESTRATEGICAS"


class EstadoContratoEstrategico(str, Enum):
    PROVISORIO = "PROVISORIO"
    PARCIAL = "PARCIAL"
    INSUFICIENTE = "INSUFICIENTE"


class ContratoEstrategicoFundacao(BaseModel):
    """Resultado honesto da fachada: contrato ainda não calculado."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    estado_estrategico: EstadoContratoEstrategico
    modo_execucao: ModoTraducaoEstrategica
    objetivo_original: str
    referencias_consumidas: tuple[str, ...] = ()
    lacunas: tuple[str, ...] = ("procedimentos_estrategicos_nao_implementados",)
    implementacao: str = "FACHADA_FALSA"


class Relogio(Protocol):
    def agora(self) -> datetime: ...


class MotorTraducaoEstrategicaFake:
    """Valida e exercita o contrato comum sem antecipar o motor real."""

    def __init__(self, relogio: Relogio):
        self.relogio = relogio

    def executar(self, comando: ComandoMotor) -> SaidaMotor:
        if comando.motor_destino != MOTOR_TRADUCAO_ESTRATEGICA:
            raise ValueError("comando destinado a outro motor")
        try:
            modo = ModoTraducaoEstrategica(comando.modo_execucao)
        except ValueError as erro:
            raise ValueError("modo de Tradução Estratégica inválido") from erro

        referencias = tuple(
            f"{referencia.tipo}:{referencia.id}:{referencia.versao}"
            for referencia in comando.referencias_de_entrada
        )
        estado_estrategico = (
            EstadoContratoEstrategico.PARCIAL
            if referencias
            else EstadoContratoEstrategico.INSUFICIENTE
        )
        principal = ContratoEstrategicoFundacao(
            estado_estrategico=estado_estrategico,
            modo_execucao=modo,
            objetivo_original=comando.objetivo_da_execucao,
            referencias_consumidas=referencias,
        )
        validacao = ValidacaoLocal(
            codigo="FACHADA_SEM_PROCEDIMENTOS",
            objeto_validado="contrato_estrategico_do_planejamento",
            resultado=ResultadoValidacao.INDETERMINADO,
            severidade=Severidade.ATENCAO,
            mensagem=(
                "A fachada valida o envelope, mas ainda não executa "
                "procedimentos estratégicos."
            ),
            impacto_na_execucao="resultado obrigatoriamente parcial",
            acao_recomendada="implementar procedimentos a partir das Bibliotecas 14–18",
        )
        alerta = Alerta(
            codigo="MOTOR_EM_FUNDACAO",
            severidade=Severidade.ATENCAO,
            titulo="Tradução Estratégica ainda não implementada",
            mensagem="Nenhum objetivo, prioridade, peso ou meio foi derivado.",
            objeto_afetado="contrato_estrategico_do_planejamento",
            impacto="saída não utilizável para decisão de arquitetura",
            acao_possivel="implementar a primeira regra versionada",
            origem="MotorTraducaoEstrategicaFake",
        )
        return SaidaMotor(
            id_comando=comando.id_comando,
            motor=MOTOR_TRADUCAO_ESTRATEGICA,
            modo_execucao=modo.value,
            nivel_execucao=comando.nivel_execucao,
            estado_execucao=EstadoExecucao.PARCIAL,
            resultado_principal=principal,
            validacoes=(validacao,),
            alertas=(alerta,),
            confianca=Confianca.INDETERMINADA,
            explicacao={
                "conclusao_pratica": "Tradução não executada.",
                "principais_razoes": (
                    "A fachada existe apenas para validar o contrato.",
                ),
                "memoria_tecnica": {
                    "implementacao": "FACHADA_FALSA",
                    "procedimentos_executados": (),
                },
            },
            rastreabilidade=Rastreabilidade(
                entradas_utilizadas=comando.referencias_de_entrada,
            ),
            reexecucao=PlanoReexecucao(
                politica=PoliticaReexecucao.REEXECUTAR_MOTOR,
                motivo="procedimentos estratégicos ainda não implementados",
                alvos=(MOTOR_TRADUCAO_ESTRATEGICA,),
            ),
            produzido_em=self.relogio.agora(),
        )
