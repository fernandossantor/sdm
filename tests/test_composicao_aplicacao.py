from dataclasses import FrozenInstanceError

import pytest

from mediad_planner.application.dto.campanha import CriarCampanhaEntrada
from mediad_planner.composition.ambiente import (
    construir_ambiente_aplicacao_em_memoria,
)


def entrada_campanha() -> CriarCampanhaEntrada:
    return CriarCampanhaEntrada(
        nome="Campanha Compartilhada",
        nome_anunciante="Anunciante",
        nome_marca="Marca",
        nome_produto_servico="Produto",
        nome_planejador_responsavel="Planejadora",
        nomes_equipe=("Analista",),
        observacao_inicial=None,
        iniciar_briefing=True,
    )


def test_ambiente_compartilha_campanhas_com_briefings() -> None:
    ambiente = construir_ambiente_aplicacao_em_memoria()

    campanha = ambiente.campanhas.criar_campanha(entrada_campanha())
    briefing = ambiente.briefings.abrir_briefing(campanha.id_campanha)

    assert briefing.id_campanha == campanha.id_campanha
    assert briefing.codigo_campanha == campanha.codigo
    assert briefing.nome_campanha == campanha.nome
    assert briefing.anunciante == campanha.anunciante
    assert briefing.marca == campanha.marca
    assert briefing.produto_servico == campanha.produto_servico


def test_ambientes_sao_isolados_e_objeto_e_congelado() -> None:
    primeiro = construir_ambiente_aplicacao_em_memoria()
    segundo = construir_ambiente_aplicacao_em_memoria()
    campanha = primeiro.campanhas.criar_campanha(entrada_campanha())

    with pytest.raises(LookupError):
        segundo.briefings.abrir_briefing(campanha.id_campanha)
    with pytest.raises(FrozenInstanceError):
        primeiro.campanhas = segundo.campanhas
