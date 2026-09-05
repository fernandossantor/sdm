from dataclasses import FrozenInstanceError

import pytest

from mediad_planner.application.dto.campanha import CriarCampanhaEntrada
from mediad_planner.application.dto.criterios_segmentacao import (
    DefinirCriteriosSegmentacaoEntrada,
)
from mediad_planner.composition.ambiente import construir_ambiente_aplicacao_em_memoria
from mediad_planner.domain.briefing.praca_universo import (
    CriterioSegmentacao,
    EstruturaTerritorialPopulacional,
    listar_criterios_segmentacao,
)


def _ambiente_preparado():
    ambiente = construir_ambiente_aplicacao_em_memoria()
    campanha = ambiente.campanhas.criar_campanha(
        CriarCampanhaEntrada(
            nome="Campanha",
            nome_anunciante="Anunciante",
            nome_marca=None,
            nome_produto_servico=None,
            nome_planejador_responsavel="Planejadora",
            nomes_equipe=(),
            observacao_inicial=None,
            iniciar_briefing=True,
        )
    )
    ambiente.espaco_trabalho.preparar_briefing(campanha.id_campanha)
    return ambiente, campanha.id_campanha


def test_catalogo_canonico_tem_as_onze_categorias_na_ordem_normativa() -> None:
    assert tuple(item.codigo.value for item in listar_criterios_segmentacao()) == (
        "GEOGRAFICA", "DEMOGRAFICA", "SOCIOECONOMICA", "PSICOGRAFICA",
        "COMPORTAMENTAL", "CONSUMO", "RELACIONAMENTO_CATEGORIA",
        "RELACIONAMENTO_MARCA", "JORNADA", "INTENCAO", "CONTEXTO",
    )


def test_estrutura_rejeita_duplicatas_e_e_imutavel() -> None:
    with pytest.raises(ValueError, match="duplicados"):
        EstruturaTerritorialPopulacional(
            (), (), (CriterioSegmentacao.CONSUMO, CriterioSegmentacao.CONSUMO)
        )
    estrutura = EstruturaTerritorialPopulacional((), ())
    with pytest.raises(FrozenInstanceError):
        estrutura.criterios_segmentacao = (CriterioSegmentacao.CONSUMO,)


def test_cria_e_edita_selecao_preservando_estado_e_rastreabilidade() -> None:
    ambiente, id_campanha = _ambiente_preparado()
    resumo = ambiente.briefings.definir_criterios_segmentacao(
        id_campanha,
        DefinirCriteriosSegmentacaoEntrada(("GEOGRAFICA", "DEMOGRAFICA")),
    )
    assert resumo.estado == "EM_PREENCHIMENTO"
    assert resumo.criterios_segmentacao == ("GEOGRAFICA", "DEMOGRAFICA")
    atualizado = ambiente.briefings.definir_criterios_segmentacao(
        id_campanha,
        DefinirCriteriosSegmentacaoEntrada(("CONSUMO", "INTENCAO")),
    )
    assert atualizado.criterios_segmentacao == ("CONSUMO", "INTENCAO")
    assert atualizado.numero_versao == resumo.numero_versao
    with pytest.raises(ValueError, match="inválido"):
        ambiente.briefings.definir_criterios_segmentacao(
            id_campanha,
            DefinirCriteriosSegmentacaoEntrada(("INVENTADO",)),
        )
