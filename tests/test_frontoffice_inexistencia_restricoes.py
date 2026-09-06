from pathlib import Path

from streamlit.testing.v1 import AppTest

from test_frontoffice_briefing import _preservar_estado_do_formulario


def _abrir_condicoes():
    app = AppTest.from_file(str(Path(__file__).parents[1] / "app.py")).run()
    campos = {item.label: item for item in app.text_input}
    campos["Nome da Campanha"].set_value("Campanha sem restrições")
    campos["Anunciante"].set_value("Anunciante")
    campos["Planejador Responsável"].set_value("Planejadora")
    next(item for item in app.button if item.label == "Criar Campanha e iniciar Briefing").click().run()
    next(item for item in app.button if item.label == "Continuar no Briefing").click()
    _preservar_estado_do_formulario(app)
    app.run()
    _navegar(app, "Prioridades, restrições e pretensões")
    return app


def _navegar(app, subetapa):
    next(item for item in app.radio if item.label == "Subetapa em preenchimento").set_value(subetapa).run()
    assert not app.exception


def _botao(app, rotulo):
    return next(item for item in app.button if item.label == rotulo)


def test_declarar_reabrir_revisar_e_retirar_pela_interface():
    app = _abrir_condicoes()
    _botao(app, "Declarar inexistência de restrições").click().run()
    assert not app.exception
    assert any("Declaração salva" in item.value for item in app.markdown)
    assert not any(item.label == "Criar Restrição" for item in app.button)
    assert any("**7. Prioridades, restrições e pretensões** — Em preenchimento" == item.value for item in app.markdown)
    _navegar(app, "Revisão do Briefing")
    assert any("Declaração do usuário" in item.value for item in app.markdown)
    assert not any("Nenhuma restrição registrada" in item.value for item in app.warning)
    assert any("Nenhuma pretensão" in item.value for item in app.warning)
    assert any("revisão é parcial" in item.value for item in app.info)
    _navegar(app, "Prioridades, restrições e pretensões")
    _botao(app, "Retirar declaração de inexistência de restrições").click().run()
    assert not app.exception
    assert _botao(app, "Criar Restrição")
    _navegar(app, "Revisão do Briefing")
    assert not any("Declaração do usuário" in item.value for item in app.markdown)
    assert any("Nenhuma restrição registrada" in item.value for item in app.warning)
    assert {item.label: str(item.value) for item in app.metric}["Estado"] == "Em preenchimento"


def test_registros_exigem_revisao_e_remocao_nao_declara_inexistencia():
    app = _abrir_condicoes()
    next(item for item in app.text_area if item.label == "Descrição estruturada da Restrição").set_value("Prazo de produção")
    _botao(app, "Criar Restrição").click().run()
    assert not app.exception
    assert _botao(app, "Declarar inexistência de restrições").disabled
    assert any("Prazo de produção" in item.value for item in app.markdown)
    _botao(app, "Remover Restrição").click().run()
    assert not app.exception
    assert not _botao(app, "Declarar inexistência de restrições").disabled
    assert not any("Declaração salva" in item.value for item in app.markdown)
    _navegar(app, "Revisão do Briefing")
    assert any("Nenhuma restrição registrada" in item.value for item in app.warning)
