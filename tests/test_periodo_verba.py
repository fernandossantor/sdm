import pytest

from mediad_planner.application.dto.campanha import CriarCampanhaEntrada
from mediad_planner.application.dto.periodo_verba import (
    IntervaloDeclaradoEntrada,
    SalvarPeriodoVerbaEntrada,
)
from mediad_planner.composition.ambiente import construir_ambiente_aplicacao_em_memoria


def _preparar():
    ambiente = construir_ambiente_aplicacao_em_memoria()
    campanha = ambiente.campanhas.criar_campanha(CriarCampanhaEntrada(
        nome="Campanha", nome_anunciante="Anunciante", nome_marca=None,
        nome_produto_servico=None, nome_planejador_responsavel="Planejadora",
        nomes_equipe=(), observacao_inicial=None, iniciar_briefing=True,
    ))
    ambiente.espaco_trabalho.preparar_briefing(campanha.id_campanha)
    return ambiente, campanha.id_campanha


def _entrada(**mudancas):
    dados = dict(
        data_inicial="2027-01-01", data_final="2027-01-31",
        duracao=None, datas_criticas=("2027-01-15",),
        sazonalidades=("Férias de verão",),
        eventos_condicionantes=("Lançamento",),
        periodos_obrigatorios=(
            IntervaloDeclaradoEntrada("2027-01-10", "2027-01-20", "Lançamento"),
        ),
        periodos_vedados=(), observacao_periodo=None,
        valor_total="100000", moeda="BRL", natureza_limite="FLEXIVEL",
        margem_flexibilidade="até 10%", valor_minimo="90000",
        valor_maximo="110000", parcela_comprometida="20000",
        observacao_verba=None,
    )
    dados.update(mudancas)
    return SalvarPeriodoVerbaEntrada(**dados)


def test_catalogo_de_naturezas_e_criacao_editavel() -> None:
    ambiente, campanha = _preparar()
    assert tuple(item.codigo for item in ambiente.briefings.listar_naturezas_limite_verba()) == (
        "RIGIDO", "FLEXIVEL", "ESTIMADO", "AINDA_NAO_DEFINIDO",
    )
    resumo = ambiente.briefings.definir_periodo_verba(campanha, _entrada())
    assert resumo.periodo_verba.data_inicial == "2027-01-01"
    assert resumo.periodo_verba.valor_total == "100000"
    assert resumo.periodo_verba.diagnosticos == ()
    atualizado = ambiente.briefings.definir_periodo_verba(
        campanha, _entrada(valor_total="120000", natureza_limite="ESTIMADO")
    )
    assert atualizado.periodo_verba.valor_total == "120000"
    assert atualizado.periodo_verba.rotulo_natureza_limite == "Estimado"


def test_preserva_incoerencias_declaradas_e_as_sinaliza() -> None:
    ambiente, campanha = _preparar()
    resumo = ambiente.briefings.definir_periodo_verba(campanha, _entrada(
        data_inicial="2027-02-01", data_final="2027-01-01",
        periodos_obrigatorios=(
            IntervaloDeclaradoEntrada("2026-12-01", "2026-12-10", None),
        ),
        valor_total="100", moeda=None, natureza_limite="RIGIDO",
        margem_flexibilidade="10", valor_minimo="200", valor_maximo="150",
        parcela_comprometida="120",
    ))
    diagnosticos = resumo.periodo_verba.diagnosticos
    assert "Data final anterior à inicial." in diagnosticos
    assert "Período obrigatório fora do intervalo principal." in diagnosticos
    assert "Moeda ausente." in diagnosticos
    assert "Valor máximo inferior ao mínimo." in diagnosticos
    assert "Parcela comprometida superior ao total." in diagnosticos
    assert "Limite rígido com margem de flexibilidade incompatível." in diagnosticos


@pytest.mark.parametrize(
    ("mudancas", "mensagem"),
    (
        ({"data_inicial": "01/01/2027"}, "AAAA-MM-DD"),
        ({"valor_total": "1,50"}, "Valor total inválido"),
        ({"natureza_limite": "OUTRA"}, "Natureza do limite inválida"),
        ({"periodos_vedados": (IntervaloDeclaradoEntrada("2027-02-02", "2027-01-01", None),)}, "anterior"),
    ),
)
def test_rejeita_formato_invalido(mudancas, mensagem) -> None:
    ambiente, campanha = _preparar()
    with pytest.raises(ValueError, match=mensagem):
        ambiente.briefings.definir_periodo_verba(campanha, _entrada(**mudancas))


@pytest.mark.parametrize("natureza", ("AINDA_NAO_DEFINIDO", "ESTIMADO"))
def test_distingue_verba_ausente_de_declaracao_ainda_nao_definida(natureza) -> None:
    ambiente, campanha = _preparar()
    resumo = ambiente.briefings.definir_periodo_verba(campanha, _entrada(
        data_inicial=None, data_final=None, duracao=None, datas_criticas=(),
        sazonalidades=("Alta temporada",), valor_total=None, moeda=None,
        valor_minimo=None, valor_maximo=None, parcela_comprometida=None,
        margem_flexibilidade=None, natureza_limite=natureza,
        periodos_obrigatorios=(),
    ))
    assert "Duração ausente quando as datas não estão definidas." in resumo.periodo_verba.diagnosticos
    assert "Sazonalidade informada sem correspondência temporal." in resumo.periodo_verba.diagnosticos
    assert ("Verba ausente." in resumo.periodo_verba.diagnosticos) is (natureza == "ESTIMADO")
