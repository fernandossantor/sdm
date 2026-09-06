import pytest
from streamlit.testing.v1 import AppTest


APP = '''
import streamlit as st
from test_jornada import _com_publico, _jornada, _etapa
from mediad_planner.application.dto.condicoes_declaradas import SalvarPrioridadeEntrada
from mediad_planner.presentation.condicoes_declaradas import apresentar_condicoes_declaradas
from mediad_planner.presentation.jornada import apresentar_jornada
from mediad_planner.presentation.revisao_briefing import apresentar_revisao_briefing
if "ambiente" not in st.session_state:
    ambiente, campanha, publico = _com_publico()
    resumo = ambiente.briefings.abrir_briefing(campanha)
    for indice, praca in enumerate(resumo.pracas):
        ambiente.briefings.salvar_prioridade(campanha, SalvarPrioridadeEntrada(
            "PRACA", praca.id_praca, 5, None, "Justificado" if indice == 0 else None,
        ))
    resumo = ambiente.briefings.adicionar_jornada(campanha, _jornada(publico))
    for categoria in ("CONSIDERACAO", "DECISAO"):
        ambiente.briefings.adicionar_etapa_jornada(campanha, resumo.jornadas[0].id_jornada,
            _etapa(publico, categoria=categoria, ordem=None))
    st.session_state.ambiente, st.session_state.campanha = ambiente, campanha
ambiente, campanha = st.session_state.ambiente, st.session_state.campanha
resumo = ambiente.briefings.abrir_briefing(campanha)
tela = st.radio("Tela", ("Condições", "Jornada", "Revisão"))
if tela == "Condições":
    apresentar_condicoes_declaradas(ambiente.briefings, campanha, resumo)
elif tela == "Jornada":
    apresentar_jornada(ambiente.briefings, campanha, resumo)
else:
    apresentar_revisao_briefing(resumo)
'''


@pytest.mark.parametrize("tela,trechos", (
    ("Condições", ("mesmo valor", "prioridade máxima sem justificativa")),
    ("Jornada", ("sem ordenação explícita",)),
))
def test_tela_e_revisao_exibem_mesmos_diagnosticos_sem_duplicar(tela, trechos):
    app = AppTest.from_string(APP).run()
    app.radio[0].set_value(tela).run()
    assert not app.exception
    locais = [item.value for item in app.warning if any(trecho in item.value for trecho in trechos)]
    assert len(locais) == len(trechos)
    app.radio[0].set_value("Revisão").run()
    assert not app.exception
    revisao = [item.value for item in app.warning if any(trecho in item.value for trecho in trechos)]
    assert revisao == locais
