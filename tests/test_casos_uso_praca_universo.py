from dataclasses import FrozenInstanceError
from uuid import UUID

import pytest

from mediad_planner.application.dto.campanha import CriarCampanhaEntrada
from mediad_planner.application.dto.briefing import ContextoAcessoBriefings
from mediad_planner.application.dto.praca_universo import (
    AdicionarPracaEntrada,
    AdicionarUniversoEntrada,
)
from mediad_planner.application.use_cases.praca_universo import (
    AdicionarPraca,
    ListarTiposPracaTerritorial,
    ListarUnidadesPopulacionais,
)
from mediad_planner.composition.ambiente import construir_ambiente_aplicacao_em_memoria
from mediad_planner.domain.common.enums import PapelAcesso


def _ambiente_preparado():
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
    ambiente.espaco_trabalho.preparar_briefing(campanha.id_campanha)
    return ambiente, campanha.id_campanha


def _entrada_praca(**alteracoes: object) -> AdicionarPracaEntrada:
    dados = dict(
        tipo="MUNICIPIO",
        nome="São Borja",
        codigo_oficial="4318002",
        abrangencia="Todo o município",
        valor_populacao_referencia="60000.5",
        codigo_unidade_populacional="pessoas",
        unidade_populacional="rótulo forjado",
        fonte="IBGE",
        data_referencia="2025",
        observacao=None,
    )
    dados.update(alteracoes)
    return AdicionarPracaEntrada(**dados)


def _entrada_universo(ids_pracas: tuple[UUID, ...], **alteracoes: object):
    dados = dict(
        nome="Adultos",
        definicao="Pessoas com 18 anos ou mais",
        ids_pracas=ids_pracas,
        valor_populacional="45000",
        codigo_unidade="pessoas",
        unidade="rótulo forjado",
        fonte=None,
        data_referencia=None,
        criterios_inclusao="Residentes",
        criterios_exclusao="Menores de 18 anos",
        observacao=None,
    )
    dados.update(alteracoes)
    return AdicionarUniversoEntrada(**dados)


def test_catalogos_nao_dependem_de_repositorio() -> None:
    assert ListarTiposPracaTerritorial().executar()
    assert ListarUnidadesPopulacionais().executar()


def test_adiciona_praca_canonica_e_personalizada() -> None:
    ambiente, id_campanha = _ambiente_preparado()
    resumo = ambiente.briefings.adicionar_praca(id_campanha, _entrada_praca())
    assert resumo.estado == "EM_PREENCHIMENTO"
    assert resumo.pracas[0].valor_populacao_referencia == "60000.5"
    assert resumo.pracas[0].unidade_populacional == "Pessoas"
    personalizado = ambiente.briefings.adicionar_praca(
        id_campanha,
        _entrada_praca(
            nome="Lojas",
            codigo_oficial=None,
            valor_populacao_referencia="10",
            codigo_unidade_populacional=None,
            unidade_populacional="Lojas ativas",
        ),
    )
    assert personalizado.pracas[1].codigo_unidade_populacional is None
    assert personalizado.pracas[1].unidade_populacional == "Lojas ativas"


@pytest.mark.parametrize(
    ("alteracoes", "mensagem"),
    (
        ({"tipo": "INVALIDO"}, "Tipo de praça inválido"),
        ({"codigo_unidade_populacional": "invalida"}, "Unidade populacional inválida"),
        ({"valor_populacao_referencia": "10,5"}, "Valor populacional inválido"),
        ({"valor_populacao_referencia": "abc"}, "Valor populacional inválido"),
        ({"valor_populacao_referencia": "0"}, "Valor populacional inválido"),
        ({"valor_populacao_referencia": "-1"}, "Valor populacional inválido"),
    ),
)
def test_adicao_de_praca_rejeita_entradas_invalidas(
    alteracoes: dict[str, object],
    mensagem: str,
) -> None:
    ambiente, id_campanha = _ambiente_preparado()
    with pytest.raises(ValueError, match=mensagem):
        ambiente.briefings.adicionar_praca(
            id_campanha,
            _entrada_praca(**alteracoes),
        )


