from dataclasses import asdict, replace
from uuid import UUID

import pytest
from streamlit.testing.v1 import AppTest

from mediad_planner.application.dto.briefing import ContextoAcessoBriefings
from mediad_planner.application.dto.objetivos_declarados import DefinirRelacoesMarketingEntrada
from mediad_planner.application.use_cases.objetivos_declarados import DefinirRelacoesMarketing
from mediad_planner.domain.briefing.enums import EstadoBriefing
from mediad_planner.domain.common.enums import PapelAcesso
from mediad_planner.infrastructure.repositories.briefings_em_memoria import RepositorioBriefingsEmMemoria
from test_briefing_dominio import AGORA
from test_vinculos_objetivos import _dominio_objetivos, _ambiente_vinculos, AUTOR
from test_frontoffice_vinculos_objetivos import APP, _resumo
from test_casos_uso_objetivos_declarados import entrada_marketing


def test_dominio_preserva_demais_campos_e_nao_muta_original():
    original = _dominio_objetivos()
    antes = asdict(original)
    retirado = original.definir_relacoes_marketing(UUID(int=10), (), AUTOR, AGORA)
    assert retirado.objetivos_declarados.marketing == original.objetivos_declarados.marketing
    assert retirado.objetivos_declarados.comunicacao == (replace(
        original.objetivos_declarados.comunicacao[0], ids_objetivos_marketing_relacionados=()),)
    assert retirado.estado is EstadoBriefing.EM_PREENCHIMENTO
    assert retirado.atualizado_por == AUTOR
    assert retirado.atualizado_em == AGORA
    restaurado = retirado.definir_relacoes_marketing(UUID(int=10), (UUID(int=1),), AUTOR, AGORA)
    assert restaurado.objetivos_declarados == original.objetivos_declarados
    assert asdict(original) == antes


@pytest.mark.parametrize('estado', (EstadoBriefing.EM_REVISAO, EstadoBriefing.CONCLUIDO, EstadoBriefing.SUBSTITUIDO))
def test_estado_protegido(estado):
    with pytest.raises(ValueError, match='não permite alteração'):
        replace(_dominio_objetivos(), estado=estado).definir_relacoes_marketing(UUID(int=10), (), AUTOR, AGORA)


@pytest.mark.parametrize('papel', tuple(PapelAcesso))
def test_permissoes(papel):
    original = _dominio_objetivos()
    repo = RepositorioBriefingsEmMemoria()
    repo.salvar(original)
    caso = DefinirRelacoesMarketing(repo, ContextoAcessoBriefings(AUTOR, original.id_espaco_trabalho, papel), lambda: AGORA)
    entrada = DefinirRelacoesMarketingEntrada(UUID(int=10), ())
    if papel in (PapelAcesso.PROPRIETARIO, PapelAcesso.EDITOR):
        assert caso.executar(original.id_campanha, entrada).objetivos_comunicacao[0].ids_objetivos_marketing_relacionados == ()
    else:
        with pytest.raises(PermissionError):
            caso.executar(original.id_campanha, entrada)
        assert repo.obter_por_campanha(original.id_espaco_trabalho, original.id_campanha) == original


@pytest.mark.parametrize('alvo', ('espaco', 'campanha', 'comunicacao', 'marketing', 'tipo_id', 'tipo_relacao', 'duplicata', 'tipo_objetivo'))
def test_rejeicao_preserva_dados(alvo):
    original = _dominio_objetivos()
    repo = RepositorioBriefingsEmMemoria()
    repo.salvar(original)
    caso = DefinirRelacoesMarketing(repo, ContextoAcessoBriefings(AUTOR,
        UUID(int=999) if alvo == 'espaco' else original.id_espaco_trabalho, PapelAcesso.EDITOR), lambda: AGORA)
    ids = {'marketing': (UUID(int=999),), 'tipo_relacao': ('1',),
           'duplicata': (UUID(int=1), UUID(int=1))}.get(alvo, ())
    id_comunicacao = {'comunicacao': UUID(int=999), 'tipo_id': '10', 'tipo_objetivo': UUID(int=1)}.get(alvo, UUID(int=10))
    with pytest.raises((LookupError, TypeError, ValueError)):
        caso.executar(UUID(int=999) if alvo == 'campanha' else original.id_campanha,
                      DefinirRelacoesMarketingEntrada(id_comunicacao, ids))
    assert repo.obter_por_campanha(original.id_espaco_trabalho, original.id_campanha) == original


