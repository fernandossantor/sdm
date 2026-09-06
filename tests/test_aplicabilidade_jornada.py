from dataclasses import asdict, replace
from datetime import timedelta
from uuid import UUID, uuid4

import pytest

from mediad_planner.application.dto.briefing import ContextoAcessoBriefings
from mediad_planner.application.dto.jornada import DefinirAplicabilidadeJornadaEntrada
from mediad_planner.application.use_cases.jornada import DefinirAplicabilidadeJornada
from mediad_planner.domain.briefing.enums import EstadoBriefing
from mediad_planner.domain.briefing.praca_universo import (
    CriterioSegmentacao, EstruturaTerritorialPopulacional, PublicoDeclarado, SegmentoDeclarado,
)
from mediad_planner.domain.common.enums import PapelAcesso
from mediad_planner.infrastructure.repositories.briefings_em_memoria import RepositorioBriefingsEmMemoria
from test_briefing_dominio import briefing, AGORA
from test_jornada import _jornada
from test_praca_universo_dominio import _praca, _universo
from test_publicos import _preparar, _entrada


def _dominio():
    praca, universo = _praca(), _universo()
    segmento = SegmentoDeclarado(
        UUID(int=71), universo.id_universo, (praca.id_praca,),
        (CriterioSegmentacao.DEMOGRAFICA,), "Segmento", None, None, None,
    )
    publico = PublicoDeclarado(UUID(int=72), "Público", (segmento.id_segmento,), (praca.id_praca,), None, None, None, None, None)
    return replace(briefing(), estrutura_territorial_populacional=EstruturaTerritorialPopulacional(
        (praca,), (universo,), (CriterioSegmentacao.DEMOGRAFICA,), (segmento,), (publico,),
    ))


def _com_dois_publicos():
    ambiente, campanha, segmentos, pracas = _preparar()
    for indice in range(2):
        resumo = ambiente.briefings.adicionar_publico(campanha, _entrada(
            (segmentos[indice],), (pracas[indice],), nome=f"Público {indice + 1}",
        ))
    return ambiente, campanha, resumo.publicos


def test_tres_estados_preservam_contexto_e_atualizam_metadados():
    inicial = _dominio()
    id_publico = inicial.estrutura_territorial_populacional.publicos[0].id_publico
    assert inicial.estrutura_territorial_populacional.publicos[0].jornada_aplicavel is None
    atual = inicial
    for indice, aplicavel in enumerate((False, True, None), 1):
        atual = atual.definir_aplicabilidade_jornada(id_publico, aplicavel, UUID(int=80), AGORA + timedelta(seconds=indice))
        assert atual.estrutura_territorial_populacional.publicos[0].jornada_aplicavel is aplicavel
        assert atual.estado is EstadoBriefing.EM_PREENCHIMENTO
        assert atual.atualizado_por == UUID(int=80)
        assert atual.atualizado_em == AGORA + timedelta(seconds=indice)
        assert atual.contexto_herdado == inicial.contexto_herdado
        assert atual.numero_versao == inicial.numero_versao
    assert atual.estrutura_territorial_populacional == inicial.estrutura_territorial_populacional
    assert inicial.estado is EstadoBriefing.RASCUNHO


@pytest.mark.parametrize("valor", (0, 1, "false", "true", ""))
def test_rejeita_valores_ambiguos(valor):
    inicial = _dominio()
    with pytest.raises(TypeError, match="booleano ou None"):
        inicial.definir_aplicabilidade_jornada(UUID(int=72), valor, UUID(int=80), AGORA)


@pytest.mark.parametrize("estado", (EstadoBriefing.EM_REVISAO, EstadoBriefing.CONCLUIDO, EstadoBriefing.SUBSTITUIDO))
def test_preserva_estados_nao_editaveis(estado):
    inicial = replace(_dominio(), estado=estado)
    with pytest.raises(ValueError, match="não permite alteração"):
        inicial.definir_aplicabilidade_jornada(UUID(int=72), False, UUID(int=80), AGORA)


def test_valida_publico_autoria_e_data():
    inicial = _dominio()
    with pytest.raises(LookupError, match="Público"):
        inicial.definir_aplicabilidade_jornada(uuid4(), True, UUID(int=80), AGORA)
    with pytest.raises(TypeError, match="UUID"):
        inicial.definir_aplicabilidade_jornada(UUID(int=72), True, "autor", AGORA)
    with pytest.raises(ValueError, match="regredir"):
        inicial.definir_aplicabilidade_jornada(UUID(int=72), True, UUID(int=80), AGORA - timedelta(seconds=1))
    with pytest.raises(ValueError, match="fuso"):
        inicial.definir_aplicabilidade_jornada(UUID(int=72), True, UUID(int=80), AGORA.replace(tzinfo=None))


