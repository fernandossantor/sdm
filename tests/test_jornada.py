from uuid import uuid4

import pytest

from mediad_planner.application.dto.jornada import (
    SalvarEtapaJornadaEntrada,
    SalvarJornadaEntrada,
)
from test_publicos import _entrada, _preparar


def _com_publico():
    ambiente, campanha, segmentos, pracas = _preparar()
    resumo = ambiente.briefings.adicionar_publico(
        campanha, _entrada(segmentos, pracas)
    )
    return ambiente, campanha, resumo.publicos[0].id_publico


def _jornada(publico):
    return SalvarJornadaEntrada(
        nome="Jornada de compra",
        descricao="Percurso declarado",
        ids_publicos=(publico,),
        referencia_modelo=None,
        adaptada_localmente=True,
    )


def _etapa(publico, **mudancas):
    dados = dict(
        categoria="CONSIDERACAO", ordem=2, existe=True, relevancia=4,
        intensidade=3, prioridade=5, ids_publicos=(publico,),
        ids_objetivos_comunicacao=(), situacao_atual="Compara opções",
        situacao_pretendida="Reconhece diferenciais", observacao=None,
    )
    dados.update(mudancas)
    return SalvarEtapaJornadaEntrada(**dados)


def test_catalogo_tem_dez_categorias_normativas() -> None:
    ambiente, _, _ = _com_publico()
    assert tuple(
        item.codigo for item in ambiente.briefings.listar_categorias_etapa_jornada()
    ) == (
        "DESCOBERTA", "CONHECIMENTO", "CONSIDERACAO", "AVALIACAO",
        "DECISAO", "COMPRA", "EXPERIENCIA", "RECOMPRA", "FIDELIZACAO",
        "RECOMENDACAO",
    )


def test_cria_edita_remove_jornada_e_etapa() -> None:
    ambiente, campanha, publico = _com_publico()
    resumo = ambiente.briefings.adicionar_jornada(campanha, _jornada(publico))
    jornada = resumo.jornadas[0]
    resumo = ambiente.briefings.adicionar_etapa_jornada(
        campanha, jornada.id_jornada, _etapa(publico)
    )
    etapa = resumo.jornadas[0].etapas[0]
    assert etapa.rotulo_categoria == "Consideração"
    assert etapa.nomes_publicos == ("Público principal",)
    resumo = ambiente.briefings.editar_etapa_jornada(
        campanha, jornada.id_jornada, etapa.id_etapa,
        _etapa(publico, categoria="DECISAO", ordem=3),
    )
    assert resumo.jornadas[0].etapas[0].rotulo_categoria == "Decisão"
    resumo = ambiente.briefings.remover_etapa_jornada(
        campanha, jornada.id_jornada, etapa.id_etapa
    )
    assert resumo.jornadas[0].etapas == ()
    assert ambiente.briefings.remover_jornada(
        campanha, jornada.id_jornada
    ).jornadas == ()


@pytest.mark.parametrize(
    ("mudancas", "mensagem"),
    (
        ({"ids_publicos": ()}, "Público associado"),
        ({"prioridade": 6}, "entre 1 e 5"),
        ({"ordem": 0}, "inteiro positivo"),
        ({"categoria": "INVENTADA"}, "Categoria de etapa inválida"),
    ),
)
def test_rejeita_etapa_incoerente(mudancas, mensagem) -> None:
    ambiente, campanha, publico = _com_publico()
    jornada = ambiente.briefings.adicionar_jornada(
        campanha, _jornada(publico)
    ).jornadas[0]
    with pytest.raises(ValueError, match=mensagem):
        ambiente.briefings.adicionar_etapa_jornada(
            campanha, jornada.id_jornada, _etapa(publico, **mudancas)
        )


def test_protege_publico_e_valida_objetivo_de_comunicacao() -> None:
    ambiente, campanha, publico = _com_publico()
    jornada = ambiente.briefings.adicionar_jornada(
        campanha, _jornada(publico)
    ).jornadas[0]
    with pytest.raises(ValueError, match="Objetivo de Comunicação"):
        ambiente.briefings.adicionar_etapa_jornada(
            campanha, jornada.id_jornada,
            _etapa(publico, ids_objetivos_comunicacao=(uuid4(),)),
        )
    with pytest.raises(ValueError, match="vinculado a Jornada"):
        ambiente.briefings.remover_publico(campanha, publico)
