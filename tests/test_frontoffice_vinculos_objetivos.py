from dataclasses import replace

import pytest
from streamlit.testing.v1 import AppTest


APP = '''
import streamlit as st
from test_vinculos_objetivos import _ambiente_vinculos
from mediad_planner.presentation.objetivos_declarados import apresentar_objetivos_declarados
from mediad_planner.presentation.segmentos import apresentar_segmentos
if "ambiente" not in st.session_state:
    st.session_state.ambiente, st.session_state.campanha = _ambiente_vinculos()
ambiente, campanha = st.session_state.ambiente, st.session_state.campanha
resumo = ambiente.briefings.abrir_briefing(campanha)
tela = st.radio("Tela", ("Objetivos", "Públicos"))
if tela == "Objetivos":
    apresentar_objetivos_declarados(ambiente.briefings, campanha, resumo)
else:
    apresentar_segmentos(ambiente.briefings, campanha, resumo)
'''


def _resumo(app):
    return app.session_state.ambiente.briefings.abrir_briefing(app.session_state.campanha)


def _chave(app, objetivo):
    return f"vinculos_objetivo_{app.session_state.campanha}_{objetivo.id_objetivo}"


def _salvar(app, objetivo):
    next(item for item in app.button
         if item.label == "Salvar vínculos do Objetivo" and str(objetivo.id_objetivo) in item.key).click().run()
    # Completa a renderização após o st.rerun do salvamento.
    app.run()
    assert not app.exception
    assert not app.error


@pytest.mark.parametrize("grupo", ("objetivos_marketing", "objetivos_comunicacao"))
def test_interface_salva_reabre_altera_e_retira_vinculos_sem_mudar_objetivo(grupo):
    app = AppTest.from_string(APP).run()
    original = _resumo(app)
    objetivo = getattr(original, grupo)[0]
    chave = _chave(app, objetivo)
    publicos = tuple(item.id_publico for item in original.publicos)
    pracas = tuple(item.id_praca for item in original.pracas)
    assert app.multiselect(f"{chave}_publicos").options == [
        "1. Público com mesmo nome", "2. Público com mesmo nome",
    ]
    assert app.multiselect(f"{chave}_pracas").options == [
        "1. [Município] Praça A", "2. [Município] Praça B",
    ]
    for ids_publicos, ids_pracas in ((publicos, pracas), (publicos[1:], ()), ((), ())):
        app.multiselect(f"{chave}_publicos").set_value(list(ids_publicos))
        app.multiselect(f"{chave}_pracas").set_value(list(ids_pracas))
        _salvar(app, objetivo)
        salvo = _resumo(app)
        assert getattr(salvo, grupo)[0] == replace(objetivo,
            ids_publicos_relacionados=ids_publicos, ids_pracas_relacionadas=ids_pracas)
        outro = "objetivos_comunicacao" if grupo == "objetivos_marketing" else "objetivos_marketing"
        assert getattr(salvo, outro) == getattr(original, outro)
        app.radio[0].set_value("Públicos").run()
        app.radio[0].set_value("Objetivos").run()
        assert not app.exception
        assert tuple(app.multiselect(f"{chave}_publicos").value) == ids_publicos
        assert tuple(app.multiselect(f"{chave}_pracas").value) == ids_pracas
    assert any("Nenhum vínculo declarado" in item.value for item in app.markdown)


def test_escolha_nao_salva_permanece_distinta_do_vinculo_declarado():
    app = AppTest.from_string(APP).run()
    original = _resumo(app)
    objetivo = original.objetivos_marketing[0]
    chave = _chave(app, objetivo)
    app.multiselect(f"{chave}_publicos").set_value([original.publicos[0].id_publico])
    app.radio[0].set_value("Públicos").run()
    assert _resumo(app) == original
    app.radio[0].set_value("Objetivos").run()
    assert not app.exception
    assert app.multiselect(f"{chave}_publicos").value == []


@pytest.mark.parametrize("grupo", ("objetivos_marketing", "objetivos_comunicacao"))
def test_interface_protege_publico_vinculado_e_orienta_retirada(grupo):
    app = AppTest.from_string(APP).run()
    original = _resumo(app)
    objetivo = getattr(original, grupo)[0]
    chave = _chave(app, objetivo)
    publico = original.publicos[0]
    app.multiselect(f"{chave}_publicos").set_value([publico.id_publico])
    _salvar(app, objetivo)
    vinculado = _resumo(app)
    app.radio[0].set_value("Públicos").run()
    next(item for item in app.button
         if item.label == "Remover Público" and str(publico.id_publico) in item.key).click().run()
    assert not app.exception
    assert any("Retire o vínculo no Objetivo" in item.value for item in app.error)
    assert _resumo(app) == vinculado
    app.radio[0].set_value("Objetivos").run()
    app.multiselect(f"{chave}_publicos").set_value([])
    _salvar(app, objetivo)
    app.radio[0].set_value("Públicos").run()
    next(item for item in app.button
         if item.label == "Remover Público" and str(publico.id_publico) in item.key).click().run()
    assert not app.exception
    assert publico.id_publico not in {item.id_publico for item in _resumo(app).publicos}


def test_objetivo_sem_publicos_ou_pracas_pode_continuar_sem_vinculos():
    app = AppTest.from_string('''
import streamlit as st
from test_casos_uso_objetivos_declarados import ambiente_aberto, entrada_marketing
from mediad_planner.presentation.objetivos_declarados import apresentar_objetivos_declarados
if "ambiente" not in st.session_state:
    ambiente, campanha = ambiente_aberto()
    ambiente.briefings.adicionar_objetivo_marketing(campanha, entrada_marketing())
    st.session_state.ambiente, st.session_state.campanha = ambiente, campanha
ambiente, campanha = st.session_state.ambiente, st.session_state.campanha
apresentar_objetivos_declarados(ambiente.briefings, campanha, ambiente.briefings.abrir_briefing(campanha))
''').run()
    assert not app.exception
    objetivo = _resumo(app).objetivos_marketing[0]
    chave = _chave(app, objetivo)
    assert app.multiselect(f"{chave}_publicos").options == []
    assert app.multiselect(f"{chave}_pracas").options == []
    assert any("Cadastre Públicos" in item.value for item in app.info)
    assert any("Cadastre Praças" in item.value for item in app.info)
    _salvar(app, objetivo)
    assert _resumo(app).objetivos_marketing[0] == objetivo
