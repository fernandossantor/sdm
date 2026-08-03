from typing import Protocol, runtime_checkable

from mediad_planner.application.dto.catalogo_territorial import (
    EstadoCatalogoResumo,
    MunicipioCatalogoResumo,
    RegiaoGeograficaImediataCatalogoResumo,
    RegiaoGeograficaIntermediariaCatalogoResumo,
)


class CatalogoTerritorialIndisponivel(RuntimeError):
    pass


@runtime_checkable
class CatalogoTerritorial(Protocol):
    def listar_estados(self) -> tuple[EstadoCatalogoResumo, ...]: ...

    def listar_municipios(
        self,
        codigo_estado: str,
    ) -> tuple[MunicipioCatalogoResumo, ...]: ...


@runtime_checkable
class CatalogoRegioesGeograficas(Protocol):
    def listar_regioes_intermediarias(
        self,
        codigo_estado: str,
    ) -> tuple[RegiaoGeograficaIntermediariaCatalogoResumo, ...]: ...

    def listar_regioes_imediatas(
        self,
        codigo_regiao_intermediaria: str,
    ) -> tuple[RegiaoGeograficaImediataCatalogoResumo, ...]: ...
