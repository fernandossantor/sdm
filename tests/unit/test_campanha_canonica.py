from runpy import run_path


def _campanha_canonica():
    namespace = run_path("tests/fixtures/campanha_canonica.py")
    return namespace["CAMPANHA_CANONICA"]


def test_caso_canonico_tem_as_quantidades_exigidas():
    campanha = _campanha_canonica()

    assert len(campanha["objetivos_marketing"]) == 2
    assert len(campanha["objetivos_comunicacao_candidatos"]) == 3
    assert campanha["publico_prioritario"]["prioridade"] == "muito alta"
    assert campanha["segmento_secundario"]["prioridade"] == "média"


def test_dados_ausentes_sao_none_e_nunca_zero():
    campanha = _campanha_canonica()
    ausentes = campanha["dados_ausentes"]

    assert ausentes
    assert all(valor is None for valor in ausentes.values())
    assert not any(valor == 0 for valor in ausentes.values())


def test_indicadores_disponiveis_preservam_contexto_minimo_de_mensuracao():
    campanha = _campanha_canonica()
    campos_obrigatorios = {
        "metrica",
        "valor",
        "unidade_de_mensuracao",
        "natureza_do_valor",
        "publico_ou_target",
        "territorio",
        "periodo_de_referencia",
        "fonte",
        "metodologia",
        "nivel_de_confianca",
    }

    assert campanha["indicadores_disponiveis"]
    assert all(
        campos_obrigatorios <= indicador.keys()
        for indicador in campanha["indicadores_disponiveis"]
    )
