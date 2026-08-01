"""Edição em rascunho e criação rastreável de versões do Briefing."""

from uuid import uuid4

from application.dto.briefing import CriarVersaoBriefingEntrada, EditarBriefingEntrada
from domain.briefing import BriefingInicial, EstadoBriefing


class EditarBriefing:
    def __init__(self, *, relogio, autorizador, repositorio):
        self.relogio = relogio
        self.autorizador = autorizador
        self.repositorio = repositorio

    def executar(self, entrada: EditarBriefingEntrada) -> BriefingInicial:
        anterior = self.repositorio.obter_briefing(entrada.briefing_id)
        if anterior is None:
            raise LookupError("briefing não encontrado")
        if not self.autorizador.pode_editar(entrada.usuario_id, anterior.campanha_id):
            raise PermissionError("usuário não autorizado a editar briefing")
        if anterior.estado not in {EstadoBriefing.RASCUNHO, EstadoBriefing.EM_PREENCHIMENTO}:
            raise ValueError("este estado exige a criação de uma nova versão")
        if not entrada.motivo.strip():
            raise ValueError("motivo da alteração é obrigatório")
        atualizado = anterior.model_copy(update={
            "conteudo": entrada.conteudo,
            "estado": EstadoBriefing.EM_PREENCHIMENTO,
            "atualizado_por": entrada.usuario_id,
            "atualizado_em": self.relogio.agora(),
            "motivo_ultima_alteracao": entrada.motivo.strip(),
        })
        self.repositorio.salvar_edicao(anterior, atualizado, entrada.motivo.strip())
        return atualizado


class CriarNovaVersaoBriefing:
    def __init__(self, *, relogio, autorizador, repositorio):
        self.relogio = relogio
        self.autorizador = autorizador
        self.repositorio = repositorio

    def executar(self, entrada: CriarVersaoBriefingEntrada) -> BriefingInicial:
        anterior = self.repositorio.obter_briefing(entrada.briefing_id_origem)
        if anterior is None:
            raise LookupError("briefing de origem não encontrado")
        if not self.autorizador.pode_editar(entrada.usuario_id, anterior.campanha_id):
            raise PermissionError("usuário não autorizado a versionar briefing")
        if not entrada.motivo.strip():
            raise ValueError("motivo da nova versão é obrigatório")
        agora = self.relogio.agora()
        nova = BriefingInicial(
            id=uuid4(), campanha_id=anterior.campanha_id,
            versao=anterior.versao + 1,
            estado=EstadoBriefing.EM_PREENCHIMENTO,
            criado_por=entrada.usuario_id, criado_em=agora,
            conteudo=entrada.conteudo,
            atualizado_por=entrada.usuario_id, atualizado_em=agora,
            motivo_ultima_alteracao=entrada.motivo.strip(),
        )
        self.repositorio.salvar_nova_versao(anterior, nova, entrada.motivo.strip())
        return nova
