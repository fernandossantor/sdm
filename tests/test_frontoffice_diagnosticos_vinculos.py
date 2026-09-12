import pytest
from streamlit.testing.v1 import AppTest

from test_frontoffice_vinculos_objetivos import APP, _resumo, _chave, _salvar


APP_REVISAO = APP.replace(
    'from mediad_planner.presentation.segmentos import apresentar_segmentos',
    'from mediad_planner.presentation.segmentos import apresentar_segmentos\n'
    'from mediad_planner.presentation.revisao_briefing import apresentar_revisao_briefing',
).replace('(\"Objetivos\", \"Públicos\")', '(\"Objetivos\", \"Públicos\", \"Revisão\")').replace(
    'else:\n    apresentar_segmentos', 'elif tela == "Públicos":\n    apresentar_segmentos',
) + '\nelse:\n    apresentar_revisao_briefing(resumo)\n'


def _avisos(app):
    return [a.value for a in app.warning if "prioritário (prioridade" in a.value]


@pytest.mark.parametrize("grupo", ("objetivos_marketing", "objetivos_comunicacao"))
def test_vinculos_recalculam_avisos_nas_subetapas_e_revisao(grupo):
    app = AppTest.from_string(APP_REVISAO).run()
    assert not app.exception
    original = _resumo(app)
    objetivo = getattr(original, grupo)[0]
    chave = _chave(app, objetivo)
    locais_objetivos = _avisos(app)
    assert len(locais_objetivos) == 4
    app.radio[0].set_value("Públicos").run()
    locais_publicos = _avisos(app)
    assert len(locais_publicos) == 2
    app.radio[0].set_value("Revisão").run()
    assert not app.exception
    assert _avisos(app) == locais_objetivos + locais_publicos
    app.radio[0].set_value("Objetivos").run()
    for publicos, pracas, quantidade_objetivos, quantidade_publicos in (
        ([original.publicos[0].id_publico], [], 3, 1),
        ([original.publicos[0].id_publico], [original.pracas[0].id_praca], 2, 1),
        ([], [], 4, 2),
    ):
        app.multiselect(f"{chave}_publicos").set_value(publicos)
        app.multiselect(f"{chave}_pracas").set_value(pracas)
        _salvar(app, objetivo)
        assert len(_avisos(app)) == quantidade_objetivos
        app.radio[0].set_value("Revisão").run()
        assert not app.exception
        assert len(_avisos(app)) == quantidade_objetivos + quantidade_publicos
        app.radio[0].set_value("Públicos").run()
        assert len(_avisos(app)) == quantidade_publicos
        app.radio[0].set_value("Objetivos").run()
