import ast
from pathlib import Path


ARQUIVO = Path(__file__).parents[1] / "mediad_planner/presentation/jornada.py"


def test_interface_expoe_campos_acoes_e_alertas_normativos() -> None:
    fonte = ARQUIVO.read_text(encoding="utf-8")
    for texto in (
        "Criar Jornada", "Editar Jornada", "Remover Jornada",
        "Criar Etapa", "Editar Etapa", "Remover Etapa",
        "Públicos associados à Jornada", "Categoria da Etapa", "Ordem",
        "Relevância da Etapa", "Intensidade da Etapa", "Prioridade da Etapa",
        "Situação atual", "Situação pretendida", "Objetivos de Comunicação",
        "Pontos de contato não pertencem ao Briefing",
    ):
        assert texto in fonte


def test_interface_nao_acessa_dominio_ou_infraestrutura() -> None:
    arvore = ast.parse(ARQUIVO.read_text(encoding="utf-8"))
    importacoes = {
        no.module for no in ast.walk(arvore)
        if isinstance(no, ast.ImportFrom) and no.module
    }
    proibidos = ("mediad_planner.domain", "mediad_planner.infrastructure",
                 "mediad_planner.composition", "mediad_planner.engines")
    assert not any(item.startswith(proibidos) for item in importacoes)
