from dataclasses import fields, replace
from datetime import datetime, timezone
from uuid import UUID

import pytest

from mediad_planner.application.dto.briefing import ContextoAcessoBriefings
from mediad_planner.application.dto.campanha import CriarCampanhaEntrada
from mediad_planner.application.dto.objetivos_declarados import (
    AdicionarObjetivoComunicacaoEntrada,
    AdicionarObjetivoMarketingEntrada,
)
from mediad_planner.application.use_cases.objetivos_declarados import (
    AdicionarObjetivoMarketing,
)
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


def ambiente_aberto():
    ambiente = construir_ambiente_aplicacao_em_memoria()
    campanha = ambiente.campanhas.criar_campanha(
        CriarCampanhaEntrada(
            nome="Campanha",
            nome_anunciante="Anunciante",
            nome_marca=None,
            nome_produto_servico=None,
            nome_planejador_responsavel="Pessoa",
            nomes_equipe=(),
            observacao_inicial=None,
            iniciar_briefing=True,
        )
    )
    ambiente.briefings.abrir_briefing(campanha.id_campanha)
    return ambiente, campanha.id_campanha


def entrada_marketing() -> AdicionarObjetivoMarketingEntrada:
    return AdicionarObjetivoMarketingEntrada(
        codigo_objetivo="marketing_crescimento",
        objetivo="Rótulo adulterado",
        dimensoes_composto=("PRODUTO", "PRACA"),
        prioridade_declarada=5,
        intensidade_declarada=4,
        justificativa="Expandir presença",
    )


def entrada_comunicacao(
    relacionados: tuple[UUID, ...],
) -> AdicionarObjetivoComunicacaoEntrada:
    return AdicionarObjetivoComunicacaoEntrada(
        codigo_objetivo="comunicacao_notoriedade",
        objetivo="Rótulo adulterado",
        ids_objetivos_marketing_relacionados=relacionados,
        prioridade_declarada=4,
        intensidade_declarada=3,
        justificativa="Apoiar crescimento",
    )


def test_catalogos_e_dimensoes_chegam_por_dtos() -> None:
    ambiente, _ = ambiente_aberto()

    marketing = ambiente.briefings.listar_objetivos_marketing()
    comunicacao = ambiente.briefings.listar_objetivos_comunicacao()
    dimensoes = ambiente.briefings.listar_dimensoes_composto_marketing()

    assert len(marketing) == 10
    assert len(comunicacao) == 17
    assert marketing[4].codigo == "marketing_crescimento"
    assert marketing[4].descricao
    assert tuple(item.codigo for item in dimensoes) == (
        "PRODUTO",
        "PRECO",
        "PRACA",
        "PROMOCAO",
    )


def test_adiciona_canonicos_preserva_vinculo_e_abertura() -> None:
    ambiente, id_campanha = ambiente_aberto()

    marketing = ambiente.briefings.adicionar_objetivo_marketing(
        id_campanha,
        entrada_marketing(),
    )
    id_marketing = marketing.objetivos_marketing[0].id_objetivo
    comunicacao = ambiente.briefings.adicionar_objetivo_comunicacao(
        id_campanha,
        entrada_comunicacao((id_marketing,)),
    )
    reaberto = ambiente.briefings.abrir_briefing(id_campanha)

    salvo_marketing = reaberto.objetivos_marketing[0]
    salvo_comunicacao = reaberto.objetivos_comunicacao[0]
    assert salvo_marketing.objetivo == "Crescimento"
    assert salvo_marketing.codigo_objetivo == "marketing_crescimento"
    assert salvo_marketing.dimensoes_composto == ("PRODUTO", "PRACA")
    assert salvo_marketing.rotulos_dimensoes_composto == (
        "Produto",
        "Praça (distribuição)",
    )
    assert salvo_marketing.prioridade_declarada == 5
    assert salvo_marketing.intensidade_declarada == 4
    assert salvo_comunicacao.objetivo == "Notoriedade"
    assert salvo_comunicacao.ids_objetivos_marketing_relacionados == (
        id_marketing,
    )
    assert comunicacao.estado == "EM_PREENCHIMENTO"


def test_personalizados_e_relacao_vazia_sao_aceitos() -> None:
    ambiente, id_campanha = ambiente_aberto()
    marketing = replace(
        entrada_marketing(),
        codigo_objetivo=None,
        objetivo="Expansão regional sustentável",
        dimensoes_composto=(),
    )
    comunicacao = replace(
        entrada_comunicacao(()),
        codigo_objetivo=None,
        objetivo="Esclarecimento institucional",
    )

    resumo = ambiente.briefings.adicionar_objetivo_marketing(
        id_campanha,
        marketing,
    )
    resumo = ambiente.briefings.adicionar_objetivo_comunicacao(
        id_campanha,
        comunicacao,
    )

    assert resumo.objetivos_marketing[0].codigo_objetivo is None
    assert resumo.objetivos_comunicacao[0].codigo_objetivo is None
    assert resumo.objetivos_comunicacao[0].ids_objetivos_marketing_relacionados == ()


