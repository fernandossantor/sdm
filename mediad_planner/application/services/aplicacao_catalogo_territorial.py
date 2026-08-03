from mediad_planner.application.dto.catalogo_territorial import (
    EstadoCatalogoResumo,
    MunicipioCatalogoResumo,
)
from mediad_planner.application.use_cases.catalogo_territorial import (
    ListarEstadosCatalogoTerritorial,
    ListarMunicipiosCatalogoTerritorial,
)


class AplicacaoCatalogoTerritorial:
    def __init__(
        self,
        listar_estados: ListarEstadosCatalogoTerritorial,
        listar_municipios: ListarMunicipiosCatalogoTerritorial,
    ) -> None:
        self._listar_estados = listar_estados
        self._listar_municipios = listar_municipios

    def listar_estados(self) -> tuple[EstadoCatalogoResumo, ...]:
        return self._listar_estados.executar()

    def listar_municipios(
        self,
        codigo_estado: str,
    ) -> tuple[MunicipioCatalogoResumo, ...]:
        return self._listar_municipios.executar(codigo_estado)
