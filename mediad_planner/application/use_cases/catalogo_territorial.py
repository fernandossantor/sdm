from mediad_planner.application.dto.catalogo_territorial import (
    EstadoCatalogoResumo,
    MunicipioCatalogoResumo,
)
from mediad_planner.application.ports.catalogo_territorial import CatalogoTerritorial


class ListarEstadosCatalogoTerritorial:
    def __init__(self, catalogo: CatalogoTerritorial) -> None:
        self._catalogo = catalogo

    def executar(self) -> tuple[EstadoCatalogoResumo, ...]:
        return tuple(sorted(self._catalogo.listar_estados(), key=lambda item: item.nome.casefold()))


class ListarMunicipiosCatalogoTerritorial:
    def __init__(self, catalogo: CatalogoTerritorial) -> None:
        self._catalogo = catalogo

    def executar(self, codigo_estado: str) -> tuple[MunicipioCatalogoResumo, ...]:
        if (
            not isinstance(codigo_estado, str)
            or len(codigo_estado) != 2
            or not codigo_estado.isdigit()
        ):
            raise ValueError("Código de UF inválido")
        return tuple(
            sorted(
                self._catalogo.listar_municipios(codigo_estado),
                key=lambda item: item.nome.casefold(),
            )
        )
