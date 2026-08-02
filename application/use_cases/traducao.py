from uuid import uuid4

from domain.briefing import EstadoBriefing
from domain.traducao import revisar_traducao, traduzir_briefing


class CriarTraducaoEstrategica:
    def __init__(self, *, relogio, autorizador, repositorio):
        self.relogio = relogio
        self.autorizador = autorizador
        self.repositorio = repositorio

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
        contrato = traduzir_briefing(
            briefing, contrato_id=uuid4(), criado_por=usuario_id,
            criado_em=self.relogio.agora(),
        )
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
