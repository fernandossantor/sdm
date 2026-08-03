from dataclasses import FrozenInstanceError
from decimal import Decimal
from uuid import UUID

import pytest

from mediad_planner.domain.briefing.situacao_mercadologica import (
    EscopoSituacaoMercadologica,
    DefinicaoAspectoSituacao,
    NaturezaRegistroSituacao,
    RegistroSituacaoMercadologica,
    SituacaoMercadologicaCompetitiva,
    listar_aspectos_iniciais,
)


def registro(**alteracoes: object) -> RegistroSituacaoMercadologica:
    dados = {
        "id_registro": UUID(int=1),
        "escopo": EscopoSituacaoMercadologica.ANUNCIANTE,
        "codigo_aspecto": "participacao_mercado",
        "aspecto": "Participação de mercado",
        "entidade_referencia": None,
        "natureza": NaturezaRegistroSituacao.QUANTITATIVO,
        "valor_quantitativo": Decimal("-2.75"),
        "unidade": "%",
        "valor_qualitativo": None,
        "fonte": " Fonte ",
        "periodo_referencia": " 2026 ",
        "observacao": " ",
    }
    dados.update(alteracoes)
    return RegistroSituacaoMercadologica(**dados)


def test_enums_possuem_composicao_exata() -> None:
    assert tuple(item.value for item in EscopoSituacaoMercadologica) == (
        "ANUNCIANTE", "MERCADO", "CATEGORIA", "CONCORRENCIA",
    )
    assert tuple(item.value for item in NaturezaRegistroSituacao) == (
        "QUANTITATIVO", "QUALITATIVO",
    )


def test_aspectos_iniciais_possuem_taxonomia_revisada() -> None:
    aspectos = listar_aspectos_iniciais(EscopoSituacaoMercadologica.ANUNCIANTE)
    rotulos = tuple(item.rotulo for item in aspectos)

    assert rotulos == (
        "Posição competitiva", "Participação de mercado", "Penetração",
        "Notoriedade", "Lembrança", "Imagem percebida", "Preferência",
        "Fidelização", "Desempenho comercial", "Amplitude da distribuição",
        "Presença geográfica", "Estágio do ciclo de vida",
        "Tendência de desempenho",
    )
    for escopo in EscopoSituacaoMercadologica:
        definicoes = listar_aspectos_iniciais(escopo)
        assert isinstance(definicoes, tuple)
        assert "Estabilidade" not in tuple(item.rotulo for item in definicoes)
        assert "Retração" not in tuple(item.rotulo for item in definicoes)

    esperados = {
        EscopoSituacaoMercadologica.MERCADO: (
            "Tamanho do mercado", "Taxa de crescimento do mercado",
            "Sazonalidade", "Grau de concentração", "Estágio de maturidade",
            "Tendência de desempenho do mercado", "Intensidade competitiva",
            "Mudanças relevantes no mercado",
        ),
        EscopoSituacaoMercadologica.CATEGORIA: (
            "Tamanho da categoria", "Taxa de crescimento da categoria",
            "Sazonalidade", "Grau de concentração", "Estágio de maturidade",
            "Tendência de desempenho da categoria", "Intensidade competitiva",
            "Mudanças relevantes na categoria",
        ),
        EscopoSituacaoMercadologica.CONCORRENCIA: (
            "Posição competitiva", "Participação de mercado do concorrente",
            "Intensidade competitiva", "Presença territorial",
            "Presença de comunicação", "Investimento em mídia",
            "Share of Voice", "Vantagens percebidas", "Desvantagens percebidas",
            "Tendência de desempenho do concorrente",
        ),
    }
    for escopo, rotulos_esperados in esperados.items():
        assert tuple(
            item.rotulo for item in listar_aspectos_iniciais(escopo)
        ) == rotulos_esperados


def test_sugestoes_de_unidades_chegam_as_definicoes() -> None:
    aspectos = listar_aspectos_iniciais(EscopoSituacaoMercadologica.ANUNCIANTE)
    por_rotulo = {item.rotulo: item for item in aspectos}

    assert por_rotulo["Participação de mercado"].unidades_sugeridas == ("%",)
    assert por_rotulo["Desempenho comercial"].unidades_sugeridas == (
        "R$", "unidades", "%", "índice",
    )


def test_aspecto_personalizado_e_normalizacao() -> None:
    item = registro(aspecto=" Novo aspecto ", fonte=" ")

    assert item.aspecto == "Novo aspecto"
    assert item.fonte is None
    assert item.periodo_referencia == "2026"
    assert item.observacao is None
    with pytest.raises(ValueError, match="aspecto"):
        registro(aspecto=" ")
    with pytest.raises(TypeError, match="UUID"):
        registro(id_registro="1")


