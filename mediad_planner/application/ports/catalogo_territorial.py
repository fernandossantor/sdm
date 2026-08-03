from typing import Protocol, runtime_checkable

from mediad_planner.application.dto.catalogo_territorial import (
    EstadoCatalogoResumo,
    MunicipioCatalogoResumo,
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
