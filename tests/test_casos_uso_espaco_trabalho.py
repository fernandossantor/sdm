from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from uuid import UUID

import pytest

from mediad_planner.application.dto.campanha import (
    ContextoAcessoCampanhas,
    CriarCampanhaEntrada,
)
from mediad_planner.application.dto.espaco_trabalho import (
    ContextoAcessoEspacoTrabalho,
)
from mediad_planner.application.use_cases.campanhas import CriarCampanha
from mediad_planner.application.use_cases.espaco_trabalho import (
    ObterEspacoTrabalhoCampanha,
)
from mediad_planner.composition.ambiente import construir_ambiente_aplicacao_em_memoria
from mediad_planner.domain.common.enums import PapelAcesso
from mediad_planner.infrastructure.repositories.briefings_em_memoria import (
    RepositorioBriefingsEmMemoria,
)
from mediad_planner.infrastructure.repositories.campanhas_em_memoria import (
    RepositorioCampanhasEmMemoria,
)


ID_USUARIO = UUID("00000000-0000-0000-0000-000000000101")
ID_ESPACO = UUID("00000000-0000-0000-0000-000000000102")
ID_CAMPANHA = UUID("00000000-0000-0000-0000-000000000103")
INSTANTE = datetime(2026, 8, 3, 12, 0, tzinfo=timezone.utc)


def _entrada(iniciar: bool = False) -> CriarCampanhaEntrada:
    return CriarCampanhaEntrada(
        nome="Campanha",
        nome_anunciante="Anunciante",
        nome_marca=None,
        nome_produto_servico=None,
        nome_planejador_responsavel="Planejadora",
        nomes_equipe=(),
        observacao_inicial=None,
        iniciar_briefing=iniciar,
    )


def _repositorio_com_campanha() -> RepositorioCampanhasEmMemoria:
    repositorio = RepositorioCampanhasEmMemoria()
    criar = CriarCampanha(
        repositorio=repositorio,
        contexto_acesso=ContextoAcessoCampanhas(
            id_usuario=ID_USUARIO,
            id_espaco_trabalho=ID_ESPACO,
            papel=PapelAcesso.EDITOR,
        ),
        relogio=lambda: INSTANTE,
        gerador_uuid=lambda: ID_CAMPANHA,
    )
    criar.executar(_entrada())
    return repositorio


def _caso_obter(
    papel: PapelAcesso,
    repositorio_campanhas: object,
    repositorio_briefings: object,
) -> ObterEspacoTrabalhoCampanha:
    return ObterEspacoTrabalhoCampanha(
        repositorio_campanhas=repositorio_campanhas,
        repositorio_briefings=repositorio_briefings,
        contexto_acesso=ContextoAcessoEspacoTrabalho(
            id_usuario=ID_USUARIO,
            id_espaco_trabalho=ID_ESPACO,
            papel=papel,
        ),
    )


class _RepositorioNaoDeveSerConsultado:
    def __getattr__(self, nome: str) -> object:
        raise AssertionError(f"repositório não deveria ser consultado: {nome}")


class _CampanhasEspiao:
    def __init__(self, repositorio: RepositorioCampanhasEmMemoria) -> None:
        self._repositorio = repositorio
        self.obtencoes = 0
        self.salvamentos = 0
        self.reservas = 0

    def obter(self, id_espaco_trabalho: UUID, id_campanha: UUID) -> object:
        self.obtencoes += 1
        return self._repositorio.obter(id_espaco_trabalho, id_campanha)

    def salvar(self, campanha: object) -> None:
        self.salvamentos += 1
        self._repositorio.salvar(campanha)

    def reservar_proximo_sequencial_global(self) -> int:
        self.reservas += 1
        return self._repositorio.reservar_proximo_sequencial_global()


class _BriefingsEspiao:
    def __init__(self, repositorio: RepositorioBriefingsEmMemoria) -> None:
        self._repositorio = repositorio
        self.obtencoes = 0
        self.salvamentos = 0

    def obter_por_campanha(
        self,
        id_espaco_trabalho: UUID,
        id_campanha: UUID,
    ) -> object:
        self.obtencoes += 1
        return self._repositorio.obter_por_campanha(
            id_espaco_trabalho,
            id_campanha,
        )

    def salvar(self, briefing: object) -> None:
        self.salvamentos += 1
        self._repositorio.salvar(briefing)


def test_consulta_rascunho_nao_cria_nem_altera_e_expoe_todos_modulos() -> None:
    ambiente = construir_ambiente_aplicacao_em_memoria()
    campanha = ambiente.campanhas.criar_campanha(_entrada())

    resumo = ambiente.espaco_trabalho.obter_espaco_trabalho(
        campanha.id_campanha
    )

    assert resumo.campanha == campanha
    assert resumo.briefing is None
    assert tuple(item.codigo for item in resumo.modulos) == (
        "VISAO_GERAL",
        "BRIEFING",
        "TRADUCAO_ESTRATEGICA",
        "ARQUITETURA_DE_MIDIA",
        "SIMULACAO",
        "PLANO_CONSOLIDADO",
    )
    assert resumo.modulos[0].disponivel is True
    assert resumo.modulos[0].estado == "DISPONIVEL"
    assert resumo.modulos[1].estado == "BLOQUEADO"
    assert resumo.modulos[1].motivo_bloqueio == (
        "Inicie o Briefing para continuar."
    )
    assert ambiente.espaco_trabalho.obter_espaco_trabalho(
        campanha.id_campanha
    ).briefing is None