def test_aplicabilidade_por_publico_recalcula_revisao_e_preserva_edicao():
    ambiente, campanha, publicos = _com_dois_publicos()
    primeiro, segundo = publicos
    original = ambiente.briefings.abrir_briefing(campanha)
    nao_aplicavel = ambiente.briefings.definir_aplicabilidade_jornada(campanha, DefinirAplicabilidadeJornadaEntrada(primeiro.id_publico, False))
    assert nao_aplicavel.publicos[0].jornada_aplicavel is False
    assert nao_aplicavel.publicos[1] == segundo
    assert nao_aplicavel.apontamentos_revisao == tuple(
        item for item in original.apontamentos_revisao if not (item.subetapa == "Jornada" and item.id_entidade == primeiro.id_publico)
    )
    editado = ambiente.briefings.editar_publico(campanha, primeiro.id_publico, _entrada(
        primeiro.ids_segmentos_origem, primeiro.ids_pracas, nome="Público renomeado",
    ))
    assert editado.publicos[0].jornada_aplicavel is False
    assert editado.publicos[0].nome == "Público renomeado"
    assert ambiente.briefings.abrir_briefing(campanha) == editado
    aplicavel = ambiente.briefings.definir_aplicabilidade_jornada(campanha, DefinirAplicabilidadeJornadaEntrada(primeiro.id_publico, True))
    assert any("declarada aplicável" in item.mensagem and item.id_entidade == primeiro.id_publico for item in aplicavel.apontamentos_revisao)
    retirada = ambiente.briefings.definir_aplicabilidade_jornada(campanha, DefinirAplicabilidadeJornadaEntrada(primeiro.id_publico, None))
    assert retirada.publicos[0].jornada_aplicavel is None
    assert any("verificar se" in item.mensagem and item.id_entidade == primeiro.id_publico for item in retirada.apontamentos_revisao)


def test_conflitos_na_criacao_edicao_e_declaracao_preservam_jornadas_compartilhadas():
    ambiente, campanha, publicos = _com_dois_publicos()
    primeiro, segundo = publicos
    ambiente.briefings.definir_aplicabilidade_jornada(campanha, DefinirAplicabilidadeJornadaEntrada(segundo.id_publico, False))
    com_jornada = ambiente.briefings.adicionar_jornada(campanha, _jornada(primeiro.id_publico))
    compartilhada = replace(_jornada(primeiro.id_publico), ids_publicos=(primeiro.id_publico, segundo.id_publico))
    for operacao in (
        lambda: ambiente.briefings.adicionar_jornada(campanha, compartilhada),
        lambda: ambiente.briefings.editar_jornada(campanha, com_jornada.jornadas[0].id_jornada, compartilhada),
        lambda: ambiente.briefings.definir_aplicabilidade_jornada(campanha, DefinirAplicabilidadeJornadaEntrada(primeiro.id_publico, False)),
    ):
        with pytest.raises(ValueError, match="não aplicável"):
            operacao()
        assert ambiente.briefings.abrir_briefing(campanha) == com_jornada
    ambiente.briefings.definir_aplicabilidade_jornada(campanha, DefinirAplicabilidadeJornadaEntrada(segundo.id_publico, True))
    vinculada = ambiente.briefings.editar_jornada(campanha, com_jornada.jornadas[0].id_jornada, compartilhada)
    assert vinculada.jornadas[0].ids_publicos == (primeiro.id_publico, segundo.id_publico)
    removida = ambiente.briefings.remover_jornada(campanha, vinculada.jornadas[0].id_jornada)
    assert removida.publicos[0].jornada_aplicavel is None
    assert removida.publicos[1].jornada_aplicavel is True
    assert any("declarada aplicável" in item.mensagem and item.id_entidade == segundo.id_publico for item in removida.apontamentos_revisao)


def test_remover_publico_nao_deixa_declaracao_orfa():
    ambiente, campanha, publicos = _com_dois_publicos()
    primeiro, segundo = publicos
    ambiente.briefings.definir_aplicabilidade_jornada(campanha, DefinirAplicabilidadeJornadaEntrada(primeiro.id_publico, False))
    removido = ambiente.briefings.remover_publico(campanha, primeiro.id_publico)
    assert removido.publicos == (segundo,)
    assert not any(item.id_entidade == primeiro.id_publico for item in removido.apontamentos_revisao)


@pytest.mark.parametrize("papel", tuple(PapelAcesso))
def test_permissoes_de_edicao(papel):
    original = _dominio()
    repositorio = RepositorioBriefingsEmMemoria()
    repositorio.salvar(original)
    caso = DefinirAplicabilidadeJornada(repositorio, ContextoAcessoBriefings(UUID(int=80), original.id_espaco_trabalho, papel), lambda: AGORA)
    entrada = DefinirAplicabilidadeJornadaEntrada(UUID(int=72), False)
    if papel in (PapelAcesso.EDITOR, PapelAcesso.PROPRIETARIO):
        assert caso.executar(original.id_campanha, entrada).publicos[0].jornada_aplicavel is False
    else:
        with pytest.raises(PermissionError):
            caso.executar(original.id_campanha, entrada)
        assert repositorio.obter_por_campanha(original.id_espaco_trabalho, original.id_campanha) == original


@pytest.mark.parametrize("alvo", ("espaco", "campanha", "publico"))
def test_isolamento_dos_vinculos(alvo):
    original = _dominio()
    repositorio = RepositorioBriefingsEmMemoria()
    repositorio.salvar(original)
    caso = DefinirAplicabilidadeJornada(repositorio, ContextoAcessoBriefings(
        UUID(int=80), uuid4() if alvo == "espaco" else original.id_espaco_trabalho, PapelAcesso.EDITOR,
    ), lambda: AGORA)
    with pytest.raises(LookupError):
        caso.executar(
            uuid4() if alvo == "campanha" else original.id_campanha,
            DefinirAplicabilidadeJornadaEntrada(uuid4() if alvo == "publico" else UUID(int=72), False),
        )
    assert asdict(repositorio.obter_por_campanha(original.id_espaco_trabalho, original.id_campanha)) == asdict(original)
