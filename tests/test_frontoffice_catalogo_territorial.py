import ast
from pathlib import Path

from mediad_planner.presentation import bibliotecas, praca_universo


def test_apresentacao_respeita_fronteiras() -> None:
    arvore = ast.parse(Path(praca_universo.__file__).read_text(encoding="utf-8"))
    importacoes = {
        no.module
        for no in ast.walk(arvore)
        if isinstance(no, ast.ImportFrom) and no.module
    }
    proibidos = ("urllib", "json", "mediad_planner.infrastructure", "mediad_planner.domain")
    assert not any(nome.startswith(proibidos) for nome in importacoes)


def test_formulario_contem_modos_e_fallback() -> None:
    fonte = Path(praca_universo.__file__).read_text(encoding="utf-8")
    for texto in (
        "Origem dos dados territoriais",
        "Catálogo oficial do IBGE — DTB 2025",
        "Preenchimento manual",
        "Recorte territorial oficial",
        "Unidade da Federação",
        "Município",
        "IBGE — Divisão Territorial Brasileira 2025",
        "O preenchimento manual continua disponível.",
    ):
        assert texto in fonte
    assert ".lower(" not in fonte


def test_bibliotecas_documenta_catalogo_sem_consulta() -> None:
    fonte = Path(bibliotecas.__file__).read_text(encoding="utf-8")
    assert "Catálogo territorial oficial" in fonte
    assert "Unidades da Federação e Municípios" in fonte
    assert "listar_estados" not in fonte
