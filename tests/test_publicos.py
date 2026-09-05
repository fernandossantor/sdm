from uuid import UUID

import pytest

from mediad_planner.application.dto.campanha import CriarCampanhaEntrada
from mediad_planner.application.dto.criterios_segmentacao import DefinirCriteriosSegmentacaoEntrada
from mediad_planner.application.dto.praca_universo import AdicionarPracaEntrada, AdicionarUniversoEntrada
from mediad_planner.application.dto.publicos import SalvarPublicoEntrada
from mediad_planner.application.dto.segmentos import SalvarSegmentoEntrada
from mediad_planner.composition.ambiente import construir_ambiente_aplicacao_em_memoria


def _preparar():
    ambiente = construir_ambiente_aplicacao_em_memoria()
    campanha = ambiente.campanhas.criar_campanha(CriarCampanhaEntrada(
        nome="Campanha", nome_anunciante="Anunciante", nome_marca=None,
        nome_produto_servico=None, nome_planejador_responsavel="Planejadora",
        nomes_equipe=(), observacao_inicial=None, iniciar_briefing=True,
    ))
    id_campanha = campanha.id_campanha
    ambiente.espaco_trabalho.preparar_briefing(id_campanha)
    ids_pracas = []
    for nome in ("Praça A", "Praça B"):
        resumo = ambiente.briefings.adicionar_praca(id_campanha, AdicionarPracaEntrada(
            tipo="MUNICIPIO", nome=nome, codigo_oficial=None, abrangencia=None,
            valor_populacao_referencia=None, codigo_unidade_populacional=None,
            unidade_populacional=None, fonte=None, data_referencia=None,
            observacao=None,
        ))
        ids_pracas.append(resumo.pracas[-1].id_praca)
    resumo = ambiente.briefings.adicionar_universo(id_campanha, AdicionarUniversoEntrada(
        nome="Universo", definicao="Pessoas", ids_pracas=tuple(ids_pracas),
        valor_populacional="100", codigo_unidade="pessoas", unidade="Pessoas",
        fonte="Fonte", data_referencia="2026", criterios_inclusao=None,
        criterios_exclusao=None, observacao=None,
    ))
    id_universo = resumo.universos[0].id_universo
    ambiente.briefings.definir_criterios_segmentacao(
        id_campanha, DefinirCriteriosSegmentacaoEntrada(("DEMOGRAFICA",))
    )
    ids_segmentos = []
    for indice, id_praca in enumerate(ids_pracas, 1):
        resumo = ambiente.briefings.adicionar_segmento(id_campanha, SalvarSegmentoEntrada(
            id_universo_origem=id_universo, ids_pracas=(id_praca,),
            criterios_aplicados=("DEMOGRAFICA",), definicao=f"Segmento {indice}",
            tamanho_estimado="40", fonte="Fonte", data_referencia="2026",
        ))
        ids_segmentos.append(resumo.segmentos[-1].id_segmento)
    return ambiente, id_campanha, tuple(ids_segmentos), tuple(ids_pracas)


def _entrada(segmentos: tuple[UUID, ...], pracas: tuple[UUID, ...], **mudancas):
    dados = dict(
        nome="Público principal", ids_segmentos_origem=segmentos,
        ids_pracas=pracas, prioridade=5, intensidade_importancia=4,
        tamanho_estimado="70", papel_declarado="Principal",
        justificativa="Declarado pelo anunciante",
    )
    dados.update(mudancas)
    return SalvarPublicoEntrada(**dados)


def test_cria_edita_e_remove_publico_com_multiplos_segmentos() -> None:
    ambiente, campanha, segmentos, pracas = _preparar()
    resumo = ambiente.briefings.adicionar_publico(
        campanha, _entrada(segmentos, pracas)
    )
    publico = resumo.publicos[0]
    assert publico.definicoes_segmentos_origem == ("Segmento 1", "Segmento 2")
    assert publico.rotulos_pracas == ("[Município] Praça A", "[Município] Praça B")
    resumo = ambiente.briefings.editar_publico(
        campanha, publico.id_publico,
        _entrada((segmentos[0],), (pracas[0],), nome="Público editado", prioridade=None),
    )
    assert resumo.publicos[0].nome == "Público editado"
    assert resumo.publicos[0].prioridade is None
    assert ambiente.briefings.remover_publico(
        campanha, publico.id_publico
    ).publicos == ()


@pytest.mark.parametrize(
    ("mudancas", "mensagem"),
    (
        ({"ids_segmentos_origem": ()}, "ao menos um Segmento"),
        ({"ids_pracas": ()}, "ao menos uma Praça"),
        ({"prioridade": 6}, "entre 1 e 5"),
        ({"intensidade_importancia": 0}, "entre 1 e 5"),
    ),
)
def test_rejeita_publico_incompleto_ou_escala_invalida(mudancas, mensagem) -> None:
    ambiente, campanha, segmentos, pracas = _preparar()
    with pytest.raises(ValueError, match=mensagem):
        ambiente.briefings.adicionar_publico(
            campanha, _entrada(segmentos, pracas, **mudancas)
        )


def test_rejeita_praca_incompativel_duplicidade_e_protege_segmento() -> None:
    ambiente, campanha, segmentos, pracas = _preparar()
    with pytest.raises(ValueError, match="incompatível"):
        ambiente.briefings.adicionar_publico(
            campanha, _entrada((segmentos[0],), (pracas[1],))
        )
    ambiente.briefings.adicionar_publico(campanha, _entrada(segmentos, pracas))
    with pytest.raises(ValueError, match="duplicado"):
        ambiente.briefings.adicionar_publico(
            campanha, _entrada(segmentos[::-1], pracas[::-1], nome="Outro nome")
        )
    with pytest.raises(ValueError, match="vinculado a Público"):
        ambiente.briefings.remover_segmento(campanha, segmentos[0])
