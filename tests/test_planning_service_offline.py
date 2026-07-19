from application.services.planning_service import PlanningService


def briefing_offline():
    return {
        "id": "briefing-offline",
        "nome": "Campanha Offline",
        "anunciante": "Cliente Teste",
        "objetivo_id": "objetivo-performance",
        "objetivo": {
            "id": "objetivo-performance",
            "nome": "Performance",
        },
        "orcamento": 1000.0,
        "audiencias": [
            {
                "audiencia_id": "audiencia-1",
                "peso": 100,
            }
        ],
        "inventarios": [
            {
                "id": "inv-1",
                "nome": "Search Ads",
                "plataforma": "Google",
                "ambiente": "Search",
                "score_objetivo": 25,
                "score_kpi": 25,
                "score_publico": 20,
                "score_contexto": 10,
                "score_consumo": 10,
                "score_sinergia": 5,
                "penalidade": 0,
            },
            {
                "id": "inv-2",
                "nome": "Social Ads",
                "plataforma": "Meta",
                "ambiente": "Social",
                "score_objetivo": 18,
                "score_kpi": 15,
                "score_publico": 18,
                "score_contexto": 8,
                "score_consumo": 8,
                "score_sinergia": 3,
                "penalidade": 0,
            },
        ],
        "inventarios_objetivos": [],
        "inventarios_kpis": [],
        "metricas": [],
        "consumo": [],
        "parametros": {},
        "restricoes": [],
    }


def test_planning_service_executa_pipeline_offline():
    resultado = PlanningService().executar(
        briefing_offline()
    )

    assert "contexto" in resultado
    assert "ranking" in resultado
    assert "plano_tatico" in resultado
    assert "plano" in resultado
    assert "dashboard" in resultado
    assert "report" in resultado

    assert len(resultado["ranking"]) == 2
    assert resultado["ranking"][0]["inventario"] == "Search Ads"

    plano_tatico = resultado["plano_tatico"]

    assert plano_tatico.verba_total == 1000.0
    assert plano_tatico.verba_distribuida == 1000.0
    assert len(plano_tatico.itens) == 2

    plano = resultado["plano"]

    assert plano["verba_total"] == 1000.0
    assert len(plano["inventarios"]) == 2
