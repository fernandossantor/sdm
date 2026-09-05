import ast
from pathlib import Path


RAIZ = Path(__file__).parents[1]
ARQUIVO = RAIZ / "mediad_planner/presentation/segmentos.py"


def test_interface_expoe_acoes_e_relacoes_normativas() -> None:
    fonte = ARQUIVO.read_text(encoding="utf-8")
    for texto in (
        "Segmentos e públicos",
        "Universo de origem",
        "Praças do Segmento",
        "Critérios aplicados",
        "Definição do Segmento",
        "Tamanho estimado (opcional)",
        "Criar Segmento",
        "Editar Segmento",
        "Remover Segmento",
        "Segmentos de origem",
        "Praças do Público",
        "Criar Público",
        "Editar Público",
        "Remover Público",
        "múltiplos Públicos",
        "Segmentos podem se sobrepor",
    ):
        assert texto in fonte


def test_interface_depende_somente_da_aplicacao_e_dtos() -> None:
    arvore = ast.parse(ARQUIVO.read_text(encoding="utf-8"))
    importacoes = {
        no.module
        for no in ast.walk(arvore)
        if isinstance(no, ast.ImportFrom) and no.module
    }
    proibidos = (
        "mediad_planner.domain",
        "mediad_planner.infrastructure",
        "mediad_planner.composition",
        "mediad_planner.engines",
    )
    assert not any(item.startswith(proibidos) for item in importacoes)
