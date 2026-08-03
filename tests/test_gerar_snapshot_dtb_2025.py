import io
import json
from pathlib import Path
import zipfile

import pytest

from scripts.gerar_snapshot_dtb_2025 import (
    ARQUIVO_ODS,
    SIGLAS_UF_POR_CODIGO,
    _interpretar,
    _linhas_logicas,
    _validar_mapeamento,
)


CABECALHO = (
    "UF",
    "Nome_UF",
    "Região Geográfica Intermediária",
    "Nome Região Geográfica Intermediária",
    "Região Geográfica Imediata",
    "Nome Região Geográfica Imediata",
    "Código Município Completo",
    "Nome_Município",
)


def _xml(linhas: list[tuple[str, ...]], extra: str = "") -> bytes:
    linhas_xml = []
    for linha in linhas:
        celulas = "".join(
            f"<table:table-cell><text:p>{valor}</text:p></table:table-cell>"
            for valor in linha
        )
        linhas_xml.append(f"<table:table-row>{celulas}</table:table-row>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<office:document-content '
        'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
        'xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" '
        'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">'
        f"<office:body><office:spreadsheet><table:table>{extra}"
        + "".join(linhas_xml)
        + "</table:table></office:spreadsheet></office:body>"
        "</office:document-content>"
    ).encode()


def _linhas_todas_ufs() -> list[tuple[str, ...]]:
    linhas = [CABECALHO]
    for indice, codigo in enumerate(SIGLAS_UF_POR_CODIGO):
        nome_uf = "Rio Grande do Sul" if codigo == "43" else f"Estado {codigo}"
        codigo_municipio = "4318002" if codigo == "43" else f"{codigo}{indice:05d}"
        nome = "São Borja" if codigo == "43" else f"Município {codigo}"
        linhas.append((
            codigo, nome_uf, "4304", "Intermediária",
            "430017", "Imediata", codigo_municipio, nome,
        ))
    return linhas


def test_mapeamento_canonico_e_resultados_autorizados() -> None:
    _validar_mapeamento()
    assert len(SIGLAS_UF_POR_CODIGO) == 27
    assert len(set(SIGLAS_UF_POR_CODIGO.values())) == 27
    assert SIGLAS_UF_POR_CODIGO["43"] == "RS"
    assert SIGLAS_UF_POR_CODIGO["35"] == "SP"
    assert SIGLAS_UF_POR_CODIGO["53"] == "DF"


def test_interpretacao_preserva_nome_codigos_e_regioes() -> None:
    estados, municipios = _interpretar(_xml(_linhas_todas_ufs()))
    rs = next(item for item in estados if item["codigo"] == "43")
    sao_borja = next(item for item in municipios if item["codigo"] == "4318002")
    assert rs == {
        "codigo": "43",
        "sigla": "RS",
        "nome": "Rio Grande do Sul",
        "codigo_regiao": None,
        "sigla_regiao": None,
        "nome_regiao": None,
    }
    assert sao_borja["codigo_estado"] == "43"
    assert sao_borja["codigo_regiao_intermediaria"] == "4304"
    assert sao_borja["codigo_regiao_imediata"] == "430017"


def test_codigo_desconhecido_e_cabecalho_incompleto_falham() -> None:
    linhas = _linhas_todas_ufs()
    linhas[1] = ("99",) + linhas[1][1:]
    with pytest.raises(ValueError, match="não possui sigla canônica"):
        _interpretar(_xml(linhas))
    with pytest.raises(ValueError, match="Estrutura de colunas"):
        _interpretar(_xml([("UF", "Nome_UF")]))


def test_parser_expande_repeticoes_paragrafos_e_ignora_vazio() -> None:
    extra = (
        '<table:table-row table:number-rows-repeated="2">'
        '<table:table-cell table:number-columns-repeated="2">'
        '<text:p>um</text:p><text:p>dois</text:p>'
        "</table:table-cell></table:table-row>"
        '<table:table-row><table:table-cell><text:p/></table:table-cell>'
        "</table:table-row>"
    )
    assert _linhas_logicas(_xml([], extra)) == (
        ("um dois", "um dois"),
        ("um dois", "um dois"),
    )


def test_zip_sintetico_contem_ods_e_bytes_sao_deterministicos(tmp_path: Path) -> None:
    ods = io.BytesIO()
    with zipfile.ZipFile(ods, "w") as arquivo:
        arquivo.writestr("content.xml", _xml(_linhas_todas_ufs()))
    pacote = tmp_path / "dtb.zip"
    with zipfile.ZipFile(pacote, "w") as arquivo:
        arquivo.writestr(ARQUIVO_ODS, ods.getvalue())
    with zipfile.ZipFile(pacote) as arquivo:
        assert arquivo.read(ARQUIVO_ODS) == ods.getvalue()
    assert json.dumps({"conteudo": ods.getvalue().hex()}) == json.dumps(
        {"conteudo": ods.getvalue().hex()}
    )
