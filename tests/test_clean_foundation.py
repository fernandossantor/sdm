from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]


def test_fonte_normativa_e_ativos_foram_preservados():
    assert (
        RAIZ
        / "docs"
        / "new_app"
        / "30_AUDITORIA_FINAL_DE_CONSISTENCIA_DOCUMENTAL.md"
    ).is_file()
    assert (RAIZ / "assets" / "Marca_nova.png").is_file()
    assert (RAIZ / "assets" / "favicon2.png").is_file()


def test_entrada_aponta_somente_para_o_novo_pacote():
    entrada = (RAIZ / "app.py").read_text(encoding="utf-8")
    assert "mediad_planner.presentation.streamlit_app" in entrada
    assert "from application" not in entrada
    assert "from domain" not in entrada
    assert "from engines" not in entrada
    assert "from presentation" not in entrada


def test_diretorios_operacionais_legados_nao_estao_na_raiz():
    for nome in (
        "application",
        "components",
        "domain",
        "engine",
        "engines",
        "infrastructure",
        "pages",
        "presentation",
        "scripts",
        "database",
        "data",
        "src",
        "supabase",
    ):
        assert not (RAIZ / nome).exists(), nome


def test_fundacao_nova_existe():
    for caminho in (
        "mediad_planner/application",
        "mediad_planner/domain",
        "mediad_planner/engines",
        "mediad_planner/infrastructure",
        "mediad_planner/knowledge",
        "mediad_planner/presentation",
    ):
        assert (RAIZ / caminho).exists(), caminho
