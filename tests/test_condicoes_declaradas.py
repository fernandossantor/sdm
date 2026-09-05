from uuid import uuid4

import pytest

from mediad_planner.application.dto.condicoes_declaradas import (
    SalvarPretensaoEntrada,
    SalvarPrioridadeEntrada,
    SalvarRestricaoEntrada,
)
from test_publicos import _entrada, _preparar


def test_catalogos_normativos_estao_completos() -> None:
    ambiente, _, _, _ = _preparar()
    assert len(ambiente.briefings.listar_categorias_restricao()) == 15
    assert len(ambiente.briefings.listar_categorias_pretensao()) == 18


def test_cria_edita_remove_prioridade_contextual_e_impede_duplicata() -> None:
    ambiente, campanha, segmentos, pracas = _preparar()
    entrada = SalvarPrioridadeEntrada("PRACA", pracas[0], 5, 1, "Praça principal")
    resumo = ambiente.briefings.salvar_prioridade(campanha, entrada)
    prioridade = resumo.prioridades_contextuais[0]
    assert prioridade.rotulo_entidade == "Praça A"
    with pytest.raises(ValueError, match="duplicada"):
        ambiente.briefings.salvar_prioridade(campanha, entrada)
    resumo = ambiente.briefings.salvar_prioridade(
        campanha, SalvarPrioridadeEntrada("SEGMENTO", segmentos[0], 4, None, None),
        prioridade.id_prioridade,
    )
    assert resumo.prioridades_contextuais[0].tipo_entidade == "SEGMENTO"
    assert ambiente.briefings.remover_prioridade(
        campanha, prioridade.id_prioridade
    ).prioridades_contextuais == ()


def test_restricao_preserva_declaracao_e_produz_diagnosticos() -> None:
    ambiente, campanha, _, _ = _preparar()
    entrada = SalvarRestricaoEntrada(
        "LEGAL", "Vedação declarada", None, 5, 5, "Jurídico", None, None, None
    )
    resumo = ambiente.briefings.salvar_restricao(campanha, entrada)
    restricao = resumo.restricoes[0]
    assert set(restricao.diagnosticos) == {
        "Restrição sem entidade afetada.",
        "Restrição legal sem fundamento informado.",
        "Restrição de alta intensidade sem justificativa.",
    }
    resumo = ambiente.briefings.salvar_restricao(
        campanha,
        SalvarRestricaoEntrada(
            "LEGAL", "Vedação ajustada", "Campanha", 5, 4, "Jurídico",
            "Obrigação legal", "Parecer 1", None,
        ),
        restricao.id_restricao,
    )
    assert resumo.restricoes[0].diagnosticos == ()
    assert ambiente.briefings.remover_restricao(
        campanha, restricao.id_restricao
    ).restricoes == ()


def test_cria_edita_remove_pretensao_com_relacoes() -> None:
    ambiente, campanha, segmentos, pracas = _preparar()
    resumo = ambiente.briefings.adicionar_publico(
        campanha, _entrada(segmentos, pracas)
    )
    publico = resumo.publicos[0]
    entrada = SalvarPretensaoEntrada(
        "AMPLIAR_PRESENCA", None, 5, 4, publico.id_publico, pracas[0],
        None, None, "Negociável", "Declaração do anunciante",
    )
    resumo = ambiente.briefings.salvar_pretensao(campanha, entrada)
    pretensao = resumo.pretensoes[0]
    assert pretensao.nome_publico == "Público principal"
    assert pretensao.nome_praca == "Praça A"
    resumo = ambiente.briefings.salvar_pretensao(
        campanha,
        SalvarPretensaoEntrada(
            "OUTRA", "Demonstrar atuação", 3, 3, None, None, None,
            None, None, None,
        ),
        pretensao.id_pretensao,
    )
    assert resumo.pretensoes[0].descricao_controlada == "Demonstrar atuação"
    assert ambiente.briefings.remover_pretensao(
        campanha, pretensao.id_pretensao
    ).pretensoes == ()


def test_rejeita_referencias_e_categorias_invalidas() -> None:
    ambiente, campanha, _, _ = _preparar()
    with pytest.raises(ValueError, match="Público da Pretensão não existe"):
        ambiente.briefings.salvar_pretensao(
            campanha,
            SalvarPretensaoEntrada(
                "APOIAR_VENDAS", None, 3, 3, uuid4(), None, None,
                None, None, None,
            ),
        )
    with pytest.raises(ValueError, match="outra pretensão"):
        ambiente.briefings.salvar_pretensao(
            campanha,
            SalvarPretensaoEntrada(
                "OUTRA", None, 3, 3, None, None, None, None, None, None,
            ),
        )
