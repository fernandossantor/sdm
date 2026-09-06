from dataclasses import asdict, replace
from datetime import timedelta
from uuid import UUID, uuid4

import pytest

from mediad_planner.application.dto.briefing import ContextoAcessoBriefings
from mediad_planner.application.dto.condicoes_declaradas import (
    DefinirInexistenciaRestricoesEntrada, SalvarRestricaoEntrada,
)
from mediad_planner.application.use_cases.condicoes_declaradas import GerenciarCondicoesDeclaradas
from mediad_planner.domain.briefing.condicoes_declaradas import CategoriaRestricao, RestricaoDeclarada
from mediad_planner.domain.briefing.enums import EstadoBriefing
from mediad_planner.domain.common.enums import PapelAcesso
from mediad_planner.infrastructure.repositories.briefings_em_memoria import RepositorioBriefingsEmMemoria
from test_briefing_dominio import briefing, AGORA
from test_periodo_verba import _preparar


def _restricao():
    return RestricaoDeclarada(
        UUID(int=81), CategoriaRestricao.OPERACIONAL, "Prazo de produção",
        "Campanha", 3, 3, None, None, None, None,
    )


def test_declaracao_e_retirada_preservam_contexto_e_atualizam_autoria():
    inicial = briefing()
    assert inicial.restricoes_inexistentes_declaradas is False
    declarado = inicial.definir_inexistencia_restricoes(True, UUID(int=80), AGORA + timedelta(seconds=1))
    assert declarado.restricoes_inexistentes_declaradas is True
    assert declarado.estado is EstadoBriefing.EM_PREENCHIMENTO
    assert declarado.atualizado_por == UUID(int=80)
    assert declarado.atualizado_em == AGORA + timedelta(seconds=1)
    retirado = declarado.definir_inexistencia_restricoes(False, UUID(int=82), AGORA + timedelta(seconds=2))
    assert retirado.restricoes_inexistentes_declaradas is False
    assert retirado.estado is EstadoBriefing.EM_PREENCHIMENTO
    alterados = {"estado", "atualizado_por", "atualizado_em", "restricoes_inexistentes_declaradas"}
    for campo, valor in asdict(inicial).items():
        if campo not in alterados:
            assert asdict(declarado)[campo] == valor
            assert asdict(retirado)[campo] == valor
    assert inicial.restricoes_inexistentes_declaradas is False


def test_nao_sobrescreve_declaracao_ou_registros_em_conflito():
    inicial = briefing()
    declarado = inicial.definir_inexistencia_restricoes(True, UUID(int=80), AGORA)
    with pytest.raises(ValueError, match="coexistir"):
        declarado.salvar_restricao(_restricao(), False, UUID(int=80), AGORA)
    assert declarado.restricoes_inexistentes_declaradas is True
    assert declarado.restricoes == ()
    com_restricao = inicial.salvar_restricao(_restricao(), False, UUID(int=80), AGORA)
    with pytest.raises(ValueError, match="coexistir"):
        com_restricao.definir_inexistencia_restricoes(True, UUID(int=80), AGORA)
    assert com_restricao.restricoes == (_restricao(),)
    assert com_restricao.restricoes_inexistentes_declaradas is False
    with pytest.raises(ValueError, match="coexistir"):
        replace(com_restricao, restricoes_inexistentes_declaradas=True)
    vazio = com_restricao.remover_restricao(_restricao().id_restricao, UUID(int=80), AGORA)
    assert vazio.restricoes_inexistentes_declaradas is False


@pytest.mark.parametrize("valor", (None, 0, 1, "false", "true"))
def test_nao_converte_valores_ambiguos_em_declaracao(valor):
    with pytest.raises(TypeError, match="booleano"):
        briefing().definir_inexistencia_restricoes(valor, UUID(int=80), AGORA)


@pytest.mark.parametrize("estado", (EstadoBriefing.EM_REVISAO, EstadoBriefing.CONCLUIDO, EstadoBriefing.SUBSTITUIDO))
@pytest.mark.parametrize("declarada", (True, False))
def test_declaracao_respeita_estado_editavel(estado, declarada):
    fechado = replace(briefing(), estado=estado, restricoes_inexistentes_declaradas=not declarada)
    with pytest.raises(ValueError, match="não permite alteração"):
        fechado.definir_inexistencia_restricoes(declarada, UUID(int=80), AGORA)


