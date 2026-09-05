from uuid import UUID

import pytest

from mediad_planner.application.dto.campanha import CriarCampanhaEntrada
from mediad_planner.application.dto.criterios_segmentacao import (
    DefinirCriteriosSegmentacaoEntrada,
)
from mediad_planner.application.dto.praca_universo import (
    AdicionarPracaEntrada,
    AdicionarUniversoEntrada,
)
from mediad_planner.application.dto.segmentos import SalvarSegmentoEntrada
from mediad_planner.composition.ambiente import construir_ambiente_aplicacao_em_memoria


def _preparar():
    ambiente = construir_ambiente_aplicacao_em_memoria()
    campanha = ambiente.campanhas.criar_campanha(
        CriarCampanhaEntrada(
            nome="Campanha", nome_anunciante="Anunciante", nome_marca=None,
            nome_produto_servico=None,
            nome_planejador_responsavel="Planejadora", nomes_equipe=(),
            observacao_inicial=None, iniciar_briefing=True,
        )
    )
    id_campanha = campanha.id_campanha
    ambiente.espaco_trabalho.preparar_briefing(id_campanha)
    for nome in ("Praça A", "Praça B"):
        resumo = ambiente.briefings.adicionar_praca(
            id_campanha,
            AdicionarPracaEntrada(
                tipo="MUNICIPIO", nome=nome, codigo_oficial=None,
                abrangencia=None, valor_populacao_referencia=None,
                codigo_unidade_populacional=None, unidade_populacional=None,
                fonte=None, data_referencia=None, observacao=None,
            ),
        )
    id_praca_a, id_praca_b = (item.id_praca for item in resumo.pracas)
    resumo = ambiente.briefings.adicionar_universo(
        id_campanha,
        AdicionarUniversoEntrada(
            nome="Adultos", definicao="Pessoas adultas",
            ids_pracas=(id_praca_a,), valor_populacional="100",
            codigo_unidade="pessoas", unidade="Pessoas", fonte="Fonte",
            data_referencia="2026", criterios_inclusao=None,
            criterios_exclusao=None, observacao=None,
        ),
    )
    ambiente.briefings.definir_criterios_segmentacao(
        id_campanha,
        DefinirCriteriosSegmentacaoEntrada(("DEMOGRAFICA", "CONSUMO")),
    )
    return ambiente, id_campanha, resumo.universos[0].id_universo, id_praca_a, id_praca_b


def _entrada(id_universo: UUID, id_praca: UUID, **mudancas):
    dados = dict(
        id_universo_origem=id_universo,
        ids_pracas=(id_praca,),
        criterios_aplicados=("DEMOGRAFICA",),
        definicao="Adultos de 25 a 44 anos",
        tamanho_estimado="40",
        fonte="Pesquisa",
        data_referencia="2026",
    )
    dados.update(mudancas)
    return SalvarSegmentoEntrada(**dados)


def test_cria_edita_e_remove_segmento_preservando_relacoes() -> None:
    ambiente, campanha, universo, praca, _ = _preparar()
    resumo = ambiente.briefings.adicionar_segmento(
        campanha, _entrada(universo, praca)
    )
    segmento = resumo.segmentos[0]
    assert segmento.nome_universo_origem == "Adultos"
    assert segmento.rotulos_criterios == ("Demográfica",)
    assert segmento.unidade == "Pessoas"
    resumo = ambiente.briefings.editar_segmento(
        campanha,
        segmento.id_segmento,
        _entrada(
            universo, praca, definicao="Consumidores adultos",
            criterios_aplicados=("CONSUMO",), tamanho_estimado="30",
        ),
    )
    assert resumo.segmentos[0].definicao == "Consumidores adultos"
    assert resumo.segmentos[0].tamanho_estimado == "30"
    assert ambiente.briefings.remover_segmento(
        campanha, segmento.id_segmento
    ).segmentos == ()


@pytest.mark.parametrize(
    ("mudancas", "mensagem"),
    (
        ({"criterios_aplicados": ()}, "ao menos um critério"),
        ({"criterios_aplicados": ("INTENCAO",)}, "não foi selecionado"),
        ({"tamanho_estimado": "101"}, "não pode superar"),
    ),
)
def test_rejeita_segmento_incoerente(mudancas, mensagem) -> None:
    ambiente, campanha, universo, praca, _ = _preparar()
    with pytest.raises(ValueError, match=mensagem):
        ambiente.briefings.adicionar_segmento(
            campanha, _entrada(universo, praca, **mudancas)
        )


def test_rejeita_praca_incompativel_e_protege_dependencias() -> None:
    ambiente, campanha, universo, praca, praca_incompativel = _preparar()
    with pytest.raises(ValueError, match="incompatível"):
        ambiente.briefings.adicionar_segmento(
            campanha, _entrada(universo, praca_incompativel)
        )
    resumo = ambiente.briefings.adicionar_segmento(
        campanha, _entrada(universo, praca)
    )
    with pytest.raises(ValueError, match="vinculado a Segmento"):
        ambiente.briefings.remover_universo(campanha, universo)
    with pytest.raises(ValueError, match="não foi selecionado"):
        ambiente.briefings.definir_criterios_segmentacao(
            campanha, DefinirCriteriosSegmentacaoEntrada(("CONSUMO",))
        )
    assert len(resumo.segmentos) == 1