def test_concorrencia_exige_referencia_e_outros_escopos_rejeitam() -> None:
    with pytest.raises(ValueError, match="Concorrente"):
        registro(escopo=EscopoSituacaoMercadologica.CONCORRENCIA)
    concorrente = registro(
        escopo=EscopoSituacaoMercadologica.CONCORRENCIA,
        entidade_referencia=" Concorrente Alfa ",
    )
    assert concorrente.entidade_referencia == "Concorrente Alfa"
    with pytest.raises(ValueError, match="Concorrência"):
        registro(entidade_referencia="Inadequada")


def test_regras_quantitativas() -> None:
    assert registro().valor_quantitativo == Decimal("-2.75")
    for valor in (Decimal("NaN"), Decimal("Infinity"), Decimal("-Infinity")):
        with pytest.raises(ValueError, match="finito"):
            registro(valor_quantitativo=valor)
    with pytest.raises(ValueError, match="valor_quantitativo"):
        registro(valor_quantitativo=None)
    with pytest.raises(ValueError, match="unidade"):
        registro(unidade=" ")
    with pytest.raises(ValueError, match="valor_qualitativo"):
        registro(valor_qualitativo="texto")


def test_regras_qualitativas() -> None:
    qualitativo = registro(
        natureza=NaturezaRegistroSituacao.QUALITATIVO,
        valor_quantitativo=None,
        unidade=None,
        valor_qualitativo=" Condição informada ",
    )
    assert qualitativo.valor_qualitativo == "Condição informada"
    with pytest.raises(ValueError, match="valor_qualitativo"):
        registro(
            natureza=NaturezaRegistroSituacao.QUALITATIVO,
            valor_quantitativo=None,
            unidade=None,
            valor_qualitativo=" ",
        )
    with pytest.raises(ValueError, match="valor ou unidade"):
        registro(
            natureza=NaturezaRegistroSituacao.QUALITATIVO,
            valor_qualitativo="texto",
        )


def test_colecao_imutavel_preserva_ordem_adiciona_e_remove() -> None:
    primeiro = registro()
    segundo = registro(id_registro=UUID(int=2), aspecto="Imagem percebida")
    colecao = SituacaoMercadologicaCompetitiva([primeiro])
    ampliada = colecao.adicionar(segundo)

    assert colecao.registros == (primeiro,)
    assert ampliada.registros == (primeiro, segundo)
    assert ampliada.remover(primeiro.id_registro).registros == (segundo,)
    with pytest.raises(ValueError, match="duplicado"):
        ampliada.adicionar(primeiro)
    with pytest.raises(ValueError, match="duplicados"):
        SituacaoMercadologicaCompetitiva((primeiro, primeiro))
    with pytest.raises(LookupError):
        colecao.remover(UUID(int=99))
    with pytest.raises(FrozenInstanceError):
        primeiro.aspecto = "Outro"


def test_definicao_e_imutavel_e_normaliza_unidades() -> None:
    definicao = DefinicaoAspectoSituacao(
        codigo="participacao",
        rotulo=" Participação ",
        descricao=" Parcela observada. ",
        unidades_sugeridas=[" % ", "", "%", "pontos"],
    )

    assert definicao.rotulo == "Participação"
    assert definicao.descricao == "Parcela observada."
    assert definicao.unidades_sugeridas == ("%", "pontos")
    with pytest.raises(ValueError, match="rotulo"):
        DefinicaoAspectoSituacao("codigo", " ", "Descrição", ())
    with pytest.raises(ValueError, match="descricao"):
        DefinicaoAspectoSituacao("codigo", "Rótulo", " ", ())
    with pytest.raises(FrozenInstanceError):
        definicao.rotulo = "Outro"


@pytest.mark.parametrize(
    "codigo",
    (
        "ParticipacaoMercado",
        "participação_mercado",
        "participacao mercado",
        "_participacao",
        "participacao_",
        "",
    ),
)
def test_codigo_semantico_invalido_e_rejeitado(codigo: str) -> None:
    with pytest.raises(ValueError, match="codigo"):
        DefinicaoAspectoSituacao(codigo, "Rótulo", "Descrição", ())


def test_codigos_da_taxonomia_sao_unicos_e_obrigatorios() -> None:
    definicoes = tuple(
        aspecto
        for escopo in EscopoSituacaoMercadologica
        for aspecto in listar_aspectos_iniciais(escopo)
    )
    codigos = tuple(aspecto.codigo for aspecto in definicoes)

    assert all(codigos)
    assert len(codigos) == len(set(codigos))
    assert "participacao_mercado" in codigos
    assert "share_of_voice_concorrente" in codigos


def test_registro_preserva_codigo_canonico_ou_identidade_personalizada() -> None:
    canonico = registro()
    personalizado = registro(
        codigo_aspecto=None,
        aspecto="Índice de disponibilidade local",
    )

    assert canonico.codigo_aspecto == "participacao_mercado"
    assert canonico.aspecto == "Participação de mercado"
    assert personalizado.codigo_aspecto is None
    assert personalizado.aspecto == "Índice de disponibilidade local"
    with pytest.raises(ValueError, match="codigo"):
        registro(codigo_aspecto=" ")
