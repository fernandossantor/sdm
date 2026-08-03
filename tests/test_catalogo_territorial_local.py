import json
from pathlib import Path

import pytest

from mediad_planner.application.ports.catalogo_territorial import (
    CatalogoTerritorialIndisponivel,
)
from mediad_planner.infrastructure.ibge.catalogo_territorial_local import (
    CatalogoTerritorialLocal,
)


def _dados() -> dict[str, object]:
    return {
        "metadados": {"quantidade_estados": 1, "quantidade_municipios": 1},
        "estados": [{
            "codigo": "43", "sigla": "RS", "nome": "Rio Grande do Sul",
            "codigo_regiao": None, "sigla_regiao": None, "nome_regiao": None,
        }],
        "municipios": [{
            "codigo": "4318002", "nome": "São Borja", "codigo_estado": "43",
        }],
    }


def _gravar(caminho: Path, dados: object) -> None:
    caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")


def test_carregamento_preguicoso_converte_agrupa_e_reutiliza(tmp_path: Path) -> None:
    caminho = tmp_path / "snapshot.json"
    catalogo = CatalogoTerritorialLocal(caminho)
    _gravar(caminho, _dados())
    estados = catalogo.listar_estados()
    caminho.unlink()
    assert catalogo.listar_estados() is estados
    assert catalogo.listar_municipios("43")[0].codigo == "4318002"
    assert catalogo.listar_municipios("99") == ()


@pytest.mark.parametrize(
    "mutacao",
    [
        lambda dados: [],
        lambda dados: {**dados, "metadados": []},
        lambda dados: {**dados, "estados": {}},
        lambda dados: {**dados, "municipios": {}},
        lambda dados: {
            **dados,
            "metadados": {"quantidade_estados": 2, "quantidade_municipios": 1},
        },
        lambda dados: {**dados, "municipios": []},
        lambda dados: {
            **dados,
            "municipios": [{
                "codigo": "4318002", "nome": "São Borja", "codigo_estado": "42",
            }],
        },
        lambda dados: {
            **dados,
            "municipios": [{
                "codigo": "4300000", "nome": "Outro", "codigo_estado": "43",
            }],
        },
    ],
)
def test_estrutura_invalida_produz_erro_publico(tmp_path: Path, mutacao) -> None:
    caminho = tmp_path / "snapshot.json"
    _gravar(caminho, mutacao(_dados()))
    with pytest.raises(CatalogoTerritorialIndisponivel) as capturado:
        CatalogoTerritorialLocal(caminho).listar_estados()
    assert capturado.value.__cause__ is not None


def test_arquivo_ausente_json_e_utf8_invalidos(tmp_path: Path) -> None:
    caminhos = (tmp_path / "ausente", tmp_path / "json", tmp_path / "utf8")
    caminhos[1].write_text("{", encoding="utf-8")
    caminhos[2].write_bytes(b"\xff")
    for caminho in caminhos:
        with pytest.raises(CatalogoTerritorialIndisponivel):
            CatalogoTerritorialLocal(caminho).listar_estados()
