from dataclasses import replace
from datetime import datetime, timezone
from uuid import UUID

import pytest

from mediad_planner.application.dto.briefing import (
    AdicionarRegistroSituacaoEntrada,
    ContextoAcessoBriefings,
)
from mediad_planner.application.use_cases.briefings import (
    AdicionarRegistroSituacaoMercadologica,
    RemoverRegistroSituacaoMercadologica,
)
from mediad_planner.application.dto.campanha import CriarCampanhaEntrada
from mediad_planner.composition.ambiente import (
    construir_ambiente_aplicacao_em_memoria,
)
from mediad_planner.domain.briefing.contexto import ContextoHerdadoBriefing
from mediad_planner.domain.briefing.entidades import Briefing
from mediad_planner.domain.campanha.codigo import CodigoCampanha
from mediad_planner.domain.campanha.vinculos import (
    AnuncianteCampanha,
    ParticipanteCampanha,
)
from mediad_planner.domain.common.enums import PapelAcesso
from mediad_planner.infrastructure.repositories.briefings_em_memoria import (
    RepositorioBriefingsEmMemoria,
)


def criar_ambiente_com_briefing():
    ambiente = construir_ambiente_aplicacao_em_memoria()
    campanha = ambiente.campanhas.criar_campanha(
        CriarCampanhaEntrada(
            nome="Campanha",
            nome_anunciante="Anunciante",
            nome_marca=None,
            nome_produto_servico=None,
            nome_planejador_responsavel="Planejadora",
            nomes_equipe=(),
            observacao_inicial=None,
            iniciar_briefing=True,
        )
    )
    ambiente.briefings.abrir_briefing(campanha.id_campanha)
    return ambiente, campanha.id_campanha


def entrada(valor: str = "10") -> AdicionarRegistroSituacaoEntrada:
    return AdicionarRegistroSituacaoEntrada(
        escopo="ANUNCIANTE",
        codigo_aspecto="participacao_mercado",
        aspecto="Participação de mercado",
        entidade_referencia=None,
        natureza="QUANTITATIVO",
        valor_quantitativo=valor,
        unidade="%",
        valor_qualitativo=None,
        fonte="Instituto",
        periodo_referencia="2026",
        observacao=None,
    )


class ContadorCallable:
    def __init__(self, retorno: object) -> None:
        self.retorno = retorno
        self.chamadas = 0

    def __call__(self):
        self.chamadas += 1
        return self.retorno


def preparar_casos_por_papel(papel: PapelAcesso):
    repositorio = RepositorioBriefingsEmMemoria()
    instante = datetime(2026, 8, 3, tzinfo=timezone.utc)
    contexto_herdado = ContextoHerdadoBriefing(
        codigo_campanha=CodigoCampanha("MP-202608-0001"),
        nome_campanha="Campanha",
        anunciante=AnuncianteCampanha(UUID(int=3), "Anunciante"),
        marca=None,
        produto_servico=None,
        planejador_responsavel=ParticipanteCampanha(UUID(int=4), "Pessoa"),
        equipe=(),
    )
    briefing = Briefing.criar_versao_inicial(
        id_briefing=UUID(int=5),
        id_campanha=UUID(int=6),
        id_espaco_trabalho=UUID(int=7),
        contexto_herdado=contexto_herdado,
        criado_por=UUID(int=8),
        criado_em=instante,
        atualizado_por=UUID(int=8),
        atualizado_em=instante,
    )
    repositorio.salvar(briefing)
    contexto = ContextoAcessoBriefings(UUID(int=8), UUID(int=7), papel)
    relogio = ContadorCallable(instante)
    gerador = ContadorCallable(UUID(int=9))
    adicionar = AdicionarRegistroSituacaoMercadologica(
        repositorio,
        contexto,
        relogio,
        gerador,
    )
    remover = RemoverRegistroSituacaoMercadologica(
        repositorio,
        contexto,
        relogio,
    )
    return adicionar, remover, relogio, gerador, briefing.id_campanha


@pytest.mark.parametrize(
    "papel",
    [PapelAcesso.PROPRIETARIO, PapelAcesso.EDITOR],
)
def test_papeis_de_autoria_adicionam_e_removem(papel: PapelAcesso) -> None:
    adicionar, remover, _, _, id_campanha = preparar_casos_por_papel(papel)

    resumo = adicionar.executar(id_campanha, entrada())
    removido = remover.executar(
        id_campanha,
        resumo.registros_situacao[0].id_registro,
    )

    assert removido.registros_situacao == ()


@pytest.mark.parametrize(
    "papel",
    [PapelAcesso.LEITOR, PapelAcesso.ADMINISTRADOR],
)
def test_papeis_sem_autoria_falham_antes_de_relogio_e_uuid(
    papel: PapelAcesso,
) -> None:
    adicionar, remover, relogio, gerador, id_campanha = preparar_casos_por_papel(
        papel
    )

    with pytest.raises(PermissionError):
        adicionar.executar(id_campanha, entrada())
    with pytest.raises(PermissionError):
        remover.executar(id_campanha, UUID(int=9))

    assert relogio.chamadas == 0
    assert gerador.chamadas == 0


