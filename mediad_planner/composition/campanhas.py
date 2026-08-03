from mediad_planner.application.services.aplicacao_campanhas import (
    AplicacaoCampanhas,
)
from mediad_planner.composition.ambiente import (
    construir_ambiente_aplicacao_em_memoria,
)


def construir_aplicacao_campanhas_em_memoria() -> AplicacaoCampanhas:
    return construir_ambiente_aplicacao_em_memoria().campanhas
