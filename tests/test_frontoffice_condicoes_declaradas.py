import ast
from pathlib import Path


ARQUIVO = Path(__file__).parents[1] / "mediad_planner/presentation/condicoes_declaradas.py"


def test_interface_expoe_crud_campos_e_alertas() -> None:
    fonte = ARQUIVO.read_text(encoding="utf-8")
    for texto in (
        "Prioridades, Restrições e Pretensões", "Entidade priorizada",
        "Criar Prioridade", "Editar Prioridade", "Remover Prioridade",
        "Categoria da Restrição", "Entidade afetada", "Intensidade da Restrição",
        "Criar Restrição", "Editar Restrição", "Remover Restrição",
        "Categoria da Pretensão", "Público associado", "Praça associada",
        "Etapa da Jornada associada", "Flexibilidade declarada",
        "Criar Pretensão", "Editar Pretensão", "Remover Pretensão",
        "Todos os itens estão marcados com a mesma prioridade",
        "múltiplas prioridades máximas sem justificativa",
        "classificação técnica e as decisões de mídia pertencem às etapas posteriores",
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