def test_universo_multiplas_pracas_ordem_unidade_e_remocoes() -> None:
    ambiente, id_campanha = _ambiente_preparado()
    resumo = ambiente.briefings.adicionar_praca(id_campanha, _entrada_praca())
    resumo = ambiente.briefings.adicionar_praca(
        id_campanha,
        _entrada_praca(nome="Centro", codigo_oficial=None),
    )
    ids = (resumo.pracas[1].id_praca, resumo.pracas[0].id_praca)
    resumo = ambiente.briefings.adicionar_universo(
        id_campanha,
        _entrada_universo(ids),
    )
    universo = resumo.universos[0]
    assert universo.ids_pracas == ids
    assert universo.unidade == "Pessoas"
    with pytest.raises(ValueError, match="Praça vinculada a Universo"):
        ambiente.briefings.remover_praca(id_campanha, ids[0])
    resumo = ambiente.briefings.remover_universo(
        id_campanha,
        universo.id_universo,
    )
    resumo = ambiente.briefings.remover_praca(id_campanha, ids[0])
    assert resumo.estado == "EM_PREENCHIMENTO"
    assert len(resumo.pracas) == 1


def test_universo_personalizado_e_validacoes_de_praca() -> None:
    ambiente, id_campanha = _ambiente_preparado()
    resumo = ambiente.briefings.adicionar_praca(id_campanha, _entrada_praca())
    id_praca = resumo.pracas[0].id_praca
    personalizado = ambiente.briefings.adicionar_universo(
        id_campanha,
        _entrada_universo(
            (id_praca,),
            valor_populacional=None,
            codigo_unidade=None,
            unidade="Organizações",
        ),
    )
    assert personalizado.universos[0].codigo_unidade is None
    assert personalizado.universos[0].unidade == "Organizações"
    with pytest.raises(ValueError, match="ao menos uma Praça"):
        ambiente.briefings.adicionar_universo(
            id_campanha,
            _entrada_universo(()),
        )
    with pytest.raises(ValueError, match="Praça relacionada não existe"):
        ambiente.briefings.adicionar_universo(
            id_campanha,
            _entrada_universo((UUID(int=999),)),
        )


def test_dtos_sao_congelados() -> None:
    entrada = _entrada_praca()
    with pytest.raises(FrozenInstanceError):
        entrada.nome = "Outro"


class _RepositorioPermissoes:
    def __init__(self, permite_consulta: bool) -> None:
        self.permite_consulta = permite_consulta
        self.consultas = 0

    def obter_por_campanha(self, id_espaco: UUID, id_campanha: UUID):
        if not self.permite_consulta:
            raise AssertionError("repositório não deveria ser consultado")
        self.consultas += 1
        return None


def _caso_permissao(papel: PapelAcesso, repositorio: object) -> AdicionarPraca:
    return AdicionarPraca(
        repositorio=repositorio,
        contexto_acesso=ContextoAcessoBriefings(
            id_usuario=UUID(int=1),
            id_espaco_trabalho=UUID(int=2),
            papel=papel,
        ),
        relogio=lambda: None,
        gerador_uuid=lambda: UUID(int=3),
    )


@pytest.mark.parametrize("papel", (PapelAcesso.PROPRIETARIO, PapelAcesso.EDITOR))
def test_proprietario_e_editor_passam_pela_autorizacao(papel: PapelAcesso) -> None:
    repositorio = _RepositorioPermissoes(permite_consulta=True)
    caso = _caso_permissao(papel, repositorio)
    with pytest.raises(LookupError, match="Briefing não encontrado"):
        caso.executar(UUID(int=4), _entrada_praca())
    assert repositorio.consultas == 1


@pytest.mark.parametrize("papel", (PapelAcesso.LEITOR, PapelAcesso.ADMINISTRADOR))
def test_leitor_e_administrador_falham_antes_do_repositorio(
    papel: PapelAcesso,
) -> None:
    repositorio = _RepositorioPermissoes(permite_consulta=False)
    caso = _caso_permissao(papel, repositorio)
    with pytest.raises(
        PermissionError,
        match="Papel sem permissão para alterar Briefings",
    ):
        caso.executar(UUID(int=4), _entrada_praca())
    assert repositorio.consultas == 0
