from mediad_planner.composition.ambiente import construir_ambiente_aplicacao_em_memoria


def test_ambiente_contem_catalogo_sem_consulta_http() -> None:
    ambiente = construir_ambiente_aplicacao_em_memoria()
    assert callable(ambiente.catalogo_territorial.listar_estados)
    assert callable(ambiente.catalogo_territorial.listar_municipios)


def test_composicao_usa_adaptador_local() -> None:
    from pathlib import Path
    from mediad_planner.composition import catalogo_territorial

    fonte = Path(catalogo_territorial.__file__).read_text(encoding="utf-8")
    assert "CatalogoTerritorialLocal" in fonte
    assert "CatalogoTerritorialIBGE" not in fonte


def test_aplicacao_expoe_quatro_operacoes_territoriais() -> None:
    ambiente = construir_ambiente_aplicacao_em_memoria()
    aplicacao = ambiente.catalogo_territorial
    assert callable(aplicacao.listar_estados)
    assert callable(aplicacao.listar_municipios)
    assert callable(aplicacao.listar_regioes_intermediarias)
    assert callable(aplicacao.listar_regioes_imediatas)
