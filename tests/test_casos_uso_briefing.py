from datetime import datetime, timezone
from uuid import UUID

import pytest

from mediad_planner.application.dto.briefing import (
    BriefingResumo,
    ContextoAcessoBriefings,
)
from mediad_planner.application.use_cases.briefings import AbrirBriefingCampanha
from mediad_planner.domain.campanha.codigo import gerar_codigo_campanha
from mediad_planner.domain.campanha.entidades import Campanha
from mediad_planner.domain.campanha.vinculos import (
    AnuncianteCampanha,
    MarcaCampanha,
    ParticipanteCampanha,
    ProdutoServicoCampanha,
)
from mediad_planner.domain.common.enums import PapelAcesso
from mediad_planner.infrastructure.repositories.briefings_em_memoria import (
    RepositorioBriefingsEmMemoria,
)
from mediad_planner.infrastructure.repositories.campanhas_em_memoria import (
    RepositorioCampanhasEmMemoria,
)


INSTANTE = datetime(2026, 8, 2, 12, 0, tzinfo=timezone.utc)
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_ESPACO = UUID("00000000-0000-0000-0000-000000000002")


class GeradorUUIDDeterministico:
    def __init__(self) -> None:
        self.chamadas = 0

    def __call__(self) -> UUID:
        self.chamadas += 1
        return UUID(int=100 + self.chamadas)


def criar_campanha(
    *,
    id_espaco: UUID = ID_ESPACO,
    iniciar: bool = True,
    com_marca: bool = True,
    com_produto: bool = True,
) -> Campanha:
    id_anunciante = UUID(int=10)
    marca = None
    if com_marca:
        marca = MarcaCampanha(
            id_marca=UUID(int=11),
            id_anunciante=id_anunciante,
            nome_snapshot="Marca Áurea",
        )
    produto = None
    if com_produto:
        produto = ProdutoServicoCampanha(
            id_produto_servico=UUID(int=12),
            id_anunciante=id_anunciante,
            id_marca=marca.id_marca if marca else None,
            nome_snapshot="Produto Um",
        )
    campanha = Campanha.criar_rascunho(
        id_campanha=UUID(int=20),
        id_espaco_trabalho=id_espaco,
        codigo=gerar_codigo_campanha(INSTANTE, 1),
        nome="Campanha Agosto",
        anunciante=AnuncianteCampanha(
            id_anunciante=id_anunciante,
            nome_snapshot="Anunciante Exemplo",
        ),
        marca=marca,
        produto_servico=produto,
        planejador_responsavel=ParticipanteCampanha(
            id_usuario=ID_USUARIO,
            nome_snapshot="Planejadora",
        ),
        equipe=(
            ParticipanteCampanha(
                id_usuario=UUID(int=13),
                nome_snapshot="Analista",
            ),
        ),
        observacao_inicial=None,
        criado_por=ID_USUARIO,
        criado_em=INSTANTE,
        atualizado_por=ID_USUARIO,
        atualizado_em=INSTANTE,
    )
    if iniciar:
        return campanha.iniciar_briefing(
            atualizado_por=ID_USUARIO,
            atualizado_em=INSTANTE,
        )
    return campanha


def construir_caso(
    papel: PapelAcesso,
    campanha: Campanha | None = None,
    repositorio_briefings: RepositorioBriefingsEmMemoria | None = None,
    id_espaco: UUID = ID_ESPACO,
) -> tuple[
    AbrirBriefingCampanha,
    RepositorioBriefingsEmMemoria,
    GeradorUUIDDeterministico,
]:
    repositorio_campanhas = RepositorioCampanhasEmMemoria()
    if campanha is not None:
        repositorio_campanhas.salvar(campanha)
    briefings = repositorio_briefings or RepositorioBriefingsEmMemoria()
    gerador = GeradorUUIDDeterministico()
    contexto = ContextoAcessoBriefings(
        id_usuario=ID_USUARIO,
        id_espaco_trabalho=id_espaco,
        papel=papel,
    )
    caso = AbrirBriefingCampanha(
        repositorio_campanhas=repositorio_campanhas,
        repositorio_briefings=briefings,
        contexto_acesso=contexto,
        relogio=lambda: INSTANTE,
        gerador_uuid=gerador,
    )
    return caso, briefings, gerador


