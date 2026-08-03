from mediad_planner.application.services.aplicacao_catalogo_territorial import (
    AplicacaoCatalogoTerritorial,
)
from mediad_planner.application.use_cases.catalogo_territorial import (
    ListarEstadosCatalogoTerritorial,
    ListarMunicipiosCatalogoTerritorial,
)
from mediad_planner.infrastructure.ibge.catalogo_territorial_local import (
    CatalogoTerritorialLocal,
)


def construir_aplicacao_catalogo_territorial() -> AplicacaoCatalogoTerritorial:
    catalogo = CatalogoTerritorialLocal()
    return AplicacaoCatalogoTerritorial(
        listar_estados=ListarEstadosCatalogoTerritorial(catalogo),
        listar_municipios=ListarMunicipiosCatalogoTerritorial(catalogo),
    )