def test_entrada_nao_compartilha_lista_mutavel():
    ids = [UUID(int=1)]
    entrada = DefinirRelacoesMarketingEntrada(UUID(int=10), ids)
    atualizado = _dominio_objetivos().definir_relacoes_marketing(UUID(int=10), ids, AUTOR, AGORA)
    ids.clear()
    assert entrada.ids_objetivos_marketing == (UUID(int=1),)
    assert atualizado.objetivos_declarados.comunicacao[0].ids_objetivos_marketing_relacionados == (UUID(int=1),)


def test_aplicacao_salva_troca_retira_reabre_e_libera_remocao():
    ambiente, campanha = _ambiente_vinculos()
    resumo = ambiente.briefings.adicionar_objetivo_marketing(campanha,
        replace(entrada_marketing(), codigo_objetivo=None, objetivo='Outro resultado'))
    objetivo = resumo.objetivos_comunicacao[0]
    ids = tuple(o.id_objetivo for o in resumo.objetivos_marketing)
    for relacoes in (ids, ids[1:], ()):
        salvo = ambiente.briefings.definir_relacoes_marketing(campanha,
            DefinirRelacoesMarketingEntrada(objetivo.id_objetivo, relacoes))
        assert salvo.objetivos_comunicacao[0] == replace(objetivo, ids_objetivos_marketing_relacionados=relacoes)
        assert ambiente.briefings.abrir_briefing(campanha) == salvo
        assert any('sem relação explícita' in a.mensagem and a.id_entidade == objetivo.id_objetivo
                   for a in salvo.apontamentos_revisao) == (not relacoes)
    assert len(ambiente.briefings.remover_objetivo_marketing(campanha, ids[0]).objetivos_marketing) == 1


def test_interface_salva_retira_e_reabre():
    app = AppTest.from_string(APP).run()
    original = _resumo(app)
    objetivo = original.objetivos_comunicacao[0]
    chave = f'relacoes_marketing_{app.session_state.campanha}_{objetivo.id_objetivo}'
    for ids in ((), objetivo.ids_objetivos_marketing_relacionados):
        app.multiselect(f'{chave}_objetivos').set_value(list(ids))
        next(b for b in app.button if b.label == 'Salvar relações com Marketing').click().run()
        app.run()
        assert not app.exception
        assert not app.error
        assert _resumo(app).objetivos_comunicacao[0] == replace(objetivo, ids_objetivos_marketing_relacionados=ids)
        app.radio[0].set_value('Públicos').run()
        app.radio[0].set_value('Objetivos').run()
        assert tuple(app.multiselect(f'{chave}_objetivos').value) == ids


def test_interface_nao_salva_sem_submissao():
    app = AppTest.from_string(APP).run()
    original = _resumo(app)
    objetivo = original.objetivos_comunicacao[0]
    chave = f'relacoes_marketing_{app.session_state.campanha}_{objetivo.id_objetivo}'
    app.multiselect(f'{chave}_objetivos').set_value([])
    app.radio[0].set_value('Públicos').run()
    assert _resumo(app) == original


def test_objetivo_de_outra_campanha_nao_pode_ser_relacionado():
    original = _dominio_objetivos()
    outro = replace(original, id_briefing=UUID(int=800), id_campanha=UUID(int=801),
        objetivos_declarados=replace(original.objetivos_declarados,
            marketing=(replace(original.objetivos_declarados.marketing[0], id_objetivo=UUID(int=802)),),
            comunicacao=()))
    repo = RepositorioBriefingsEmMemoria()
    repo.salvar(original)
    repo.salvar(outro)
    caso = DefinirRelacoesMarketing(repo, ContextoAcessoBriefings(AUTOR,
        original.id_espaco_trabalho, PapelAcesso.EDITOR), lambda: AGORA)
    with pytest.raises(ValueError, match='não existe'):
        caso.executar(original.id_campanha,
            DefinirRelacoesMarketingEntrada(UUID(int=10), (UUID(int=802),)))
    assert repo.obter_por_campanha(original.id_espaco_trabalho, original.id_campanha) == original
    assert repo.obter_por_campanha(outro.id_espaco_trabalho, outro.id_campanha) == outro
