import pytest

from src.domain.objetivos import Prioridade
from src.engines.traducao_estrategica.matriz_marketing_comunicacao import (
    CandidatoComunicacao,
    ContextoMatriz,
    SituacaoMercadologica,
    avaliar_matriz_marketing_comunicacao,
)


def _candidatos():
    adequacao_comum = {
        "adequacao_publico": 80,
        "adequacao_praca": 80,
        "adequacao_jornada": 80,
        "adequacao_periodo": 80,
        "adequacao_restricoes": 80,
    }
    return (
        CandidatoComunicacao(
            "com_intencao", "Intenção", 80, 100, "PRIORITARIA", **adequacao_comum
        ),
        CandidatoComunicacao(
            "com_reducao_incerteza",
            "Redução de incerteza",
            60,
            79,
            "PRIORITARIA",
            **adequacao_comum,
        ),
        CandidatoComunicacao(
            "com_notoriedade",
            "Notoriedade",
            40,
            59,
            "COMPLEMENTAR",
            **adequacao_comum,
        ),
    )


def _contexto(**alteracoes):
    dados = {
        "objetivo_marketing": "mkt_aumento_vendas",
        "prioridade_declarada": Prioridade.MUITO_ALTA,
        "candidatos": _candidatos(),
        "situacao_mercadologica": SituacaoMercadologica(78, 1.1),
        "pressao_competitiva": 35,
        "publico": "Responsáveis pela decisão de energia residencial",
        "praca": "Campinas (SP)",
        "jornada": "consideração para intenção",
        "periodo": "2026-09-01/2026-10-31",
        "verba_disponivel_percentual_do_necessario": 60,
        "restricoes": ("teto orçamentário rígido",),
        "confianca": 80,
    }
    dados.update(alteracoes)
    return ContextoMatriz(**dados)


def _ordem(resultado):
    return tuple(item.candidato for item in resultado)


def test_caso_canonico_prioriza_intencao_e_preserva_componentes():
    resultado = avaliar_matriz_marketing_comunicacao(_contexto())

    assert _ordem(resultado) == (
        "com_intencao",
        "com_reducao_incerteza",
        "com_notoriedade",
    )
    assert tuple(item.ordem for item in resultado) == (1, 2, 3)
    assert all(item.versao_configuracao == "1.0" for item in resultado)
    assert len(resultado[0].contribuicoes_por_dimensao) == 11
    assert {item.dimensao for item in resultado[0].contribuicoes_por_dimensao} == {
        "forca_padrao",
        "prioridade",
        "situacao_mercadologica",
        "situacao_competitiva",
        "publico",
        "praca",
        "jornada",
        "periodo",
        "verba",
        "restricoes",
        "confianca",
    }


def test_baixa_notoriedade_muda_ordem_e_prioriza_notoriedade():
    resultado = avaliar_matriz_marketing_comunicacao(
        _contexto(situacao_mercadologica=SituacaoMercadologica(30, 10))
    )

    assert resultado[0].candidato == "com_notoriedade"
    assert "notoriedade_baixa" in resultado[0].justificativa_estruturada


def test_alta_notoriedade_e_baixa_conversao_mantem_intencao_primeira():
    resultado = avaliar_matriz_marketing_comunicacao(
        _contexto(situacao_mercadologica=SituacaoMercadologica(85, 0.8))
    )

    assert resultado[0].candidato == "com_intencao"
    assert resultado[-1].candidato == "com_notoriedade"
    assert "conversao_baixa" in resultado[0].justificativa_estruturada


def test_verba_muito_restrita_muda_ordem_e_expoe_penalizacao():
    resultado = avaliar_matriz_marketing_comunicacao(
        _contexto(verba_disponivel_percentual_do_necessario=15)
    )

    assert resultado[0].candidato == "com_reducao_incerteza"
    intencao = next(item for item in resultado if item.candidato == "com_intencao")
    assert intencao.penalizacoes[0].codigo == "verba_muito_restrita"
    assert intencao.penalizacoes[0].valor == 15


def test_forca_contextual_e_reconstituivel_pelos_componentes():
    item = avaliar_matriz_marketing_comunicacao(_contexto())[0]
    valor_reconstituido = sum(
        contribuicao.contribuicao
        for contribuicao in item.contribuicoes_por_dimensao
    ) - sum(penalizacao.valor for penalizacao in item.penalizacoes)

    assert item.forca_contextual == round(valor_reconstituido, 2)


def test_rejeita_faixa_de_forca_padrao_invalida():
    candidato = CandidatoComunicacao(
        "com_intencao", "Intenção", 90, 80, "PRIORITARIA", 80, 80, 80, 80, 80
    )

    with pytest.raises(ValueError, match="faixa de força padrão inválida"):
        avaliar_matriz_marketing_comunicacao(_contexto(candidatos=(candidato,)))
