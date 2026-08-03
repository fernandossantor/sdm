from mediad_planner.application.dto.campanha import CriarCampanhaEntrada
from mediad_planner.application.dto.praca_universo import (
    AdicionarPracaEntrada,
    AdicionarUniversoEntrada,
)
from mediad_planner.composition.ambiente import construir_ambiente_aplicacao_em_memoria


def test_mapper_preserva_decimais_rotulos_relacoes_e_opcionais() -> None:
    ambiente = construir_ambiente_aplicacao_em_memoria()
    campanha = ambiente.campanhas.criar_campanha(
        CriarCampanhaEntrada(
            nome="Campanha", nome_anunciante="A", nome_marca=None,
            nome_produto_servico=None, nome_planejador_responsavel="P",
            nomes_equipe=(), observacao_inicial=None, iniciar_briefing=True,
        )
    )
    ambiente.espaco_trabalho.preparar_briefing(campanha.id_campanha)
    resumo = ambiente.briefings.adicionar_praca(
        campanha.id_campanha,
        AdicionarPracaEntrada(
            tipo="MUNICIPIO", nome="São Borja", codigo_oficial="4318002",
            abrangencia=None, valor_populacao_referencia="60000.50",
            codigo_unidade_populacional="pessoas",
            unidade_populacional="forjado", fonte=None,
            data_referencia=None, observacao=None,
        ),
    )
    id_praca = resumo.pracas[0].id_praca
    resumo = ambiente.briefings.adicionar_universo(
        campanha.id_campanha,
        AdicionarUniversoEntrada(
            nome="Adultos", definicao="Pessoas com 18 anos ou mais",
            ids_pracas=(id_praca,), valor_populacional="45000.00",
            codigo_unidade=None, unidade="Indivíduos", fonte=None,
            data_referencia=None, criterios_inclusao=None,
            criterios_exclusao=None, observacao=None,
        ),
    )
    praca = resumo.pracas[0]
    universo = resumo.universos[0]
    assert praca.valor_populacao_referencia == "60000.50"
    assert praca.rotulo_tipo == "Município"
    assert praca.unidade_populacional == "Pessoas"
    assert universo.valor_populacional == "45000.00"
    assert universo.codigo_unidade is None
    assert universo.ids_pracas == (id_praca,)
    assert universo.rotulos_pracas == (
        "[Município] São Borja — 4318002",
    )
    assert universo.fonte is None
