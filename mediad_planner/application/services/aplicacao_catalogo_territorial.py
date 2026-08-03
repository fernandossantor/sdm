from mediad_planner.application.dto.catalogo_territorial import (
    EstadoCatalogoResumo,
    MunicipioCatalogoResumo,
    RegiaoGeograficaImediataCatalogoResumo,
    RegiaoGeograficaIntermediariaCatalogoResumo,
)
from mediad_planner.application.use_cases.catalogo_territorial import (
    ListarEstadosCatalogoTerritorial,
    ListarMunicipiosCatalogoTerritorial,
    ListarRegioesImediatasCatalogoTerritorial,
    ListarRegioesIntermediariasCatalogoTerritorial,
)


class AplicacaoCatalogoTerritorial:
    def __init__(
        self,
        listar_estados: ListarEstadosCatalogoTerritorial,
        listar_municipios: ListarMunicipiosCatalogoTerritorial,
        listar_regioes_intermediarias: (
            ListarRegioesIntermediariasCatalogoTerritorial
        ),
        listar_regioes_imediatas: ListarRegioesImediatasCatalogoTerritorial,
    ) -> None:
        self._listar_estados = listar_estados
        self._listar_municipios = listar_municipios
        self._listar_regioes_intermediarias = listar_regioes_intermediarias
        self._listar_regioes_imediatas = listar_regioes_imediatas

    def listar_estados(self) -> tuple[EstadoCatalogoResumo, ...]:
        return self._listar_estados.executar()

    def listar_municipios(
        self,
        codigo_estado: str,
    ) -> tuple[MunicipioCatalogoResumo, ...]:
        return self._listar_municipios.executar(codigo_estado)


    def listar_regioes_intermediarias(
        self,
        codigo_estado: str,
    ) -> tuple[RegiaoGeograficaIntermediariaCatalogoResumo, ...]:
        return self._listar_regioes_intermediarias.executar(codigo_estado)

    def listar_regioes_imediatas(
        self,
        codigo_regiao_intermediaria: str,
    ) -> tuple[RegiaoGeograficaImediataCatalogoResumo, ...]:
        return self._listar_regioes_imediatas.executar(
            codigo_regiao_intermediaria
        )
