from streamlit.testing.v1 import AppTest


APP = '''
import streamlit as st
from test_aplicabilidade_jornada import _com_dois_publicos
from mediad_planner.presentation.briefings import _apresentar_subetapas
from mediad_planner.presentation.jornada import apresentar_jornada
from mediad_planner.presentation.revisao_briefing import apresentar_revisao_briefing
if "ambiente" not in st.session_state:
    ambiente, campanha, _ = _com_dois_publicos()
    st.session_state.ambiente = ambiente
    st.session_state.campanha = campanha
ambiente, campanha = st.session_state.ambiente, st.session_state.campanha
resumo = ambiente.briefings.abrir_briefing(campanha)
_apresentar_subetapas(resumo)
apresentar_jornada(ambiente.briefings, campanha, resumo)
apresentar_revisao_briefing(resumo)
'''


def _selecionar(app, rotulo, valor):
    next(item for item in app.selectbox if item.label == rotulo).set_value(valor).run()
    assert not app.exception


def _salvar(app, valor):
    _selecionar(app, "Aplicabilidade da Jornada", valor)
    next(item for item in app.button if item.label == "Salvar aplicabilidade da Jornada").click().run()
    assert not app.exception


def test_aplicabilidade_por_publico_reabre_e_filtra_opcoes_da_jornada():
    app = AppTest.from_string(APP).run()
    assert not app.exception
    assert any("Público 1: sem jornada vinculada; verificar se" in item.value for item in app.warning)
    _salvar(app, "Não aplicável")
    assert any("Jornada não aplicável para Público 1" in item.value for item in app.markdown)
    assert not any("Público 1: sem jornada" in item.value for item in app.warning)
    assert any("Público 2: sem jornada" in item.value for item in app.warning)
    assert any(item.value == "**5. Jornada** — Em preenchimento" for item in app.markdown)
    publicos_jornada = next(item for item in app.multiselect if item.label == "Públicos associados à Jornada")
    assert len(publicos_jornada.options) == 1
    assert publicos_jornada.options[0].startswith("Público 2")
    seletor = next(item for item in app.selectbox if item.label == "Público para declarar aplicabilidade")
    primeiro, segundo = seletor.options
    _selecionar(app, "Público para declarar aplicabilidade", segundo)
    assert next(item for item in app.selectbox if item.label == "Aplicabilidade da Jornada").value == "Não informada"
    _selecionar(app, "Público para declarar aplicabilidade", primeiro)
    assert next(item for item in app.selectbox if item.label == "Aplicabilidade da Jornada").value == "Não aplicável"
    _salvar(app, "Aplicável")
    assert any("Público 1: jornada declarada aplicável" in item.value for item in app.warning)
    _salvar(app, "Não informada")
    assert any("Público 1: sem jornada vinculada; verificar se" in item.value for item in app.warning)
    assert not any("Declaração do usuário" in item.value for item in app.markdown)
    _salvar(app, "Não aplicável")
    _selecionar(app, "Público para declarar aplicabilidade", segundo)
    _salvar(app, "Não aplicável")
    assert not any(item.label == "Criar Jornada" for item in app.button)
    assert any("não aplicável para todos" in item.value for item in app.info)
    assert not any("sem jornada vinculada" in item.value for item in app.warning)
    _salvar(app, "Não informada")
    assert any(item.label == "Criar Jornada" for item in app.button)


def test_conflito_na_interface_preserva_jornada_e_declaracao_salva():
    app = AppTest.from_string(APP).run()
    _salvar(app, "Aplicável")
    next(item for item in app.text_input if item.label == "Nome da Jornada").set_value("Jornada do público 1")
    associados = next(item for item in app.multiselect if item.label == "Públicos associados à Jornada")
    associados.set_value([associados.options[0]])
    next(item for item in app.button if item.label == "Criar Jornada").click().run()
    assert not app.exception
    _salvar(app, "Não aplicável")
    assert any("não aplicável não pode ter Jornada vinculada" in item.value for item in app.error)
    assert any("Jornada do público 1" in item.value for item in app.markdown)
    assert any("Jornada aplicável para Público 1" in item.value for item in app.markdown)
    assert not any("Jornada não aplicável para Público 1" in item.value for item in app.markdown)
