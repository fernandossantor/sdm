import ast
from pathlib import Path


ARQUIVO = Path(__file__).parents[1] / "mediad_planner/presentation/periodo_verba.py"


def test_interface_expoe_campos_acoes_e_limites_normativos() -> None:
    fonte = ARQUIVO.read_text(encoding="utf-8")
    for texto in (
        "Período pretendido e Verba", "Data inicial pretendida",
        "Data final pretendida", "Duração declarada", "Datas críticas",
        "Sazonalidades", "Eventos condicionantes", "Períodos obrigatórios",
        "Períodos vedados", "Valor total disponível", "Moeda",
        "Natureza do limite", "Margem de flexibilidade", "Valor mínimo",
        "Valor máximo", "Parcela já comprometida", "Criar Período e Verba",
        "Editar Período e Verba", "Flight, distribuição e otimização",
    ):
        assert texto in fonte


def test_interface_respeita_fronteiras() -> None:
    arvore = ast.parse(ARQUIVO.read_text(encoding="utf-8"))
    importacoes = {
        no.module for no in ast.walk(arvore)
        if isinstance(no, ast.ImportFrom) and no.module
    }
    proibidos = ("mediad_planner.domain", "mediad_planner.infrastructure",
                 "mediad_planner.composition", "mediad_planner.engines")
    assert not any(item.startswith(proibidos) for item in importacoes)
