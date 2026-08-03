import json
import urllib.error

import pytest

from mediad_planner.application.ports.catalogo_territorial import (
    CatalogoTerritorialIndisponivel,
)
from mediad_planner.infrastructure.ibge.catalogo_territorial_ibge import (
    CatalogoTerritorialIBGE,
)


ESTADOS = [{
    "id": 43,
    "sigla": "RS",
    "nome": "Rio Grande do Sul",
    "regiao": {"id": 4, "sigla": "S", "nome": "Sul"},
    "extra": True,
}]
MUNICIPIOS = [{"id": 4318002, "nome": "São Borja", "extra": True}]


class Leitor:
    def __init__(self) -> None:
        self.chamadas: list[tuple[str, float]] = []

    def __call__(self, url: str, timeout: float) -> object:
        self.chamadas.append((url, timeout))
        return MUNICIPIOS if "/municipios?" in url else ESTADOS


def test_urls_parsing_e_codigos_preservados() -> None:
    leitor = Leitor()
    catalogo = CatalogoTerritorialIBGE(leitor_json=leitor)
    estado = catalogo.listar_estados()[0]
    municipio = catalogo.listar_municipios("43")[0]
    assert (estado.codigo, estado.codigo_regiao) == ("43", "4")
    assert (municipio.codigo, municipio.codigo_estado) == ("4318002", "43")
    assert leitor.chamadas[0][0].endswith("/estados?orderBy=nome")
    assert leitor.chamadas[1][0].endswith("/estados/43/municipios?orderBy=nome")


def test_cache_por_recurso_e_expiracao() -> None:
    leitor = Leitor()
    instante = [10.0]
    catalogo = CatalogoTerritorialIBGE(
        leitor_json=leitor,
        relogio_monotonico=lambda: instante[0],
        duracao_cache_segundos=5,
    )
    assert catalogo.listar_estados() is catalogo.listar_estados()
    assert catalogo.listar_municipios("43") is catalogo.listar_municipios("43")
    catalogo.listar_municipios("42")
    assert len(leitor.chamadas) == 3
    instante[0] = 16
    catalogo.listar_estados()
    assert len(leitor.chamadas) == 4


@pytest.mark.parametrize("payload", [{}, ["inválido"], [{}]])
def test_resposta_de_estados_malformada_e_controlada(payload: object) -> None:
    catalogo = CatalogoTerritorialIBGE(leitor_json=lambda _url, _timeout: payload)
    with pytest.raises(CatalogoTerritorialIndisponivel) as capturado:
        catalogo.listar_estados()
    assert capturado.value.__cause__ is not None


@pytest.mark.parametrize(
    "erro",
    [
        urllib.error.URLError("rede"),
        TimeoutError("tempo"),
        OSError("transporte"),
        json.JSONDecodeError("json", "x", 0),
        UnicodeError("utf-8"),
    ],
)
def test_falhas_de_transporte_sao_controladas(erro: BaseException) -> None:
    def falhar(_url: str, _timeout: float) -> object:
        raise erro

    catalogo = CatalogoTerritorialIBGE(leitor_json=falhar)
    with pytest.raises(
        CatalogoTerritorialIndisponivel,
        match="Catálogo territorial do IBGE indisponível no momento",
    ):
        catalogo.listar_estados()


def test_construcao_nao_consulta_e_validacoes_do_construtor() -> None:
    leitor = Leitor()
    CatalogoTerritorialIBGE(leitor_json=leitor)
    assert leitor.chamadas == []
    for argumentos in (
        {"url_base": " "},
        {"timeout_segundos": 0},
        {"duracao_cache_segundos": 0},
    ):
        with pytest.raises(ValueError):
            CatalogoTerritorialIBGE(**argumentos)
