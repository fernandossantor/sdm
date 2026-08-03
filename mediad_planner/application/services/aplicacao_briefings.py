from uuid import UUID

from mediad_planner.application.dto.briefing import BriefingResumo
from mediad_planner.application.use_cases.briefings import AbrirBriefingCampanha


class AplicacaoBriefings:
    def __init__(self, abrir: AbrirBriefingCampanha) -> None:
        self._abrir = abrir

    def abrir_briefing(self, id_campanha: UUID) -> BriefingResumo:
        return self._abrir.executar(id_campanha)
