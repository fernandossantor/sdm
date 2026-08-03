import pytest

from mediad_planner.application.dto.catalogo_territorial import (
    EstadoCatalogoResumo,
    MunicipioCatalogoResumo,
)
from mediad_planner.application.services.aplicacao_catalogo_territorial import (
    AplicacaoCatalogoTerritorial,
)
from mediad_planner.application.use_cases.catalogo_territorial import (
    ListarEstadosCatalogoTerritorial,
    ListarMunicipiosCatalogoTerritorial,
)


class CatalogoFalso:
    def __init__(self) -> None:
        self.codigos: list[str] = []

    def listar_estados(self) -> tuple[EstadoCatalogoResumo, ...]:
        return (
            EstadoCatalogoResumo("43", "RS", "Zulu", None, None, None),
            EstadoCatalogoResumo("42", "SC", "águas", None, None, None),
        )

    def listar_municipios(self, codigo_estado: str) -> tuple[MunicipioCatalogoResumo, ...]:
        self.codigos.append(codigo_estado)
        return (
            MunicipioCatalogoResumo("4300002", "Zulu", codigo_estado),
            MunicipioCatalogoResumo("4300001", "Alfa", codigo_estado),
        )


def test_casos_ordenam_e_servico_delega() -> None:
    porta = CatalogoFalso()
    listar_estados = ListarEstadosCatalogoTerritorial(porta)
    listar_municipios = ListarMunicipiosCatalogoTerritorial(porta)
    aplicacao = AplicacaoCatalogoTerritorial(listar_estados, listar_municipios)
    assert [item.nome for item in aplicacao.listar_estados()] == ["Zulu", "águas"]
    assert [item.nome for item in aplicacao.listar_municipios("43")] == ["Alfa", "Zulu"]
    assert porta.codigos == ["43"]


@pytest.mark.parametrize("codigo", ["RS", "4", "043", "43.0", 43])
def test_codigo_invalido_falha_antes_da_porta(codigo: object) -> None:
    porta = CatalogoFalso()
    caso = ListarMunicipiosCatalogoTerritorial(porta)
    with pytest.raises(ValueError, match="Código de UF inválido"):
        caso.executar(codigo)  # type: ignore[arg-type]
    assert porta.codigos == []