def test_declaracao_respeita_relogio_e_identidade_do_autor():
    inicial = briefing()
    with pytest.raises(ValueError, match="regredir"):
        inicial.definir_inexistencia_restricoes(True, UUID(int=80), AGORA - timedelta(seconds=1))
    with pytest.raises(ValueError, match="fuso"):
        inicial.definir_inexistencia_restricoes(True, UUID(int=80), AGORA.replace(tzinfo=None))
    with pytest.raises(TypeError, match="UUID"):
        inicial.definir_inexistencia_restricoes(True, "autor", AGORA)


def test_aplicacao_salva_reabre_e_recalcula_pendencia():
    ambiente, campanha = _preparar()
    inicial = ambiente.briefings.abrir_briefing(campanha)
    pendencias = tuple(item for item in inicial.apontamentos_revisao if "Nenhuma restrição registrada" not in item.mensagem)
    declarado = ambiente.briefings.definir_inexistencia_restricoes(campanha, DefinirInexistenciaRestricoesEntrada(True))
    assert declarado.restricoes_inexistentes_declaradas is True
    assert declarado.apontamentos_revisao == pendencias
    assert ambiente.briefings.abrir_briefing(campanha) == declarado
    with pytest.raises(ValueError, match="coexistir"):
        ambiente.briefings.salvar_restricao(campanha, SalvarRestricaoEntrada(
            "OPERACIONAL", "Prazo", "Campanha", 3, 3, None, None, None, None,
        ))
    assert ambiente.briefings.abrir_briefing(campanha) == declarado
    retirado = ambiente.briefings.definir_inexistencia_restricoes(campanha, DefinirInexistenciaRestricoesEntrada(False))
    assert retirado.apontamentos_revisao == inicial.apontamentos_revisao
    salvo = ambiente.briefings.salvar_restricao(campanha, SalvarRestricaoEntrada(
        "OPERACIONAL", "Prazo", "Campanha", 3, 3, None, None, None, None,
    ))
    with pytest.raises(ValueError, match="coexistir"):
        ambiente.briefings.definir_inexistencia_restricoes(campanha, DefinirInexistenciaRestricoesEntrada(True))
    assert ambiente.briefings.abrir_briefing(campanha) == salvo
    removido = ambiente.briefings.remover_restricao(campanha, salvo.restricoes[0].id_restricao)
    assert removido.restricoes_inexistentes_declaradas is False
    assert removido.apontamentos_revisao == inicial.apontamentos_revisao


@pytest.mark.parametrize("papel", tuple(PapelAcesso))
@pytest.mark.parametrize("declarada", (True, False))
def test_caso_uso_respeita_papel_e_preserva_dados_quando_negado(papel, declarada):
    original = replace(briefing(), restricoes_inexistentes_declaradas=not declarada)
    repositorio = RepositorioBriefingsEmMemoria()
    repositorio.salvar(original)
    caso = GerenciarCondicoesDeclaradas(
        repositorio, ContextoAcessoBriefings(UUID(int=80), original.id_espaco_trabalho, papel),
        lambda: AGORA, uuid4,
    )
    if papel in (PapelAcesso.PROPRIETARIO, PapelAcesso.EDITOR):
        resumo = caso.definir_inexistencia_restricoes(original.id_campanha, DefinirInexistenciaRestricoesEntrada(declarada))
        assert resumo.restricoes_inexistentes_declaradas is declarada
    else:
        with pytest.raises(PermissionError):
            caso.definir_inexistencia_restricoes(original.id_campanha, DefinirInexistenciaRestricoesEntrada(declarada))
        assert repositorio.obter_por_campanha(original.id_espaco_trabalho, original.id_campanha) == original


@pytest.mark.parametrize("outro_espaco", (True, False))
def test_nao_altera_briefing_de_outro_espaco_ou_campanha(outro_espaco):
    original = briefing()
    repositorio = RepositorioBriefingsEmMemoria()
    repositorio.salvar(original)
    contexto = ContextoAcessoBriefings(
        UUID(int=80), uuid4() if outro_espaco else original.id_espaco_trabalho, PapelAcesso.EDITOR,
    )
    caso = GerenciarCondicoesDeclaradas(repositorio, contexto, lambda: AGORA, uuid4)
    with pytest.raises(LookupError):
        caso.definir_inexistencia_restricoes(
            original.id_campanha if outro_espaco else uuid4(), DefinirInexistenciaRestricoesEntrada(True),
        )
    assert repositorio.obter_por_campanha(original.id_espaco_trabalho, original.id_campanha) == original