def test_briefing_existente_vazio_e_etapa_atual_e_futuros_bloqueados() -> None:
    ambiente = construir_ambiente_aplicacao_em_memoria()
    campanha = ambiente.campanhas.criar_campanha(_entrada())
    ambiente.campanhas.iniciar_briefing(campanha.id_campanha)
    ambiente.briefings.abrir_briefing(campanha.id_campanha)

    resumo = ambiente.espaco_trabalho.obter_espaco_trabalho(
        campanha.id_campanha
    )

    briefing = resumo.modulos[1]
    assert resumo.briefing is not None
    assert resumo.briefing.registros_situacao == ()
    assert briefing.disponivel is True
    assert briefing.estado == "ETAPA_ATUAL"
    assert resumo.modulos[2].motivo_bloqueio == (
        "Conclua o Briefing para continuar."
    )
    assert all(not item.disponivel for item in resumo.modulos[2:])


def test_preparar_briefing_e_idempotente_para_rascunho_e_inicio_imediato() -> None:
    ambiente = construir_ambiente_aplicacao_em_memoria()
    rascunho = ambiente.campanhas.criar_campanha(_entrada())

    preparado = ambiente.espaco_trabalho.preparar_briefing(
        rascunho.id_campanha
    )
    novamente = ambiente.espaco_trabalho.preparar_briefing(
        rascunho.id_campanha
    )

    assert preparado.campanha.situacao == "EM_ANDAMENTO"
    assert preparado.campanha.etapa_atual == "BRIEFING"
    assert preparado.briefing is not None
    assert novamente.briefing is not None
    assert novamente.briefing.id_briefing == preparado.briefing.id_briefing
    assert novamente.briefing.numero_versao == 1

    iniciada = ambiente.campanhas.criar_campanha(_entrada(iniciar=True))
    preparada = ambiente.espaco_trabalho.preparar_briefing(
        iniciada.id_campanha
    )
    assert preparada.briefing is not None
    assert preparada.briefing.numero_versao == 1


def test_campanha_inexistente_e_dtos_congelados() -> None:
    ambiente = construir_ambiente_aplicacao_em_memoria()
    with pytest.raises(
        LookupError,
        match="Campanha não encontrada no espaço atual",
    ):
        ambiente.espaco_trabalho.obter_espaco_trabalho(UUID(int=999))

    campanha = ambiente.campanhas.criar_campanha(_entrada())
    resumo = ambiente.espaco_trabalho.obter_espaco_trabalho(
        campanha.id_campanha
    )
    with pytest.raises(FrozenInstanceError):
        resumo.modulos = ()


@pytest.mark.parametrize(
    "papel",
    (
        PapelAcesso.PROPRIETARIO,
        PapelAcesso.EDITOR,
        PapelAcesso.LEITOR,
    ),
)
def test_papeis_autorizados_consultam_espaco_trabalho(
    papel: PapelAcesso,
) -> None:
    caso = _caso_obter(
        papel=papel,
        repositorio_campanhas=_repositorio_com_campanha(),
        repositorio_briefings=RepositorioBriefingsEmMemoria(),
    )

    resumo = caso.executar(ID_CAMPANHA)

    assert resumo.campanha.id_campanha == ID_CAMPANHA
    assert resumo.modulos


def test_administrador_e_rejeitado_antes_de_consultar_repositorios() -> None:
    repositorio_proibido = _RepositorioNaoDeveSerConsultado()
    caso = _caso_obter(
        papel=PapelAcesso.ADMINISTRADOR,
        repositorio_campanhas=repositorio_proibido,
        repositorio_briefings=repositorio_proibido,
    )

    with pytest.raises(
        PermissionError,
        match="Papel sem permissão para acessar o espaço de trabalho",
    ):
        caso.executar(ID_CAMPANHA)


def test_consulta_executada_nao_grava_e_preserva_estado() -> None:
    campanhas_reais = _repositorio_com_campanha()
    briefings_reais = RepositorioBriefingsEmMemoria()
    campanha_antes = campanhas_reais.obter(ID_ESPACO, ID_CAMPANHA)
    briefing_antes = briefings_reais.obter_por_campanha(
        ID_ESPACO,
        ID_CAMPANHA,
    )
    assert campanha_antes is not None
    estado_antes = (
        campanha_antes.situacao,
        campanha_antes.etapa_atual,
        campanha_antes.atualizado_em,
    )
    campanhas = _CampanhasEspiao(campanhas_reais)
    briefings = _BriefingsEspiao(briefings_reais)
    caso = _caso_obter(
        papel=PapelAcesso.LEITOR,
        repositorio_campanhas=campanhas,
        repositorio_briefings=briefings,
    )

    resumo = caso.executar(ID_CAMPANHA)

    campanha_depois = campanhas_reais.obter(ID_ESPACO, ID_CAMPANHA)
    briefing_depois = briefings_reais.obter_por_campanha(
        ID_ESPACO,
        ID_CAMPANHA,
    )
    assert resumo.campanha.id_campanha == ID_CAMPANHA
    assert campanhas.obtencoes == 1
    assert briefings.obtencoes == 1
    assert campanhas.salvamentos == 0
    assert briefings.salvamentos == 0
    assert campanhas.reservas == 0
    assert campanha_depois is campanha_antes
    assert briefing_depois is briefing_antes
    assert campanha_depois is not None
    assert (
        campanha_depois.situacao,
        campanha_depois.etapa_atual,
        campanha_depois.atualizado_em,
    ) == estado_antes