@pytest.mark.parametrize(
    "papel",
    [PapelAcesso.PROPRIETARIO, PapelAcesso.EDITOR],
)
def test_autores_criam_e_abrem_briefing(papel: PapelAcesso) -> None:
    campanha = criar_campanha()
    caso, _, _ = construir_caso(papel, campanha)

    resumo = caso.executar(campanha.id_campanha)

    assert isinstance(resumo, BriefingResumo)
    assert resumo.numero_versao == 1
    assert resumo.estado == "RASCUNHO"
    assert resumo.codigo_campanha == "MP-202608-0001"
    assert resumo.nome_campanha == "Campanha Agosto"
    assert resumo.anunciante == "Anunciante Exemplo"
    assert resumo.marca == "Marca Áurea"
    assert resumo.produto_servico == "Produto Um"
    assert resumo.planejador_responsavel == "Planejadora"
    assert resumo.equipe == ("Analista",)
    assert not hasattr(resumo, "contexto_herdado")


def test_contexto_herdado_preserva_campos_opcionais_ausentes() -> None:
    campanha = criar_campanha(com_marca=False, com_produto=False)
    caso, _, _ = construir_caso(PapelAcesso.EDITOR, campanha)

    resumo = caso.executar(campanha.id_campanha)

    assert resumo.marca is None
    assert resumo.produto_servico is None


def test_leitor_nao_cria_versao_inicial() -> None:
    campanha = criar_campanha()
    caso, _, gerador = construir_caso(PapelAcesso.LEITOR, campanha)

    with pytest.raises(PermissionError):
        caso.executar(campanha.id_campanha)

    assert gerador.chamadas == 0


def test_leitor_abre_briefing_existente_sem_alterar_dados() -> None:
    campanha = criar_campanha()
    caso_editor, repositorio, _ = construir_caso(PapelAcesso.EDITOR, campanha)
    criado = caso_editor.executar(campanha.id_campanha)
    caso_leitor, _, gerador = construir_caso(
        PapelAcesso.LEITOR,
        campanha,
        repositorio,
    )

    reaberto = caso_leitor.executar(campanha.id_campanha)

    assert reaberto == criado
    assert gerador.chamadas == 0


def test_administrador_nao_cria_nem_abre() -> None:
    campanha = criar_campanha()
    caso, _, _ = construir_caso(PapelAcesso.ADMINISTRADOR, campanha)

    with pytest.raises(PermissionError):
        caso.executar(campanha.id_campanha)


def test_campanha_inexistente_e_isolamento_entre_espacos() -> None:
    campanha = criar_campanha()
    caso_inexistente, _, _ = construir_caso(PapelAcesso.EDITOR)
    outro_espaco = UUID(int=999)
    caso_outro_espaco, _, _ = construir_caso(
        PapelAcesso.EDITOR,
        campanha,
        id_espaco=outro_espaco,
    )

    with pytest.raises(LookupError):
        caso_inexistente.executar(campanha.id_campanha)
    with pytest.raises(LookupError):
        caso_outro_espaco.executar(campanha.id_campanha)


def test_campanha_em_abertura_nao_pode_criar_briefing() -> None:
    campanha = criar_campanha(iniciar=False)
    caso, _, gerador = construir_caso(PapelAcesso.EDITOR, campanha)

    with pytest.raises(ValueError):
        caso.executar(campanha.id_campanha)

    assert gerador.chamadas == 0


def test_segunda_abertura_e_idempotente() -> None:
    campanha = criar_campanha()
    caso, _, gerador = construir_caso(PapelAcesso.EDITOR, campanha)

    primeiro = caso.executar(campanha.id_campanha)
    segundo = caso.executar(campanha.id_campanha)

    assert segundo.id_briefing == primeiro.id_briefing
    assert segundo.numero_versao == primeiro.numero_versao
    assert segundo.criado_em == primeiro.criado_em
    assert segundo.atualizado_em == primeiro.atualizado_em
    assert gerador.chamadas == 1
