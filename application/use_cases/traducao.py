from uuid import uuid4

from domain.briefing import EstadoBriefing
from domain.contracts import ComandoMotor, NivelExecucao, ReferenciaVersionada
from domain.traducao import revisar_traducao
from engines.traducao_estrategica import (
    MOTOR_TRADUCAO_ESTRATEGICA, ModoTraducaoEstrategica,
)


class CriarTraducaoEstrategica:
    def __init__(self, *, relogio, autorizador, repositorio, motor):
        self.relogio = relogio
        self.autorizador = autorizador
        self.repositorio = repositorio
        self.motor = motor

    def executar(self, *, briefing_id, usuario_id):
        briefing = self.repositorio.obter_briefing(briefing_id)
        if briefing is None:
            raise LookupError("briefing não encontrado")
        if not self.autorizador.pode_editar(usuario_id, briefing.campanha_id):
            raise PermissionError("usuário não autorizado")
        if briefing.estado is not EstadoBriefing.CONCLUIDO:
            raise ValueError("briefing deve estar concluído")
        existente = self.repositorio.obter_traducao_por_briefing(briefing.id)
        if existente:
            raise ValueError("este briefing já possui tradução")
        instante = self.relogio.agora()
        comando = ComandoMotor(
            motor_destino=MOTOR_TRADUCAO_ESTRATEGICA,
            modo_execucao=ModoTraducaoEstrategica.TRADUZIR_BRIEFING,
            nivel_execucao=NivelExecucao.PREVIA,
            id_campanha=briefing.campanha_id,
            id_snapshot_campanha=briefing.campanha_id,
            id_usuario=usuario_id,
            perfil_de_acesso="PLANEJADOR",
            solicitado_em=instante,
            origem_do_comando="CriarTraducaoEstrategica",
            objetivo_da_execucao=(
                "Traduzir briefing em critérios estratégicos rastreáveis."
            ),
            referencias_de_entrada=(ReferenciaVersionada(
                id=str(briefing.id), tipo="BRIEFING",
                versao=str(briefing.versao), origem="campanha",
            ),),
            parametros_locais={"briefing": briefing, "contrato_id": uuid4()},
        )
        saida = self.motor.executar(comando)
        contrato = saida.resultado_principal.model_copy(update={
            "execucao_motor": saida.model_copy(
                update={"resultado_principal": None}
            )
        })
        self.repositorio.salvar_traducao(contrato)
        return contrato


class CriarNovaVersaoTraducao:
    def __init__(self, *, relogio, autorizador, repositorio):
        self.relogio = relogio
        self.autorizador = autorizador
        self.repositorio = repositorio

    def executar(
        self, *, briefing_id, usuario_id, categorias_aceitas, justificativa
    ):
        anterior = self.repositorio.obter_traducao_por_briefing(briefing_id)
        if anterior is None:
            raise LookupError("tradução não encontrada")
        if not self.autorizador.pode_editar(usuario_id, anterior.campanha_id):
            raise PermissionError("usuário não autorizado")
        nova = revisar_traducao(
            anterior, contrato_id=uuid4(),
            categorias_aceitas=tuple(categorias_aceitas),
            justificativa=justificativa, criado_por=usuario_id,
            criado_em=self.relogio.agora(),
        )
        self.repositorio.salvar_nova_versao_traducao(anterior, nova)
        return nova
