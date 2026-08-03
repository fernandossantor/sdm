from dataclasses import FrozenInstanceError
from uuid import UUID

import pytest

from mediad_planner.domain.briefing.objetivos_declarados import (
    DefinicaoObjetivoDeclarado,
    DimensaoCompostoMarketing,
    ObjetivoComunicacaoDeclarado,
    ObjetivoMarketingDeclarado,
    ObjetivosDeclarados,
    listar_dimensoes_composto_marketing,
    listar_objetivos_comunicacao_iniciais,
    listar_objetivos_marketing_iniciais,
)


def marketing(
    numero: int = 1,
    codigo: str | None = "marketing_crescimento",
    objetivo: str = "Crescimento",
    **mudancas: object,
) -> ObjetivoMarketingDeclarado:
    dados = {
        "id_objetivo": UUID(int=numero),
        "codigo_objetivo": codigo,
        "objetivo": objetivo,
        "dimensoes_composto": (),
        "prioridade_declarada": 3,
        "intensidade_declarada": 4,
        "justificativa": None,
    }
    dados.update(mudancas)
    return ObjetivoMarketingDeclarado(**dados)


def comunicacao(
    numero: int = 10,
    relacionados: tuple[UUID, ...] = (),
    codigo: str | None = "comunicacao_notoriedade",
    objetivo: str = "Notoriedade",
) -> ObjetivoComunicacaoDeclarado:
    return ObjetivoComunicacaoDeclarado(
        id_objetivo=UUID(int=numero),
        codigo_objetivo=codigo,
        objetivo=objetivo,
        ids_objetivos_marketing_relacionados=relacionados,
        prioridade_declarada=2,
        intensidade_declarada=5,
        justificativa="Justificativa",
    )


def test_catalogos_possuem_ordem_e_codigos_globais_unicos() -> None:
    marketing_catalogo = listar_objetivos_marketing_iniciais()
    comunicacao_catalogo = listar_objetivos_comunicacao_iniciais()

    assert tuple(item.rotulo for item in marketing_catalogo) == (
        "Branding",
        "Posicionamento",
        "Segmentação",
        "Diferenciação",
        "Crescimento",
        "Participação de mercado",
        "Fidelização",
        "Penetração",
        "Desenvolvimento de produto",
        "Diversificação",
    )
    assert len(comunicacao_catalogo) == 17
    assert comunicacao_catalogo[0].rotulo == "Notoriedade"
    assert comunicacao_catalogo[-1].rotulo == "Defesa da marca"
    codigos = tuple(
        item.codigo for item in marketing_catalogo + comunicacao_catalogo
    )
    assert len(codigos) == len(set(codigos)) == 27
    assert all(item.descricao for item in marketing_catalogo + comunicacao_catalogo)


@pytest.mark.parametrize(
    "codigo",
    (
        "Objetivo",
        "objetívo",
        "objetivo invalido",
        " objetivo_valido",
        "_objetivo",
        "objetivo_",
    ),
)
def test_definicao_rejeita_codigo_invalido(codigo: str) -> None:
    with pytest.raises(ValueError, match="codigo"):
        DefinicaoObjetivoDeclarado(codigo, "Rótulo", "Descrição")


def test_definicao_normaliza_e_e_imutavel() -> None:
    definicao = DefinicaoObjetivoDeclarado(
        "objetivo_1",
        " Rótulo ",
        " Descrição ",
    )

    assert definicao.rotulo == "Rótulo"
    assert definicao.descricao == "Descrição"
    with pytest.raises(FrozenInstanceError):
        definicao.codigo = "outro"


def test_dimensoes_composto_sao_exatas_e_diferenciam_praca() -> None:
    definicoes = listar_dimensoes_composto_marketing()

    assert tuple(item.codigo for item in definicoes) == tuple(
        DimensaoCompostoMarketing
    )
    assert tuple(item.rotulo for item in definicoes) == (
        "Produto",
        "Preço",
        "Praça (distribuição)",
        "Promoção",
    )
    assert "praça territorial" in definicoes[2].descricao
    assert isinstance(definicoes, tuple)


