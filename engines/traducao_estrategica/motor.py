"""Primeiro modo real do Motor de Tradução Estratégica."""

from uuid import UUID, uuid4

from domain.briefing import BriefingInicial
from domain.contracts import (
    Alerta, ComandoMotor, Confianca, Dependencia, EstadoExecucao,
    PlanoReexecucao, PoliticaReexecucao, Rastreabilidade,
    ReferenciaVersionada, ResultadoValidacao, SaidaMotor, Severidade,
    TipoDependencia, ValidacaoLocal,
)
from domain.traducao import traduzir_briefing

from .facade import MOTOR_TRADUCAO_ESTRATEGICA, ModoTraducaoEstrategica


class MotorTraducaoEstrategica:
    def __init__(self, *, relogio, catalogo):
        self.relogio = relogio
        self.catalogo = catalogo

    def executar(self, comando: ComandoMotor) -> SaidaMotor:
        if comando.motor_destino != MOTOR_TRADUCAO_ESTRATEGICA:
            raise ValueError("comando destinado a outro motor")
        if comando.modo_execucao != ModoTraducaoEstrategica.TRADUZIR_BRIEFING:
            raise ValueError("este incremento executa apenas TRADUZIR_BRIEFING")
        briefing = comando.parametros_locais.get("briefing")
        if not isinstance(briefing, BriefingInicial):
            raise ValueError("briefing estruturado é obrigatório")
        instante = self.relogio.agora()
        contrato = traduzir_briefing(
            briefing, contrato_id=UUID(str(
                comando.parametros_locais.get("contrato_id") or uuid4()
            )), criado_por=comando.id_usuario, criado_em=instante,
            catalogo=self.catalogo,
        )
        referencias_bibliotecas = tuple(
            ReferenciaVersionada(
                id=item.codigo, tipo=f"BIBLIOTECA_{item.biblioteca}",
                versao=item.versao, origem="catalogo_traducao_inicial",
            ) for item in contrato.referencias_bibliotecas
        )
        referencia_briefing = ReferenciaVersionada(
            id=str(briefing.id), tipo="BRIEFING",
            versao=str(briefing.versao), origem="campanha",
        )
        alertas = tuple(
            Alerta(
                codigo="TRADUCAO_COM_LACUNA", severidade=Severidade.ATENCAO,
                titulo="Tradução estratégica parcial", mensagem=lacuna,
                objeto_afetado="contrato_estrategico",
                impacto="reduz confiança ou impede derivação completa",
                acao_possivel="complementar dados ou formalizar conhecimento",
                origem=MOTOR_TRADUCAO_ESTRATEGICA,
            ) for lacuna in contrato.lacunas
        )
        estado = (
            EstadoExecucao.CONCLUIDA_COM_RESSALVAS
            if alertas else EstadoExecucao.CONCLUIDA
        )
        return SaidaMotor(
            id_comando=comando.id_comando, motor=MOTOR_TRADUCAO_ESTRATEGICA,
            modo_execucao=comando.modo_execucao,
            nivel_execucao=comando.nivel_execucao, estado_execucao=estado,
            resultado_principal=contrato,
            validacoes=(ValidacaoLocal(
                codigo="BRIEFING_CONCLUIDO",
                objeto_validado=str(briefing.id),
                resultado=ResultadoValidacao.VALIDO,
                severidade=Severidade.INFORMATIVA,
                mensagem="Briefing concluído aceito como contexto de entrada.",
            ),), alertas=alertas, confianca=contrato.confianca,
            explicacao={
                "conclusao_pratica": (
                    f"{len(contrato.objetivos_midia_derivados)} objetivos de "
                    "mídia derivados sem selecionar inventário."
                ),
                "principais_razoes": tuple(
                    item.regra for item in contrato.objetivos_midia_derivados
                ),
                "memoria_tecnica": {
                    "bibliotecas": (15, 17, 18),
                    "versao_nucleo": self.catalogo.versao,
                    "problemas": tuple(
                        item.codigo for item in contrato.problemas_identificados
                    ),
                },
            },
            rastreabilidade=Rastreabilidade(
                entradas_utilizadas=(referencia_briefing,),
                conhecimentos_aplicados=referencias_bibliotecas,
            ),
            dependencias=(Dependencia(
                referencia=referencia_briefing,
                tipo=TipoDependencia.ESTRATEGICA,
                recalcula_quando=(
                    "objetivo", "público", "praça", "jornada", "restrição",
                ),
            ),),
            reexecucao=PlanoReexecucao(
                politica=PoliticaReexecucao.RECALCULAR_PARCIALMENTE,
                motivo="reexecutar somente relações afetadas por mudança contextual",
                alvos=(MOTOR_TRADUCAO_ESTRATEGICA,),
            ), produzido_em=instante,
        )
