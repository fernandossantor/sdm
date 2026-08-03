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
    assert "Regiões Geográficas " in fonte
    assert "Intermediárias, Regiões Geográficas Imediatas e Municípios" in fonte
    assert "listar_estados" not in fonte


def test_frontoffice_oferece_regioes_sem_acessar_infraestrutura() -> None:
    fonte = Path(praca_universo.__file__).read_text(encoding="utf-8")
    for texto in (
        "Região Geográfica Intermediária",
        "Região Geográfica Imediata",
        "REGIAO_GEOGRAFICA_INTERMEDIARIA",
        "REGIAO_GEOGRAFICA_IMEDIATA",
        "listar_regioes_intermediarias",
        "listar_regioes_imediatas",
        "Nenhuma Região Geográfica Intermediária foi encontrada",
        "Nenhuma Região Geográfica Imediata foi encontrada",
    ):
        assert texto in fonte
    assert "mediad_planner.infrastructure" not in fonte
    assert "4318002" not in fonte
