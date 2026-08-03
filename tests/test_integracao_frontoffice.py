import ast
from pathlib import Path


def test_frontoffice_depende_somente_do_caso_de_uso() -> None:
    caminho = (
        Path(__file__).parents[1]
        / "mediad_planner"
        / "presentation"
        / "streamlit_app.py"
    )
    arvore = ast.parse(caminho.read_text(encoding="utf-8"))
    modulos_absolutos = set()
    imports_relativos = []

    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            modulos_absolutos.update(alias.name for alias in no.names)
        elif isinstance(no, ast.ImportFrom):
            if no.level:
                imports_relativos.append(no)
            elif no.module:
                modulos_absolutos.add(no.module)

    caso_de_uso = (
        "mediad_planner.application.use_cases.obter_diagnostico_fundacao"
    )
    prefixos_proibidos = (
        "mediad_planner.domain",
        "mediad_planner.engines",
        "mediad_planner.infrastructure",
    )

    assert caso_de_uso in modulos_absolutos
    chamadas = tuple(
        no
        for no in ast.walk(arvore)
        if isinstance(no, ast.Call)
        and isinstance(no.func, ast.Name)
        and no.func.id == "obter_diagnostico_fundacao"
    )
    assert len(chamadas) == 1
    assert imports_relativos == []
    for modulo in modulos_absolutos:
        assert not modulo.startswith(prefixos_proibidos)
