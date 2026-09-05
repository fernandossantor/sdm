from uuid import UUID

from mediad_planner.application.dto.briefing import BriefingResumo, ContextoAcessoBriefings
from mediad_planner.application.dto.jornada import (
    CategoriaEtapaJornadaResumo,
    SalvarEtapaJornadaEntrada,
    SalvarJornadaEntrada,
)
from mediad_planner.application.mappers.briefing import resumir_briefing
from mediad_planner.application.ports.repositorio_briefings import RepositorioBriefings
from mediad_planner.application.use_cases.briefings import (
    GeradorUUID, Relogio, _obter_briefing, _validar_autoria,
)
from mediad_planner.domain.briefing.jornada import (
    CategoriaEtapaJornada, EtapaJornadaDeclarada, JornadaDeclarada, ROTULOS_ETAPAS,
)


class ListarCategoriasEtapaJornada:
    def executar(self) -> tuple[CategoriaEtapaJornadaResumo, ...]:
        return tuple(
            CategoriaEtapaJornadaResumo(item.value, ROTULOS_ETAPAS[item])
            for item in CategoriaEtapaJornada
        )


class _Base:
    def __init__(self, repositorio, contexto_acesso, relogio) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio

    def _briefing(self, id_campanha: UUID):
        _validar_autoria(self._contexto)
        return _obter_briefing(self._repositorio, self._contexto, id_campanha)

    def _salvar(self, briefing) -> BriefingResumo:
        self._repositorio.salvar(briefing)
        return resumir_briefing(briefing)


class AdicionarJornada(_Base):
    def __init__(self, repositorio, contexto_acesso, relogio, gerador_uuid: GeradorUUID):
        super().__init__(repositorio, contexto_acesso, relogio)
        self._gerador_uuid = gerador_uuid

    def executar(self, id_campanha: UUID, entrada: SalvarJornadaEntrada) -> BriefingResumo:
        briefing = self._briefing(id_campanha)
        jornada = JornadaDeclarada(
            self._gerador_uuid(), entrada.nome, entrada.descricao,
            entrada.ids_publicos, entrada.referencia_modelo,
            entrada.adaptada_localmente,
        )
        return self._salvar(briefing.adicionar_jornada(
            jornada, self._contexto.id_usuario, self._relogio()
        ))


class EditarJornada(_Base):
    def executar(
        self, id_campanha: UUID, id_jornada: UUID, entrada: SalvarJornadaEntrada,
    ) -> BriefingResumo:
        briefing = self._briefing(id_campanha)
        atual = next((item for item in briefing.jornadas if item.id_jornada == id_jornada), None)
        if atual is None:
            raise LookupError("Jornada não encontrada")
        jornada = JornadaDeclarada(
            id_jornada, entrada.nome, entrada.descricao, entrada.ids_publicos,
            entrada.referencia_modelo, entrada.adaptada_localmente, atual.etapas,
        )
        return self._salvar(briefing.editar_jornada(
            jornada, self._contexto.id_usuario, self._relogio()
        ))


class RemoverJornada(_Base):
    def executar(self, id_campanha: UUID, id_jornada: UUID) -> BriefingResumo:
        briefing = self._briefing(id_campanha)
        return self._salvar(briefing.remover_jornada(
            id_jornada, self._contexto.id_usuario, self._relogio()
        ))


class _SalvarEtapa(_Base):
    def _etapa(
        self, id_etapa: UUID, entrada: SalvarEtapaJornadaEntrada,
    ) -> EtapaJornadaDeclarada:
        try:
            categoria = CategoriaEtapaJornada(entrada.categoria)
        except ValueError as erro:
            raise ValueError("Categoria de etapa inválida") from erro
        return EtapaJornadaDeclarada(
            id_etapa, categoria, entrada.ordem, entrada.existe,
            entrada.relevancia, entrada.intensidade, entrada.prioridade,
            entrada.ids_publicos, entrada.ids_objetivos_comunicacao,
            entrada.situacao_atual, entrada.situacao_pretendida, entrada.observacao,
        )


class AdicionarEtapaJornada(_SalvarEtapa):
    def __init__(self, repositorio, contexto_acesso, relogio, gerador_uuid: GeradorUUID):
        super().__init__(repositorio, contexto_acesso, relogio)
        self._gerador_uuid = gerador_uuid

    def executar(
        self, id_campanha: UUID, id_jornada: UUID,
        entrada: SalvarEtapaJornadaEntrada,
    ) -> BriefingResumo:
        briefing = self._briefing(id_campanha)
        return self._salvar(briefing.salvar_etapa_jornada(
            id_jornada, self._etapa(self._gerador_uuid(), entrada), False,
            self._contexto.id_usuario, self._relogio(),
        ))


class EditarEtapaJornada(_SalvarEtapa):
    def executar(
        self, id_campanha: UUID, id_jornada: UUID, id_etapa: UUID,
        entrada: SalvarEtapaJornadaEntrada,
    ) -> BriefingResumo:
        briefing = self._briefing(id_campanha)
        return self._salvar(briefing.salvar_etapa_jornada(
            id_jornada, self._etapa(id_etapa, entrada), True,
            self._contexto.id_usuario, self._relogio(),
        ))


class RemoverEtapaJornada(_Base):
    def executar(
        self, id_campanha: UUID, id_jornada: UUID, id_etapa: UUID,
    ) -> BriefingResumo:
        briefing = self._briefing(id_campanha)
        return self._salvar(briefing.remover_etapa_jornada(
            id_jornada, id_etapa, self._contexto.id_usuario, self._relogio()
        ))
