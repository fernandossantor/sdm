from dataclasses import fields
from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest

from mediad_planner.application.dto.campanha import (
    CampanhaResumo,
    ContextoAcessoCampanhas,
    CriarCampanhaEntrada,
)
from mediad_planner.application.use_cases.campanhas import (
    CriarCampanha,
    IniciarBriefingCampanha,
    ListarCampanhas,
)
from mediad_planner.domain.common.enums import PapelAcesso
from mediad_planner.infrastructure.repositories.campanhas_em_memoria import (
    RepositorioCampanhasEmMemoria,
)


AGORA = datetime(2026, 7, 10, 15, tzinfo=timezone.utc)


class GeradorDeterministico:
    def __init__(self, inicio: int = 100) -> None:
        self._proximo = inicio

    def __call__(self) -> UUID:
        identificador = UUID(int=self._proximo)
        self._proximo += 1
        return identificador


def contexto(papel: PapelAcesso, espaco: int = 10) -> ContextoAcessoCampanhas:
    return ContextoAcessoCampanhas(UUID(int=1), UUID(int=espaco), papel)


def entrada(
    iniciar_briefing: bool = False,
    nomes_equipe: tuple[str, ...] = (),
) -> CriarCampanhaEntrada:
    return CriarCampanhaEntrada(
        nome="Campanha de Inverno",
        nome_anunciante="Anunciante Á",
        nome_marca="Marca Ê",
        nome_produto_servico="Produto Í",
        nome_planejador_responsavel="Pessoa Ô",
        nomes_equipe=nomes_equipe,
        observacao_inicial="Observação",
        iniciar_briefing=iniciar_briefing,
    )


def criar_caso(
    papel: PapelAcesso,
    repositorio: RepositorioCampanhasEmMemoria | None = None,
    espaco: int = 10,
) -> tuple[CriarCampanha, RepositorioCampanhasEmMemoria]:
    repositorio_usado = repositorio or RepositorioCampanhasEmMemoria()
    caso = CriarCampanha(
        repositorio_usado,
        contexto(papel, espaco),
        lambda: AGORA,
        GeradorDeterministico(inicio=espaco * 100),
    )
    return caso, repositorio_usado


@pytest.mark.parametrize("papel", (PapelAcesso.PROPRIETARIO, PapelAcesso.EDITOR))
def test_proprietario_e_editor_criam_rascunho(papel: PapelAcesso) -> None:
    caso, repositorio = criar_caso(papel)
    resumo = caso.executar(entrada())
    entidade = repositorio.obter(UUID(int=10), resumo.id_campanha)
    assert resumo.codigo == "MP-202607-0001"
    assert resumo.situacao == "RASCUNHO"
    assert resumo.etapa_atual == "ABERTURA"
    assert resumo.criado_em == AGORA
    assert resumo.atualizado_em == AGORA
    assert entidade.criado_por == UUID(int=1)
    assert entidade.atualizado_por == UUID(int=1)


@pytest.mark.parametrize("papel", (PapelAcesso.LEITOR, PapelAcesso.ADMINISTRADOR))
def test_leitor_e_administrador_nao_criam(papel: PapelAcesso) -> None:
    caso, repositorio = criar_caso(papel)
    with pytest.raises(PermissionError):
        caso.executar(entrada())
    assert repositorio.listar(UUID(int=10)) == ()


def test_cria_com_vinculos_coerentes_e_equipe_deduplicada() -> None:
    caso, repositorio = criar_caso(PapelAcesso.EDITOR)
    resumo = caso.executar(entrada(nomes_equipe=(" Ana ", "ana", "", "Bia")))
    campanha = repositorio.obter(UUID(int=10), resumo.id_campanha)
    assert campanha.marca.id_anunciante == campanha.anunciante.id_anunciante
    assert campanha.produto_servico.id_anunciante == campanha.anunciante.id_anunciante
    assert campanha.produto_servico.id_marca == campanha.marca.id_marca
    assert resumo.equipe == ("Ana", "Bia")


def test_cria_sem_equipe_e_pode_iniciar_briefing_imediatamente() -> None:
    caso, _ = criar_caso(PapelAcesso.PROPRIETARIO)
    resumo = caso.executar(entrada(iniciar_briefing=True))
    assert resumo.equipe == ()
    assert resumo.situacao == "EM_ANDAMENTO"
    assert resumo.etapa_atual == "BRIEFING"


def test_inicia_briefing_posteriormente_e_falha_quando_inexistente() -> None:
    criar, repositorio = criar_caso(PapelAcesso.EDITOR)
    resumo = criar.executar(entrada())
    iniciar = IniciarBriefingCampanha(
        repositorio,
        contexto(PapelAcesso.EDITOR),
        lambda: AGORA + timedelta(minutes=1),
    )
    atualizado = iniciar.executar(resumo.id_campanha)
    assert atualizado.situacao == "EM_ANDAMENTO"
    assert atualizado.etapa_atual == "BRIEFING"
    with pytest.raises(LookupError, match="não encontrada"):
        iniciar.executar(UUID(int=999))


@pytest.mark.parametrize("papel", (PapelAcesso.LEITOR, PapelAcesso.ADMINISTRADOR))
def test_leitor_e_administrador_nao_iniciam_briefing(
    papel: PapelAcesso,
) -> None:
    criar, repositorio = criar_caso(PapelAcesso.EDITOR)
    resumo = criar.executar(entrada())
    iniciar = IniciarBriefingCampanha(
        repositorio,
        contexto(papel),
        lambda: AGORA + timedelta(minutes=1),
    )
    with pytest.raises(PermissionError):
        iniciar.executar(resumo.id_campanha)


def test_listagem_isola_espacos_e_leitor_pode_consultar() -> None:
    repositorio = RepositorioCampanhasEmMemoria()
    criar_a, _ = criar_caso(PapelAcesso.EDITOR, repositorio, espaco=10)
    criar_b, _ = criar_caso(PapelAcesso.EDITOR, repositorio, espaco=11)
    resumo_a = criar_a.executar(entrada())
    criar_b.executar(entrada())
    listar = ListarCampanhas(repositorio, contexto(PapelAcesso.LEITOR, 10))
    assert listar.executar() == (resumo_a,)


def test_saida_e_dto_sem_entidade_de_dominio() -> None:
    caso, _ = criar_caso(PapelAcesso.EDITOR)
    resumo = caso.executar(entrada())
    assert isinstance(resumo, CampanhaResumo)
    assert "Campanha" not in {campo.type for campo in fields(CampanhaResumo)}
    assert resumo.identificacao_completa == (
        f"[{resumo.codigo}] Campanha de Inverno — Marca Ê"
    )
