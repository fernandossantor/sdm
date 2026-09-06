from uuid import UUID

from mediad_planner.application.dto.briefing import BriefingResumo, ContextoAcessoBriefings
from mediad_planner.application.dto.condicoes_declaradas import (
    DefinirInexistenciaRestricoesEntrada,
    DefinicaoCategoriaResumo,
    SalvarPretensaoEntrada,
    SalvarPrioridadeEntrada,
    SalvarRestricaoEntrada,
)
from mediad_planner.application.mappers.briefing import resumir_briefing
from mediad_planner.application.ports.repositorio_briefings import RepositorioBriefings
from mediad_planner.application.use_cases.briefings import GeradorUUID, Relogio, _obter_briefing, _validar_autoria
from mediad_planner.domain.briefing.condicoes_declaradas import (
    CategoriaPretensao,
    CategoriaRestricao,
    PretensaoDeclarada,
    PrioridadeContextual,
    RestricaoDeclarada,
    ROTULOS_PRETENSOES,
    ROTULOS_RESTRICOES,
    TipoEntidadePrioridade,
)


class GerenciarCondicoesDeclaradas:
    def __init__(
        self, repositorio: RepositorioBriefings,
        contexto_acesso: ContextoAcessoBriefings, relogio: Relogio,
        gerador_uuid: GeradorUUID,
    ) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio
        self._gerador_uuid = gerador_uuid

    def listar_restricoes(self):
        return tuple(DefinicaoCategoriaResumo(item.value, ROTULOS_RESTRICOES[item]) for item in CategoriaRestricao)

    def listar_pretensoes(self):
        return tuple(DefinicaoCategoriaResumo(item.value, ROTULOS_PRETENSOES[item]) for item in CategoriaPretensao)

    def _briefing(self, id_campanha):
        _validar_autoria(self._contexto)
        return _obter_briefing(self._repositorio, self._contexto, id_campanha)

    def _salvar(self, briefing):
        self._repositorio.salvar(briefing)
        return resumir_briefing(briefing)

    def salvar_prioridade(
        self, id_campanha: UUID, entrada: SalvarPrioridadeEntrada,
        id_prioridade: UUID | None = None,
    ) -> BriefingResumo:
        briefing = self._briefing(id_campanha)
        try:
            tipo = TipoEntidadePrioridade(entrada.tipo_entidade)
        except ValueError as erro:
            raise ValueError("Tipo de entidade priorizada inválido") from erro
        item = PrioridadeContextual(
            id_prioridade or self._gerador_uuid(), tipo, entrada.id_entidade,
            entrada.prioridade, entrada.ordem, entrada.justificativa,
        )
        return self._salvar(briefing.salvar_prioridade(
            item, id_prioridade is not None, self._contexto.id_usuario, self._relogio()
        ))

    def remover_prioridade(self, id_campanha, identificador):
        briefing = self._briefing(id_campanha)
        return self._salvar(briefing.remover_prioridade(
            identificador, self._contexto.id_usuario, self._relogio()
        ))

    def salvar_restricao(
        self, id_campanha: UUID, entrada: SalvarRestricaoEntrada,
        id_restricao: UUID | None = None,
    ) -> BriefingResumo:
        briefing = self._briefing(id_campanha)
        try:
            categoria = CategoriaRestricao(entrada.categoria)
        except ValueError as erro:
            raise ValueError("Categoria de restrição inválida") from erro
        item = RestricaoDeclarada(
            id_restricao or self._gerador_uuid(), categoria, entrada.descricao,
            entrada.entidade_afetada, entrada.intensidade, entrada.prioridade,
            entrada.origem, entrada.justificativa, entrada.documento_fonte,
            entrada.observacao,
        )
        return self._salvar(briefing.salvar_restricao(
            item, id_restricao is not None, self._contexto.id_usuario, self._relogio()
        ))

    def remover_restricao(self, id_campanha, identificador):
        briefing = self._briefing(id_campanha)
        return self._salvar(briefing.remover_restricao(
            identificador, self._contexto.id_usuario, self._relogio()
        ))

    def definir_inexistencia_restricoes(
        self, id_campanha: UUID, entrada: DefinirInexistenciaRestricoesEntrada,
    ) -> BriefingResumo:
        briefing = self._briefing(id_campanha)
        return self._salvar(briefing.definir_inexistencia_restricoes(
            entrada.declarada, self._contexto.id_usuario, self._relogio(),
        ))

    def salvar_pretensao(
        self, id_campanha: UUID, entrada: SalvarPretensaoEntrada,
        id_pretensao: UUID | None = None,
    ) -> BriefingResumo:
        briefing = self._briefing(id_campanha)
        try:
            categoria = CategoriaPretensao(entrada.categoria)
        except ValueError as erro:
            raise ValueError("Categoria de pretensão inválida") from erro
        item = PretensaoDeclarada(
            id_pretensao or self._gerador_uuid(), categoria,
            entrada.descricao_controlada, entrada.prioridade, entrada.intensidade,
            entrada.id_publico, entrada.id_praca, entrada.id_etapa_jornada,
            entrada.periodo_associado, entrada.flexibilidade_declarada,
            entrada.justificativa,
        )
        return self._salvar(briefing.salvar_pretensao(
            item, id_pretensao is not None, self._contexto.id_usuario, self._relogio()
        ))

    def remover_pretensao(self, id_campanha, identificador):
        briefing = self._briefing(id_campanha)
        return self._salvar(briefing.remover_pretensao(
            identificador, self._contexto.id_usuario, self._relogio()
        ))
