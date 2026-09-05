from uuid import UUID

from mediad_planner.application.dto.briefing import BriefingResumo, ContextoAcessoBriefings
from mediad_planner.application.dto.segmentos import SalvarSegmentoEntrada
from mediad_planner.application.mappers.briefing import resumir_briefing
from mediad_planner.application.ports.repositorio_briefings import RepositorioBriefings
from mediad_planner.application.use_cases.briefings import (
    GeradorUUID,
    Relogio,
    _obter_briefing,
    _validar_autoria,
)
from mediad_planner.application.use_cases.praca_universo import _decimal_opcional
from mediad_planner.domain.briefing.praca_universo import (
    CriterioSegmentacao,
    SegmentoDeclarado,
)


class _SalvarSegmento:
    def __init__(
        self,
        repositorio: RepositorioBriefings,
        contexto_acesso: ContextoAcessoBriefings,
        relogio: Relogio,
    ) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio

    def _segmento(
        self, id_segmento: UUID, entrada: SalvarSegmentoEntrada,
    ) -> SegmentoDeclarado:
        try:
            criterios = tuple(
                CriterioSegmentacao(item) for item in entrada.criterios_aplicados
            )
        except ValueError as erro:
            raise ValueError("Critério de segmentação inválido") from erro
        return SegmentoDeclarado(
            id_segmento=id_segmento,
            id_universo_origem=entrada.id_universo_origem,
            ids_pracas=entrada.ids_pracas,
            criterios_aplicados=criterios,
            definicao=entrada.definicao,
            tamanho_estimado=_decimal_opcional(entrada.tamanho_estimado),
            fonte=entrada.fonte,
            data_referencia=entrada.data_referencia,
        )


class AdicionarSegmento(_SalvarSegmento):
    def __init__(
        self,
        repositorio: RepositorioBriefings,
        contexto_acesso: ContextoAcessoBriefings,
        relogio: Relogio,
        gerador_uuid: GeradorUUID,
    ) -> None:
        super().__init__(repositorio, contexto_acesso, relogio)
        self._gerador_uuid = gerador_uuid

    def executar(
        self, id_campanha: UUID, entrada: SalvarSegmentoEntrada,
    ) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(self._repositorio, self._contexto, id_campanha)
        atualizado = briefing.adicionar_segmento(
            self._segmento(self._gerador_uuid(), entrada),
            self._contexto.id_usuario,
            self._relogio(),
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)


class EditarSegmento(_SalvarSegmento):
    def executar(
        self,
        id_campanha: UUID,
        id_segmento: UUID,
        entrada: SalvarSegmentoEntrada,
    ) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(self._repositorio, self._contexto, id_campanha)
        atualizado = briefing.editar_segmento(
            self._segmento(id_segmento, entrada),
            self._contexto.id_usuario,
            self._relogio(),
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)


class RemoverSegmento:
    def __init__(self, repositorio, contexto_acesso, relogio) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio

    def executar(self, id_campanha: UUID, id_segmento: UUID) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(self._repositorio, self._contexto, id_campanha)
        atualizado = briefing.remover_segmento(
            id_segmento, self._contexto.id_usuario, self._relogio()
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)
