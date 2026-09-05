from uuid import UUID

from mediad_planner.application.dto.briefing import (
    BriefingResumo,
    ContextoAcessoBriefings,
)
from mediad_planner.application.dto.criterios_segmentacao import (
    DefinicaoCriterioSegmentacaoResumo,
    DefinirCriteriosSegmentacaoEntrada,
)
from mediad_planner.application.mappers.briefing import resumir_briefing
from mediad_planner.application.ports.repositorio_briefings import RepositorioBriefings
from mediad_planner.application.use_cases.briefings import (
    Relogio,
    _obter_briefing,
    _validar_autoria,
)
from mediad_planner.domain.briefing.praca_universo import (
    CriterioSegmentacao,
    listar_criterios_segmentacao,
)


class ListarCriteriosSegmentacao:
    def executar(self) -> tuple[DefinicaoCriterioSegmentacaoResumo, ...]:
        return tuple(
            DefinicaoCriterioSegmentacaoResumo(item.codigo.value, item.rotulo)
            for item in listar_criterios_segmentacao()
        )


class DefinirCriteriosSegmentacao:
    def __init__(
        self,
        repositorio: RepositorioBriefings,
        contexto_acesso: ContextoAcessoBriefings,
        relogio: Relogio,
    ) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio

    def executar(
        self,
        id_campanha: UUID,
        entrada: DefinirCriteriosSegmentacaoEntrada,
    ) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(self._repositorio, self._contexto, id_campanha)
        try:
            criterios = tuple(CriterioSegmentacao(item) for item in entrada.codigos)
        except ValueError as erro:
            raise ValueError("Critério de segmentação inválido") from erro
        atualizado = briefing.definir_criterios_segmentacao(
            criterios,
            self._contexto.id_usuario,
            self._relogio(),
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)
