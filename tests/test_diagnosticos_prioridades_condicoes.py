from dataclasses import asdict, replace
from uuid import UUID

import pytest
from streamlit.testing.v1 import AppTest

from mediad_planner.application.dto.condicoes_declaradas import SalvarPretensaoEntrada, SalvarRestricaoEntrada
from mediad_planner.domain.briefing.condicoes_declaradas import (
    CategoriaPretensao, CategoriaRestricao, PretensaoDeclarada, RestricaoDeclarada,
)
from mediad_planner.domain.briefing.revisao import avaliar_briefing
from test_aplicabilidade_jornada import _dominio
from test_publicos import _preparar


def _item(grupo, indice, prioridade, justificativa):
    identificador = UUID(int=900 + indice)
    if grupo == 'restricoes':
        return RestricaoDeclarada(identificador, CategoriaRestricao.OPERACIONAL,
            f'Condição {indice}', 'Campanha', 3, prioridade, None, justificativa, None, None)
    return PretensaoDeclarada(identificador, CategoriaPretensao.OUTRA,
        f'Condição {indice}', prioridade, 3, None, None, None, None, None, justificativa)


def _alertas(briefing):
    return [a for a in avaliar_briefing(briefing) if a.referencia_normativa.endswith('13.3')]


@pytest.mark.parametrize('grupo', ('restricoes', 'pretensoes'))
@pytest.mark.parametrize('valores,justificativas,iguais,lacunas', (
    ((), (), False, ()),
    ((5,), (None,), False, ()),
    ((1, 2, 3, 4, 5), (None,) * 5, False, ()),
    ((1, 1), (None, None), True, ()),
    ((4, 4), (None, None), True, ()),
    ((5, 5), (None, None), True, (0, 1)),
    ((5, 5), ('Motivo', None), True, (1,)),
    ((5, 5), ('Motivo', 'Outro'), True, ()),
    ((5, 5, 3), (' ', 'Motivo', None), False, (0,)),
))
def test_avaliacao_por_conjunto_preserva_declaracoes(grupo, valores, justificativas, iguais, lacunas):
    original = replace(_dominio(), **{grupo: tuple(
        _item(grupo, i, valor, justificativas[i]) for i, valor in enumerate(valores)
    )})
    antes = asdict(original)
    alertas = _alertas(original)
    assert sum('mesmo valor' in a.mensagem for a in alertas) == int(iguais)
    assert {a.id_entidade for a in alertas if 'sem justificativa' in a.mensagem} == {
        UUID(int=900 + i) for i in lacunas
    }
    assert all(a.subetapa == 'Prioridades, restrições e pretensões' for a in alertas)
    assert asdict(original) == antes


def test_nao_combina_restricao_e_pretensao_e_usa_rotulo_canonico():
    original = replace(_dominio(), restricoes=(_item('restricoes', 0, 5, None),),
        pretensoes=(_item('pretensoes', 1, 5, None),))
    assert not _alertas(original)
    pretensao = replace(original.pretensoes[0], categoria=CategoriaPretensao.APOIAR_VENDAS,
                       descricao_controlada=None)
    original = replace(original, pretensoes=(pretensao, _item('pretensoes', 2, 5, None)))
    assert any('Apoiar vendas' in a.mensagem for a in _alertas(original))


def _entrada(grupo, prioridade=5, justificativa=None):
    if grupo == 'restricoes':
        return SalvarRestricaoEntrada('OPERACIONAL', 'Condição', 'Campanha', 3,
                                     prioridade, None, justificativa, None, None)
    return SalvarPretensaoEntrada('APOIAR_VENDAS', None, prioridade, 3,
                                 None, None, None, None, None, justificativa)


def _preparar_condicoes(grupo):
    ambiente, campanha, _, _ = _preparar()
    salvar = getattr(ambiente.briefings, 'salvar_restricao' if grupo == 'restricoes' else 'salvar_pretensao')
    for _ in range(2):
        salvar(campanha, _entrada(grupo))
    return ambiente, campanha


@pytest.mark.parametrize('grupo,singular', (('restricoes', 'restricao'), ('pretensoes', 'pretensao')))
def test_recalcula_apos_justificar_alterar_prioridade_remover_e_reabrir(grupo, singular):
    ambiente, campanha = _preparar_condicoes(grupo)
    salvar = getattr(ambiente.briefings, f'salvar_{singular}')
    resumo = ambiente.briefings.abrir_briefing(campanha)
    primeiro, segundo = getattr(resumo, grupo)
    ids = [getattr(item, f'id_{singular}') for item in (primeiro, segundo)]
    assert sum('prioridade máxima sem justificativa' in a.mensagem for a in resumo.apontamentos_revisao) == 2
    resumo = salvar(campanha, _entrada(grupo, justificativa='Motivo'), ids[0])
    assert [a.id_entidade for a in resumo.apontamentos_revisao if 'prioridade máxima sem justificativa' in a.mensagem] == [ids[1]]
    resumo = salvar(campanha, _entrada(grupo, prioridade=4), ids[1])
    assert not any(a.referencia_normativa.endswith('13.3') for a in resumo.apontamentos_revisao)
    getattr(ambiente.briefings, f'remover_{singular}')(campanha, ids[1])
    resumo = ambiente.briefings.abrir_briefing(campanha)
    assert len(getattr(resumo, grupo)) == 1
    assert not any(a.referencia_normativa.endswith('13.3') for a in resumo.apontamentos_revisao)


APP = '''
import streamlit as st
from test_diagnosticos_prioridades_condicoes import _preparar_condicoes
from mediad_planner.presentation.condicoes_declaradas import apresentar_condicoes_declaradas
from mediad_planner.presentation.revisao_briefing import apresentar_revisao_briefing
if 'ambiente' not in st.session_state:
    st.session_state.ambiente, st.session_state.campanha = _preparar_condicoes(GRUPO)
ambiente, campanha = st.session_state.ambiente, st.session_state.campanha
resumo = ambiente.briefings.abrir_briefing(campanha)
if st.radio('Tela', ('Condições', 'Revisão')) == 'Condições':
    apresentar_condicoes_declaradas(ambiente.briefings, campanha, resumo)
else:
    apresentar_revisao_briefing(resumo)
'''


@pytest.mark.parametrize('grupo,rotulo,botao', (
    ('restricoes', 'Restrições', 'Remover Restrição'),
    ('pretensoes', 'Pretensões', 'Remover Pretensão'),
))
def test_interface_revisao_e_remocao(grupo, rotulo, botao):
    app = AppTest.from_string(APP.replace('GRUPO', repr(grupo))).run()
    assert not app.exception
    locais = [a.value for a in app.warning if a.value.startswith(rotulo)]
    assert len(locais) == 3
    app.radio[0].set_value('Revisão').run()
    assert not app.exception
    assert [a.value for a in app.warning if a.value.startswith(rotulo)] == locais
    app.radio[0].set_value('Condições').run()
    next(b for b in app.button if b.label == botao).click().run()
    app.run()
    assert not app.exception
    assert not any(a.value.startswith(rotulo) for a in app.warning)
    app.radio[0].set_value('Revisão').run()
    assert not app.exception
    assert not any(a.value.startswith(rotulo) for a in app.warning)