@pytest.mark.parametrize("valor", ["10", "10.5", "-2.75"])
def test_adiciona_decimal_e_preserva_na_abertura(valor: str) -> None:
    ambiente, id_campanha = criar_ambiente_com_briefing()

    alterado = ambiente.briefings.adicionar_registro_situacao(
        id_campanha,
        entrada(valor),
    )
    reaberto = ambiente.briefings.abrir_briefing(id_campanha)

    assert alterado.estado == "EM_PREENCHIMENTO"
    assert reaberto.registros_situacao == alterado.registros_situacao
    assert alterado.registros_situacao[0].valor_quantitativo == valor
    assert isinstance(alterado.registros_situacao[0].escopo, str)


@pytest.mark.parametrize("valor", ["texto", "10,5"])
def test_rejeita_decimal_invalido(valor: str) -> None:
    ambiente, id_campanha = criar_ambiente_com_briefing()

    with pytest.raises(ValueError, match="Valor quantitativo inválido"):
        ambiente.briefings.adicionar_registro_situacao(
            id_campanha,
            entrada(valor),
        )


def test_aspecto_canonico_valida_escopo_e_ignora_rotulo_adulterado() -> None:
    ambiente, id_campanha = criar_ambiente_com_briefing()

    resumo = ambiente.briefings.adicionar_registro_situacao(
        id_campanha,
        replace(entrada(), aspecto="Rótulo adulterado"),
    )

    registro = resumo.registros_situacao[0]
    assert registro.codigo_aspecto == "participacao_mercado"
    assert registro.aspecto == "Participação de mercado"
    assert ambiente.briefings.abrir_briefing(
        id_campanha
    ).registros_situacao == resumo.registros_situacao
    with pytest.raises(ValueError, match="não pertence"):
        ambiente.briefings.adicionar_registro_situacao(
            id_campanha,
            replace(entrada(), codigo_aspecto="codigo_inexistente"),
        )
    with pytest.raises(ValueError, match="não pertence"):
        ambiente.briefings.adicionar_registro_situacao(
            id_campanha,
            replace(
                entrada(),
                escopo="MERCADO",
                codigo_aspecto="participacao_mercado",
            ),
        )


def test_aspecto_personalizado_exige_nome_e_nao_recebe_codigo() -> None:
    ambiente, id_campanha = criar_ambiente_com_briefing()
    personalizado = replace(
        entrada("7.5"),
        codigo_aspecto=None,
        aspecto="Índice de disponibilidade local",
        unidade="índice",
    )

    resumo = ambiente.briefings.adicionar_registro_situacao(
        id_campanha,
        personalizado,
    )

    assert resumo.registros_situacao[0].codigo_aspecto is None
    assert resumo.registros_situacao[0].aspecto == (
        "Índice de disponibilidade local"
    )
    for invalido in ("", "  ", "Outro aspecto", " Outro aspecto "):
        with pytest.raises(ValueError, match="Informe o nome"):
            ambiente.briefings.adicionar_registro_situacao(
                id_campanha,
                replace(
                    entrada(),
                    codigo_aspecto=None,
                    aspecto=invalido,
                ),
            )


def test_lista_aspectos_com_descricoes_e_rejeita_escopo_invalido() -> None:
    ambiente, _ = criar_ambiente_com_briefing()

    aspectos = ambiente.briefings.listar_aspectos_situacao("MERCADO")

    assert aspectos[0].rotulo == "Tamanho do mercado"
    assert aspectos[0].descricao
    assert aspectos[0].unidades_sugeridas == ("R$", "unidades", "pessoas")
    with pytest.raises(ValueError, match="Escopo inválido"):
        ambiente.briefings.listar_aspectos_situacao("GERAL")


def test_remove_um_registro_e_preserva_os_demais_e_estado() -> None:
    ambiente, id_campanha = criar_ambiente_com_briefing()
    primeiro = ambiente.briefings.adicionar_registro_situacao(
        id_campanha,
        entrada("10"),
    )
    segundo = ambiente.briefings.adicionar_registro_situacao(
        id_campanha,
        replace(entrada("20"), aspecto="Penetração"),
    )

    removido = ambiente.briefings.remover_registro_situacao(
        id_campanha,
        primeiro.registros_situacao[0].id_registro,
    )

    assert removido.estado == "EM_PREENCHIMENTO"
    assert removido.registros_situacao == (segundo.registros_situacao[1],)
    with pytest.raises(LookupError):
        ambiente.briefings.remover_registro_situacao(
            id_campanha,
            UUID(int=999),
        )
