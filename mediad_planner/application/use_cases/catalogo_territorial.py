from mediad_planner.application.dto.catalogo_territorial import (
    EstadoCatalogoResumo,
    MunicipioCatalogoResumo,
    RegiaoGeograficaImediataCatalogoResumo,
    RegiaoGeograficaIntermediariaCatalogoResumo,
)
from mediad_planner.application.ports.catalogo_territorial import (
    CatalogoRegioesGeograficas,
    CatalogoTerritorial,
)


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


class ListarRegioesIntermediariasCatalogoTerritorial:
    def __init__(self, catalogo: CatalogoRegioesGeograficas) -> None:
        self._catalogo = catalogo

    def executar(
        self,
        codigo_estado: str,
    ) -> tuple[RegiaoGeograficaIntermediariaCatalogoResumo, ...]:
        if (
            not isinstance(codigo_estado, str)
            or len(codigo_estado) != 2
            or not codigo_estado.isdigit()
        ):
            raise ValueError("Código de UF inválido")
        return tuple(
            sorted(
                self._catalogo.listar_regioes_intermediarias(codigo_estado),
                key=lambda item: (item.nome.casefold(), item.codigo),
            )
        )


class ListarRegioesImediatasCatalogoTerritorial:
    def __init__(self, catalogo: CatalogoRegioesGeograficas) -> None:
        self._catalogo = catalogo

    def executar(
        self,
        codigo_regiao_intermediaria: str,
    ) -> tuple[RegiaoGeograficaImediataCatalogoResumo, ...]:
        if (
            not isinstance(codigo_regiao_intermediaria, str)
            or len(codigo_regiao_intermediaria) != 4
            or not codigo_regiao_intermediaria.isdigit()
        ):
            raise ValueError(
                "Código de Região Geográfica Intermediária inválido"
            )
        return tuple(
            sorted(
                self._catalogo.listar_regioes_imediatas(
                    codigo_regiao_intermediaria
                ),
                key=lambda item: (item.nome.casefold(), item.codigo),
            )
        )
