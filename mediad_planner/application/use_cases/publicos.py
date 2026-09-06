from dataclasses import replace
from uuid import UUID

from mediad_planner.application.dto.briefing import BriefingResumo, ContextoAcessoBriefings
from mediad_planner.application.dto.publicos import SalvarPublicoEntrada
from mediad_planner.application.mappers.briefing import resumir_briefing
from mediad_planner.application.ports.repositorio_briefings import RepositorioBriefings
from mediad_planner.application.use_cases.briefings import (
    GeradorUUID,
    Relogio,
    _obter_briefing,
    _validar_autoria,
)
from mediad_planner.application.use_cases.praca_universo import _decimal_opcional
from mediad_planner.domain.briefing.praca_universo import PublicoDeclarado


class _SalvarPublico:
    def __init__(
        self, repositorio: RepositorioBriefings,
        contexto_acesso: ContextoAcessoBriefings, relogio: Relogio,
    ) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio

    def _publico(
        self, id_publico: UUID, entrada: SalvarPublicoEntrada,
    ) -> PublicoDeclarado:
        return PublicoDeclarado(
            id_publico=id_publico,
            nome=entrada.nome,
            ids_segmentos_origem=entrada.ids_segmentos_origem,
            ids_pracas=entrada.ids_pracas,
            prioridade=entrada.prioridade,
            intensidade_importancia=entrada.intensidade_importancia,
            tamanho_estimado=_decimal_opcional(entrada.tamanho_estimado),
            papel_declarado=entrada.papel_declarado,
            justificativa=entrada.justificativa,
        )


class AdicionarPublico(_SalvarPublico):
    def __init__(
        self, repositorio: RepositorioBriefings,
        contexto_acesso: ContextoAcessoBriefings, relogio: Relogio,
        gerador_uuid: GeradorUUID,
    ) -> None:
        super().__init__(repositorio, contexto_acesso, relogio)
        self._gerador_uuid = gerador_uuid

    def executar(
        self, id_campanha: UUID, entrada: SalvarPublicoEntrada,
    ) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(self._repositorio, self._contexto, id_campanha)
        atualizado = briefing.adicionar_publico(
            self._publico(self._gerador_uuid(), entrada),
            self._contexto.id_usuario,
            self._relogio(),
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)


class EditarPublico(_SalvarPublico):
    def executar(
        self, id_campanha: UUID, id_publico: UUID,
        entrada: SalvarPublicoEntrada,
    ) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(self._repositorio, self._contexto, id_campanha)
        atual = next((
            item for item in briefing.estrutura_territorial_populacional.publicos
            if item.id_publico == id_publico
        ), None)
        if atual is None:
            raise LookupError("Público não encontrado")
        atualizado = briefing.editar_publico(
            replace(self._publico(id_publico, entrada), jornada_aplicavel=atual.jornada_aplicavel),
            self._contexto.id_usuario,
            self._relogio(),
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)


class RemoverPublico:
    def __init__(self, repositorio, contexto_acesso, relogio) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio

    def executar(self, id_campanha: UUID, id_publico: UUID) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(self._repositorio, self._contexto, id_campanha)
        atualizado = briefing.remover_publico(
            id_publico, self._contexto.id_usuario, self._relogio()
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)
