import pytest

from mediad_planner.application.dto.catalogo_territorial import (
    EstadoCatalogoResumo,
    MunicipioCatalogoResumo,
    RegiaoGeograficaImediataCatalogoResumo,
    RegiaoGeograficaIntermediariaCatalogoResumo,
)
from mediad_planner.application.services.aplicacao_catalogo_territorial import (
    AplicacaoCatalogoTerritorial,
)
from mediad_planner.application.use_cases.catalogo_territorial import (
    ListarEstadosCatalogoTerritorial,
    ListarMunicipiosCatalogoTerritorial,
    ListarRegioesImediatasCatalogoTerritorial,
    ListarRegioesIntermediariasCatalogoTerritorial,
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


    def listar_regioes_intermediarias(
        self,
        codigo_estado: str,
    ) -> tuple[RegiaoGeograficaIntermediariaCatalogoResumo, ...]:
        self.codigos.append(codigo_estado)
        return (
            RegiaoGeograficaIntermediariaCatalogoResumo(
                "4304", "Zulu", codigo_estado
            ),
            RegiaoGeograficaIntermediariaCatalogoResumo(
                "4303", "Alfa", codigo_estado
            ),
        )

    def listar_regioes_imediatas(
        self,
        codigo_regiao_intermediaria: str,
    ) -> tuple[RegiaoGeograficaImediataCatalogoResumo, ...]:
        self.codigos.append(codigo_regiao_intermediaria)
        return (
            RegiaoGeograficaImediataCatalogoResumo(
                "430017", "Zulu", "43", codigo_regiao_intermediaria
            ),
            RegiaoGeograficaImediataCatalogoResumo(
                "430016", "Alfa", "43", codigo_regiao_intermediaria
            ),
        )


def test_casos_ordenam_e_servico_delega() -> None:
    porta = CatalogoFalso()
    listar_estados = ListarEstadosCatalogoTerritorial(porta)
    listar_municipios = ListarMunicipiosCatalogoTerritorial(porta)
    listar_intermediarias = ListarRegioesIntermediariasCatalogoTerritorial(porta)
    listar_imediatas = ListarRegioesImediatasCatalogoTerritorial(porta)
    aplicacao = AplicacaoCatalogoTerritorial(
        listar_estados,
        listar_municipios,
        listar_intermediarias,
        listar_imediatas,
    )
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


def test_casos_regionais_ordenam_e_preservam_codigos() -> None:
    porta = CatalogoFalso()
    intermediarias = ListarRegioesIntermediariasCatalogoTerritorial(porta)
    imediatas = ListarRegioesImediatasCatalogoTerritorial(porta)
    assert [item.nome for item in intermediarias.executar("43")] == [
        "Alfa", "Zulu"
    ]
    assert [item.nome for item in imediatas.executar("4304")] == [
        "Alfa", "Zulu"
    ]
    assert porta.codigos == ["43", "4304"]


@pytest.mark.parametrize("codigo", ["430", "43045", "ABCD", 4304])
def test_codigo_intermediario_invalido_falha_antes_da_porta(
    codigo: object,
) -> None:
    porta = CatalogoFalso()
    caso = ListarRegioesImediatasCatalogoTerritorial(porta)
    with pytest.raises(
        ValueError,
        match="Código de Região Geográfica Intermediária inválido",
    ):
        caso.executar(codigo)  # type: ignore[arg-type]
    assert porta.codigos == []
