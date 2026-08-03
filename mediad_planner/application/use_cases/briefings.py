from collections.abc import Callable
from datetime import datetime
from uuid import UUID

from mediad_planner.application.dto.briefing import (
    BriefingResumo,
    ContextoAcessoBriefings,
)
from mediad_planner.application.ports.repositorio_briefings import (
    RepositorioBriefings,
)
from mediad_planner.application.ports.repositorio_campanhas import (
    RepositorioCampanhas,
)
from mediad_planner.domain.briefing.contexto import ContextoHerdadoBriefing
from mediad_planner.domain.briefing.entidades import Briefing
from mediad_planner.domain.campanha.enums import EtapaCampanha, SituacaoCampanha
from mediad_planner.domain.common.enums import PapelAcesso


Relogio = Callable[[], datetime]
GeradorUUID = Callable[[], UUID]


def _resumir(briefing: Briefing) -> BriefingResumo:
    contexto = briefing.contexto_herdado
    return BriefingResumo(
        id_briefing=briefing.id_briefing,
        id_campanha=briefing.id_campanha,
        numero_versao=briefing.numero_versao,
        estado=briefing.estado.value,
        codigo_campanha=contexto.codigo_campanha.valor,
        nome_campanha=contexto.nome_campanha,
        anunciante=contexto.anunciante.nome_snapshot,
        marca=contexto.marca.nome_snapshot if contexto.marca else None,
        produto_servico=(
            contexto.produto_servico.nome_snapshot
            if contexto.produto_servico
            else None
        ),
        planejador_responsavel=contexto.planejador_responsavel.nome_snapshot,
        equipe=tuple(item.nome_snapshot for item in contexto.equipe),
        criado_em=briefing.criado_em,
        atualizado_em=briefing.atualizado_em,
    )


class AbrirBriefingCampanha:
    def __init__(
        self,
        repositorio_campanhas: RepositorioCampanhas,
        repositorio_briefings: RepositorioBriefings,
        contexto_acesso: ContextoAcessoBriefings,
        relogio: Relogio,
        gerador_uuid: GeradorUUID,
    ) -> None:
        self._repositorio_campanhas = repositorio_campanhas
        self._repositorio_briefings = repositorio_briefings
        self._contexto = contexto_acesso
        self._relogio = relogio
        self._gerador_uuid = gerador_uuid

    def executar(self, id_campanha: UUID) -> BriefingResumo:
        papeis_consulta = (
            PapelAcesso.PROPRIETARIO,
            PapelAcesso.EDITOR,
            PapelAcesso.LEITOR,
        )
        if self._contexto.papel not in papeis_consulta:
            raise PermissionError("Papel sem permissão para abrir Briefings")
        campanha = self._repositorio_campanhas.obter(
            self._contexto.id_espaco_trabalho,
            id_campanha,
        )
        if campanha is None:
            raise LookupError("Campanha não encontrada no espaço atual")
        if (
            campanha.situacao is not SituacaoCampanha.EM_ANDAMENTO
            or campanha.etapa_atual is not EtapaCampanha.BRIEFING
        ):
            raise ValueError("Campanha não está na etapa de Briefing")
        existente = self._repositorio_briefings.obter_por_campanha(
            self._contexto.id_espaco_trabalho,
            id_campanha,
        )
        if existente is not None:
            return _resumir(existente)
        if self._contexto.papel is PapelAcesso.LEITOR:
            raise PermissionError("Leitor não pode criar a versão inicial do Briefing")

        contexto_herdado = ContextoHerdadoBriefing(
            codigo_campanha=campanha.codigo,
            nome_campanha=campanha.nome,
            anunciante=campanha.anunciante,
            marca=campanha.marca,
            produto_servico=campanha.produto_servico,
            planejador_responsavel=campanha.planejador_responsavel,
            equipe=campanha.equipe,
        )
        agora = self._relogio()
        briefing = Briefing.criar_versao_inicial(
            id_briefing=self._gerador_uuid(),
            id_campanha=campanha.id_campanha,
            id_espaco_trabalho=campanha.id_espaco_trabalho,
            contexto_herdado=contexto_herdado,
            criado_por=self._contexto.id_usuario,
            criado_em=agora,
            atualizado_por=self._contexto.id_usuario,
            atualizado_em=agora,
        )
        self._repositorio_briefings.salvar(briefing)
        return _resumir(briefing)
