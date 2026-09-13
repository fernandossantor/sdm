from dataclasses import asdict, replace
from uuid import UUID

import pytest
from streamlit.testing.v1 import AppTest

from mediad_planner.application.dto.briefing import ContextoAcessoBriefings
from mediad_planner.application.dto.objetivos_declarados import EditarPrioridadeObjetivoEntrada
from mediad_planner.application.use_cases.objetivos_declarados import EditarPrioridadeObjetivo
from mediad_planner.domain.briefing.enums import EstadoBriefing
from mediad_planner.domain.common.enums import PapelAcesso
from mediad_planner.infrastructure.repositories.briefings_em_memoria import RepositorioBriefingsEmMemoria
from test_briefing_dominio import AGORA
from test_vinculos_objetivos import _dominio_objetivos, _objetivo, AUTOR, PUBLICO, PRACA
from test_frontoffice_vinculos_objetivos import APP, _resumo


@pytest.mark.parametrize('id_objetivo', (UUID(int=1), UUID(int=10)))
@pytest.mark.parametrize('prioridade', range(1, 6))
def test_edicao_preserva_identidade_vinculos_demais_campos_e_original(id_objetivo, prioridade):
    original = _dominio_objetivos().definir_vinculos_objetivo(id_objetivo, (PUBLICO,), (PRACA,), AUTOR, AGORA)
    antes = asdict(original)
    atualizado = original.editar_prioridade_objetivo(id_objetivo, prioridade, 2, ' Motivo ', AUTOR, AGORA)
    assert _objetivo(atualizado, id_objetivo) == replace(_objetivo(original, id_objetivo),
        prioridade_declarada=prioridade, intensidade_declarada=2, justificativa='Motivo')
    assert atualizado.atualizado_por == AUTOR
    assert atualizado.atualizado_em == AGORA
    assert atualizado.estado is EstadoBriefing.EM_PREENCHIMENTO
    assert replace(atualizado, objetivos_declarados=original.objetivos_declarados,
                   estado=original.estado, atualizado_por=original.atualizado_por,
                   atualizado_em=original.atualizado_em) == original
    outro = UUID(int=10) if id_objetivo == UUID(int=1) else UUID(int=1)
    assert _objetivo(atualizado, outro) == _objetivo(original, outro)
    assert asdict(original) == antes
    limpo = atualizado.editar_prioridade_objetivo(id_objetivo, prioridade, 2, ' ', AUTOR, AGORA)
    assert _objetivo(limpo, id_objetivo).justificativa is None


@pytest.mark.parametrize('campo', ('prioridade_declarada', 'intensidade_declarada'))
@pytest.mark.parametrize('valor', (0, 6, True, 3.5, '4', None))
def test_valores_invalidos_nao_alteram_repositorio(campo, valor):
    original, repositorio, caso = _caso()
    entrada = replace(EditarPrioridadeObjetivoEntrada(UUID(int=1), 4, 3, None), **{campo: valor})
    with pytest.raises((TypeError, ValueError)):
        caso.executar(original.id_campanha, entrada)
    assert repositorio.obter_por_campanha(original.id_espaco_trabalho, original.id_campanha) == original


def _caso(papel=PapelAcesso.EDITOR, outro_espaco=False):
    original = _dominio_objetivos()
    repositorio = RepositorioBriefingsEmMemoria()
    repositorio.salvar(original)
    caso = EditarPrioridadeObjetivo(repositorio, ContextoAcessoBriefings(
        AUTOR, UUID(int=999) if outro_espaco else original.id_espaco_trabalho, papel), lambda: AGORA)
    return original, repositorio, caso


@pytest.mark.parametrize('papel', tuple(PapelAcesso))
def test_permissoes(papel):
    original, repositorio, caso = _caso(papel)
    entrada = EditarPrioridadeObjetivoEntrada(UUID(int=1), 4, 3, None)
    if papel in (PapelAcesso.EDITOR, PapelAcesso.PROPRIETARIO):
        assert caso.executar(original.id_campanha, entrada).objetivos_marketing[0].prioridade_declarada == 4
    else:
        with pytest.raises(PermissionError):
            caso.executar(original.id_campanha, entrada)
        assert repositorio.obter_por_campanha(original.id_espaco_trabalho, original.id_campanha) == original


@pytest.mark.parametrize('estado', (EstadoBriefing.EM_REVISAO, EstadoBriefing.CONCLUIDO, EstadoBriefing.SUBSTITUIDO))
def test_estados_nao_editaveis(estado):
    original = replace(_dominio_objetivos(), estado=estado)
    with pytest.raises(ValueError, match='não permite alteração'):
        original.editar_prioridade_objetivo(UUID(int=1), 4, 3, None, AUTOR, AGORA)