@pytest.mark.parametrize("campo", ("prioridade_declarada", "intensidade_declarada"))
@pytest.mark.parametrize("valor", (0, -1, 6, True, 1.0, "1"))
def test_escalas_rejeitam_valores_invalidos(campo: str, valor: object) -> None:
    with pytest.raises(ValueError, match=campo):
        marketing(**{campo: valor})


@pytest.mark.parametrize("valor", (1, 2, 3, 4, 5))
def test_escalas_aceitam_intervalo_completo(valor: int) -> None:
    criado = marketing(
        prioridade_declarada=valor,
        intensidade_declarada=valor,
    )

    assert criado.prioridade_declarada == valor
    assert criado.intensidade_declarada == valor


def test_objetivos_normalizam_colecoes_e_justificativa() -> None:
    objetivo = marketing(
        dimensoes_composto=[
            DimensaoCompostoMarketing.PRODUTO,
            DimensaoCompostoMarketing.PRACA,
        ],
        justificativa=" ",
    )
    relacionado = comunicacao(relacionados=[objetivo.id_objetivo])

    assert objetivo.dimensoes_composto == (
        DimensaoCompostoMarketing.PRODUTO,
        DimensaoCompostoMarketing.PRACA,
    )
    assert objetivo.justificativa is None
    assert relacionado.ids_objetivos_marketing_relacionados == (
        objetivo.id_objetivo,
    )
    with pytest.raises(ValueError, match="duplicatas"):
        marketing(
            dimensoes_composto=[
                DimensaoCompostoMarketing.PRODUTO,
                DimensaoCompostoMarketing.PRODUTO,
            ]
        )
    with pytest.raises(ValueError, match="duplicatas"):
        comunicacao(relacionados=(objetivo.id_objetivo,) * 2)


def test_colecao_preserva_ordem_vinculos_e_operacoes_imutaveis() -> None:
    primeiro = marketing()
    segundo = marketing(2, None, "Expansão regional")
    inicial = ObjetivosDeclarados([], [])
    com_marketing = inicial.adicionar_marketing(primeiro).adicionar_marketing(
        segundo
    )
    objetivo_comunicacao = comunicacao(relacionados=(primeiro.id_objetivo,))
    completo = com_marketing.adicionar_comunicacao(objetivo_comunicacao)

    assert inicial.marketing == ()
    assert completo.marketing == (primeiro, segundo)
    assert completo.comunicacao == (objetivo_comunicacao,)
    with pytest.raises(ValueError, match="vinculado"):
        completo.remover_marketing(primeiro.id_objetivo)
    sem_comunicacao = completo.remover_comunicacao(
        objetivo_comunicacao.id_objetivo
    )
    assert sem_comunicacao.remover_marketing(primeiro.id_objetivo).marketing == (
        segundo,
    )
    with pytest.raises(LookupError):
        completo.remover_comunicacao(UUID(int=999))


def test_colecao_rejeita_duplicidades_e_vinculo_inexistente() -> None:
    primeiro = marketing()

    with pytest.raises(ValueError, match="IDs"):
        ObjetivosDeclarados((primeiro,), (comunicacao(1),))
    with pytest.raises(ValueError, match="Código"):
        ObjetivosDeclarados((primeiro, marketing(2)), ())
    with pytest.raises(ValueError, match="personalizado"):
        ObjetivosDeclarados(
            (
                marketing(2, None, "Expansão"),
                marketing(3, None, " expansão "),
            ),
            (),
        )
    with pytest.raises(ValueError, match="não existe"):
        ObjetivosDeclarados((), (comunicacao(relacionados=(UUID(int=99),)),))


def test_colecao_rejeita_objetivos_em_tipo_incorreto_antes_de_atributos() -> None:
    objetivo_marketing = marketing()
    objetivo_comunicacao = comunicacao()

    with pytest.raises(TypeError, match="marketing contém objetivo de tipo inválido"):
        ObjetivosDeclarados((objetivo_comunicacao,), ())
    with pytest.raises(
        TypeError,
        match="comunicacao contém objetivo de tipo inválido",
    ):
        ObjetivosDeclarados((), (objetivo_marketing,))

    assert ObjetivosDeclarados(
        (objetivo_marketing,),
        (comunicacao(relacionados=(objetivo_marketing.id_objetivo,)),),
    ).marketing == (objetivo_marketing,)