@pytest.mark.parametrize("texto", ("", " ", "Outro objetivo", " Outro objetivo "))
def test_personalizados_rejeitam_opcao_visual(texto: str) -> None:
    ambiente, id_campanha = ambiente_aberto()

    with pytest.raises(ValueError, match="Informe o Objetivo de Marketing"):
        ambiente.briefings.adicionar_objetivo_marketing(
            id_campanha,
            replace(
                entrada_marketing(),
                codigo_objetivo=None,
                objetivo=texto,
            ),
        )
    with pytest.raises(ValueError, match="Informe o Objetivo de Comunicação"):
        ambiente.briefings.adicionar_objetivo_comunicacao(
            id_campanha,
            replace(
                entrada_comunicacao(()),
                codigo_objetivo=None,
                objetivo=texto,
            ),
        )


def test_rejeita_codigos_dimensoes_escalas_e_relacoes_invalidas() -> None:
    ambiente, id_campanha = ambiente_aberto()

    with pytest.raises(ValueError, match="Marketing inválido"):
        ambiente.briefings.adicionar_objetivo_marketing(
            id_campanha,
            replace(entrada_marketing(), codigo_objetivo="inexistente"),
        )
    with pytest.raises(ValueError, match="Dimensão"):
        ambiente.briefings.adicionar_objetivo_marketing(
            id_campanha,
            replace(entrada_marketing(), dimensoes_composto=("INVALIDA",)),
        )
    with pytest.raises(ValueError, match="prioridade"):
        ambiente.briefings.adicionar_objetivo_marketing(
            id_campanha,
            replace(entrada_marketing(), prioridade_declarada=6),
        )
    with pytest.raises(ValueError, match="Comunicação inválido"):
        ambiente.briefings.adicionar_objetivo_comunicacao(
            id_campanha,
            replace(entrada_comunicacao(()), codigo_objetivo="inexistente"),
        )
    with pytest.raises(ValueError, match="não existe"):
        ambiente.briefings.adicionar_objetivo_comunicacao(
            id_campanha,
            entrada_comunicacao((UUID(int=999),)),
        )


def test_remocoes_respeitam_vinculo_e_preservam_outros() -> None:
    ambiente, id_campanha = ambiente_aberto()
    primeiro = ambiente.briefings.adicionar_objetivo_marketing(
        id_campanha,
        entrada_marketing(),
    ).objetivos_marketing[0]
    segundo = ambiente.briefings.adicionar_objetivo_marketing(
        id_campanha,
        replace(
            entrada_marketing(),
            codigo_objetivo=None,
            objetivo="Expansão regional",
        ),
    ).objetivos_marketing[1]
    comunicacao = ambiente.briefings.adicionar_objetivo_comunicacao(
        id_campanha,
        entrada_comunicacao((primeiro.id_objetivo,)),
    ).objetivos_comunicacao[0]

    with pytest.raises(ValueError, match="vinculado"):
        ambiente.briefings.remover_objetivo_marketing(
            id_campanha,
            primeiro.id_objetivo,
        )
    ambiente.briefings.remover_objetivo_marketing(
        id_campanha,
        segundo.id_objetivo,
    )
    ambiente.briefings.remover_objetivo_comunicacao(
        id_campanha,
        comunicacao.id_objetivo,
    )
    final = ambiente.briefings.remover_objetivo_marketing(
        id_campanha,
        primeiro.id_objetivo,
    )

    assert final.estado == "EM_PREENCHIMENTO"
    assert final.objetivos_marketing == ()
    assert final.objetivos_comunicacao == ()


class Contador:
    def __init__(self, retorno: object) -> None:
        self.retorno = retorno
        self.chamadas = 0

    def __call__(self):
        self.chamadas += 1
        return self.retorno


@pytest.mark.parametrize("papel", (PapelAcesso.LEITOR, PapelAcesso.ADMINISTRADOR))
def test_permissao_antecede_relogio_e_uuid(papel: PapelAcesso) -> None:
    repositorio = RepositorioBriefingsEmMemoria()
    agora = datetime(2026, 8, 3, tzinfo=timezone.utc)
    briefing = Briefing.criar_versao_inicial(
        id_briefing=UUID(int=1),
        id_campanha=UUID(int=2),
        id_espaco_trabalho=UUID(int=3),
        contexto_herdado=ContextoHerdadoBriefing(
            CodigoCampanha("MP-202608-0001"),
            "Campanha",
            AnuncianteCampanha(UUID(int=4), "Anunciante"),
            None,
            None,
            ParticipanteCampanha(UUID(int=5), "Pessoa"),
            (),
        ),
        criado_por=UUID(int=6),
        criado_em=agora,
        atualizado_por=UUID(int=6),
        atualizado_em=agora,
    )
    repositorio.salvar(briefing)
    relogio = Contador(agora)
    gerador = Contador(UUID(int=7))
    caso = AdicionarObjetivoMarketing(
        repositorio,
        ContextoAcessoBriefings(UUID(int=6), UUID(int=3), papel),
        relogio,
        gerador,
    )

    with pytest.raises(PermissionError):
        caso.executar(briefing.id_campanha, entrada_marketing())

    assert relogio.chamadas == 0
    assert gerador.chamadas == 0


def test_dtos_nao_expoem_dominio_peso_ou_objetivo_midia() -> None:
    ambiente, id_campanha = ambiente_aberto()
    resumo = ambiente.briefings.adicionar_objetivo_marketing(
        id_campanha,
        entrada_marketing(),
    )
    nomes = {campo.name for campo in fields(resumo.objetivos_marketing[0])}

    assert "peso" not in nomes
    assert "objetivo_midia" not in nomes
    assert all(
        not type(valor).__module__.startswith("mediad_planner.domain")
        for valor in resumo.objetivos_marketing
    )