@pytest.mark.parametrize('alvo', ('espaco', 'campanha', 'objetivo', 'tipo_id'))
def test_isolamento_e_identificacao(alvo):
    original, repositorio, caso = _caso(outro_espaco=alvo == 'espaco')
    entrada = EditarPrioridadeObjetivoEntrada(
        '1' if alvo == 'tipo_id' else UUID(int=999) if alvo == 'objetivo' else UUID(int=1), 4, 3, None)
    with pytest.raises(TypeError if alvo == 'tipo_id' else LookupError):
        caso.executar(UUID(int=999) if alvo == 'campanha' else original.id_campanha, entrada)
    assert repositorio.obter_por_campanha(original.id_espaco_trabalho, original.id_campanha) == original


@pytest.mark.parametrize('grupo', ('objetivos_marketing', 'objetivos_comunicacao'))
def test_interface_edita_reabre_e_recalcula_alertas_sem_trocar_objetivo(grupo):
    app = AppTest.from_string(APP).run()
    original = _resumo(app)
    objetivo = getattr(original, grupo)[0]
    chave = f'prioridade_objetivo_{app.session_state.campanha}_{objetivo.id_objetivo}'
    for prioridade in (3, 5):
        app.selectbox(f'{chave}_prioridade').set_value(f'{prioridade} — ' + ('Média' if prioridade == 3 else 'Muito alta'))
        app.selectbox(f'{chave}_intensidade').set_value('2 — Baixa')
        app.text_area(f'{chave}_justificativa').set_value('Motivo editado')
        next(b for b in app.button if b.label == 'Salvar prioridade do Objetivo' and str(objetivo.id_objetivo) in b.key).click().run()
        app.run()
        assert not app.exception
        assert not app.error
        salvo = _resumo(app)
        assert getattr(salvo, grupo)[0] == replace(objetivo, prioridade_declarada=prioridade,
            intensidade_declarada=2, justificativa='Motivo editado')
        avisos = [a for a in salvo.apontamentos_revisao if a.id_entidade == objetivo.id_objetivo and 'objetivo prioritário' in a.mensagem]
        assert len(avisos) == (2 if prioridade == 5 else 0)
        assert all(any(a.mensagem == w.value for w in app.warning) for a in avisos)
        app.radio[0].set_value('Públicos').run()
        app.radio[0].set_value('Objetivos').run()
        assert not app.exception
        assert app.text_area(f'{chave}_justificativa').value == 'Motivo editado'
        assert app.selectbox(f'{chave}_prioridade').value.startswith(str(prioridade))


def test_edicao_nao_submetida_nao_altera_declaracoes():
    app = AppTest.from_string(APP).run()
    original = _resumo(app)
    objetivo = original.objetivos_marketing[0]
    chave = f'prioridade_objetivo_{app.session_state.campanha}_{objetivo.id_objetivo}'
    app.text_area(f'{chave}_justificativa').set_value('Não salvo')
    app.radio[0].set_value('Públicos').run()
    assert _resumo(app) == original


@pytest.mark.parametrize('grupo', ('marketing', 'comunicacao'))
def test_justificar_e_reduzir_prioridade_recalcula_multiplas_maximas(grupo):
    from test_vinculos_objetivos import _ambiente_vinculos
    from test_casos_uso_objetivos_declarados import entrada_marketing, entrada_comunicacao
    ambiente, campanha = _ambiente_vinculos()
    entrada = entrada_marketing() if grupo == 'marketing' else entrada_comunicacao(())
    entrada = replace(entrada, codigo_objetivo=None, objetivo='Outro resultado',
                      prioridade_declarada=5, justificativa=None)
    resumo = getattr(ambiente.briefings, f'adicionar_objetivo_{grupo}')(campanha, entrada)
    primeiro, segundo = getattr(resumo, f'objetivos_{grupo}')
    ambiente.briefings.editar_prioridade_objetivo(campanha,
        EditarPrioridadeObjetivoEntrada(primeiro.id_objetivo, 5, 3, None))
    resumo = ambiente.briefings.abrir_briefing(campanha)
    ids = {primeiro.id_objetivo, segundo.id_objetivo}
    assert {a.id_entidade for a in resumo.apontamentos_revisao
            if a.id_entidade in ids and 'prioridade máxima sem justificativa' in a.mensagem} == ids
    resumo = ambiente.briefings.editar_prioridade_objetivo(campanha,
        EditarPrioridadeObjetivoEntrada(primeiro.id_objetivo, 5, 3, 'Motivo'))
    assert {a.id_entidade for a in resumo.apontamentos_revisao
            if a.id_entidade in ids and 'prioridade máxima sem justificativa' in a.mensagem} == {segundo.id_objetivo}
    resumo = ambiente.briefings.editar_prioridade_objetivo(campanha,
        EditarPrioridadeObjetivoEntrada(segundo.id_objetivo, 3, 3, None))
    assert not any(a.id_entidade in ids and 'prioridade máxima sem justificativa' in a.mensagem
                   for a in resumo.apontamentos_revisao)
    assert ambiente.briefings.abrir_briefing(campanha) == resumo
