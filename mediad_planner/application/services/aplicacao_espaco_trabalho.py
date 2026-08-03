from uuid import UUID

from mediad_planner.application.dto.espaco_trabalho import (
    EspacoTrabalhoCampanhaResumo,
)
from mediad_planner.application.use_cases.espaco_trabalho import (
    ObterEspacoTrabalhoCampanha,
    PrepararBriefingCampanha,
)


class AplicacaoEspacoTrabalho:
    def __init__(
        self,
        obter: ObterEspacoTrabalhoCampanha,
        preparar: PrepararBriefingCampanha,
    ) -> None:
        self._obter = obter
        self._preparar = preparar

    def obter_espaco_trabalho(
        self,
        id_campanha: UUID,
    ) -> EspacoTrabalhoCampanhaResumo:
        return self._obter.executar(id_campanha)

    def preparar_briefing(
        self,
        id_campanha: UUID,
    ) -> EspacoTrabalhoCampanhaResumo:
        return self._preparar.executar(id_campanha)
