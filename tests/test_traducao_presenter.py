from presentation.traducao_presenter import (
    AJUDAS,
    apresentar_contexto,
    apresentar_objetivos,
    apresentar_revisao,
    formatar_peso,
)
from tests.test_pesos_contextuais_traducao import _briefing, _traduzir


def test_prioridade_e_peso_sao_formatados_corretamente():
    contrato = _traduzir(_briefing())
    _, midia = apresentar_objetivos(contrato)

    assert midia[0].prioridade == "Alta"
    assert midia[0].peso_efetivo.endswith("%")
    assert formatar_peso(0.260769) == "26,1%"


def test_origem_distingue_calculado_e_ajustado():
    contrato = _traduzir(_briefing())
    _, midia = apresentar_objetivos(contrato)
    assert midia[0].origem_peso == "Calculado pelo motor"

    ajustado = contrato.model_copy(update={
        "objetivos_midia_derivados": (
            contrato.objetivos_midia_derivados[0].model_copy(update={
                "peso_ajustado": 0.3, "peso_efetivo": 0.3,
            }),
            *contrato.objetivos_midia_derivados[1:],
        )
    })
    assert apresentar_objetivos(ajustado)[1][0].origem_peso == (
        "Ajustado pelo planejador; calculado preservado"
    )


def test_ausencia_nao_aparece_como_zero():
    briefing = _briefing().model_copy(update={
        "conteudo": _briefing().conteudo.model_copy(update={
            "verba": {"natureza": "ainda não definido", "valor_total": None}
        })
    })
    assert formatar_peso(None) == "Pendente"
    assert next(item for item in apresentar_contexto(briefing) if item.titulo == "Verba").valor == "Pendente"


def test_empate_e_fatores_positivos_e_negativos_sao_apresentados():
    contrato = _traduzir(_briefing(comunicacao="conhecimento", restrita=True))
    _, midia = apresentar_objetivos(contrato)

    empatados = [item for item in midia if item.empate_tecnico]
    assert empatados
    assert all(item.fatores_positivos for item in midia)
    assert all(any("orçament" in fator for fator in item.fatores_negativos) for item in midia)


def test_memoria_tecnica_e_conceitos_permanecem_disponiveis_no_codigo_da_tela():
    interface = open("presentation/streamlit_app.py", encoding="utf-8").read()

    assert "Ver fundamentação técnica e rastreabilidade" in interface
    for conceito in ("forca_padrao", "pontuacao_contextual", "peso_calculado", "peso_ajustado", "peso_efetivo", "confianca", "condicao", "restricao", "tensao", "efeito_arquitetura"):
        assert conceito in AJUDAS


def test_interface_nao_reimplementa_formula_e_revisao_expoe_delta():
    interface = open("presentation/streamlit_app.py", encoding="utf-8").read()
    contrato = _traduzir(_briefing())
    proposta = apresentar_revisao(contrato, ("construir alcance",))

    assert "CONFIGURACAO_PONTUACAO" not in interface
    assert "pontuacao_contextual =" not in interface
    assert proposta[0]["Valor calculado"] != "Pendente"
    assert proposta[1]["Novo valor proposto"] == "Não adotar"
    assert "nova versão" in proposta[1]["Efeito estimado"]
