from pathlib import Path

from mediad_planner.application.dto.campanha import CriarCampanhaEntrada
from mediad_planner.composition.ambiente import construir_ambiente_aplicacao_em_memoria


def test_mapper_publico_preserva_resumo_e_substitui_mapper_privado() -> None:
    ambiente = construir_ambiente_aplicacao_em_memoria()
    resumo = ambiente.campanhas.criar_campanha(
        CriarCampanhaEntrada(
            nome="Campanha Mapper",
            nome_anunciante="Anunciante",
            nome_marca="Marca",
            nome_produto_servico="Produto",
            nome_planejador_responsavel="Planejadora",
            nomes_equipe=("Pessoa",),
            observacao_inicial="Observação",
            iniciar_briefing=False,
        )
    )
    assert resumo.situacao == "RASCUNHO"
    assert resumo.etapa_atual == "ABERTURA"
    assert resumo.equipe == ("Pessoa",)
    assert resumo.identificacao_completa.endswith("— Marca")

    fonte = Path(
        "mediad_planner/application/use_cases/campanhas.py"
    ).read_text(encoding="utf-8")
    assert "resumir_campanha" in fonte
    assert "def _resumir" not in fonte
