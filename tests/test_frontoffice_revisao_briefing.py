from pathlib import Path

from streamlit.testing.v1 import AppTest

from test_frontoffice_briefing import _preservar_estado_do_formulario


def test_revisao_acessivel_apresenta_lacunas_e_preserva_rascunho():
    app = AppTest.from_file(str(Path(__file__).parents[1] / "app.py")).run()
    campos = {item.label: item for item in app.text_input}
    campos["Nome da Campanha"].set_value("Campanha revisão")
    campos["Anunciante"].set_value("Anunciante")
    campos["Planejador Responsável"].set_value("Planejadora")
    next(item for item in app.button if item.label == "Criar Campanha e iniciar Briefing").click().run()
    next(item for item in app.button if item.label == "Continuar no Briefing").click()
    _preservar_estado_do_formulario(app)
    app.run()
    next(item for item in app.radio if item.label == "Subetapa em preenchimento").set_value("Revisão do Briefing").run()
    assert not app.exception
    assert any("Nenhum objetivo de marketing" in item.value for item in app.warning)
    assert any("revisão é parcial" in item.value for item in app.info)
    assert {item.label: str(item.value) for item in app.metric}["Estado"] == "Rascunho"
    assert not any("Concluir" in item.label for item in app.button)
    next(item for item in app.radio if item.label == "Subetapa em preenchimento").set_value("Situação mercadológica e competitiva").run()
    assert not app.exception
    assert any(item.label == "Fonte dos dados (opcional)" for item in app.text_input)


def test_ausencia_de_apontamentos_nao_certifica_conclusao():
    app = AppTest.from_string('''
from dataclasses import replace
from mediad_planner.presentation.revisao_briefing import apresentar_revisao_briefing
from mediad_planner.application.mappers.briefing import resumir_briefing
from test_briefing_dominio import briefing
apresentar_revisao_briefing(replace(resumir_briefing(briefing()), apontamentos_revisao=()))
''').run()
    assert not app.exception
    assert not app.success
    assert any("Isso não certifica" in item.value for item in app.markdown)
