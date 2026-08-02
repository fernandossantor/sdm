from uuid import UUID

from mediad_planner.application.dto.campanha import (
    CampanhaResumo,
    CriarCampanhaEntrada,
)
from mediad_planner.application.use_cases.campanhas import (
    CriarCampanha,
    IniciarBriefingCampanha,
    ListarCampanhas,
)


class AplicacaoCampanhas:
    def __init__(
        self,
        criar: CriarCampanha,
        iniciar_briefing: IniciarBriefingCampanha,
        listar: ListarCampanhas,
    ) -> None:
        self._criar = criar
        self._iniciar_briefing = iniciar_briefing
        self._listar = listar

    def criar_campanha(self, entrada: CriarCampanhaEntrada) -> CampanhaResumo:
        return self._criar.executar(entrada)

    def iniciar_briefing(self, id_campanha: UUID) -> CampanhaResumo:
        return self._iniciar_briefing.executar(id_campanha)

    def listar_campanhas(self) -> tuple[CampanhaResumo, ...]:
        return self._listar.executar()
