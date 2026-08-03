from threading import RLock
from uuid import UUID

from mediad_planner.domain.briefing.entidades import Briefing
from mediad_planner.domain.briefing.enums import EstadoBriefing


class RepositorioBriefingsEmMemoria:
    def __init__(self) -> None:
        self._briefings: dict[tuple[UUID, UUID], Briefing] = {}
        self._lock = RLock()

    def salvar(self, briefing: Briefing) -> None:
        chave = (briefing.id_espaco_trabalho, briefing.id_campanha)
        with self._lock:
            for outra_chave, outro in self._briefings.items():
                if outro.id_briefing == briefing.id_briefing and outra_chave != chave:
                    raise ValueError("id_briefing já pertence a outra Campanha")
            existente = self._briefings.get(chave)
            if existente is not None:
                if existente.id_briefing != briefing.id_briefing:
                    raise ValueError("Campanha já possui Briefing corrente")
                if existente.id_campanha != briefing.id_campanha:
                    raise ValueError("Briefing não pode mudar de Campanha")
                if existente.id_espaco_trabalho != briefing.id_espaco_trabalho:
                    raise ValueError("Briefing não pode mudar de espaço")
                if existente.numero_versao != briefing.numero_versao:
                    raise ValueError("numero_versao atual não pode ser alterado")
                if existente.contexto_herdado != briefing.contexto_herdado:
                    raise ValueError("contexto herdado não pode ser alterado")
                if existente.criado_por != briefing.criado_por:
                    raise ValueError("criado_por não pode ser alterado")
                if existente.criado_em != briefing.criado_em:
                    raise ValueError("criado_em não pode ser alterado")
                if briefing.atualizado_em < existente.atualizado_em:
                    raise ValueError("atualizado_em não pode regredir")
                if (
                    existente.estado is EstadoBriefing.EM_PREENCHIMENTO
                    and briefing.estado is EstadoBriefing.RASCUNHO
                ):
                    raise ValueError("estado não pode retornar a RASCUNHO")
            if briefing.estado not in (
                EstadoBriefing.RASCUNHO,
                EstadoBriefing.EM_PREENCHIMENTO,
            ):
                raise ValueError("estado ainda não suportado")
            self._briefings[chave] = briefing

    def obter_por_campanha(
        self,
        id_espaco_trabalho: UUID,
        id_campanha: UUID,
    ) -> Briefing | None:
        with self._lock:
            return self._briefings.get((id_espaco_trabalho, id_campanha))
