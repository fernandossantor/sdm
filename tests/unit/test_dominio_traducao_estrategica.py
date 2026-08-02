from dataclasses import FrozenInstanceError
from datetime import date
from decimal import Decimal

import pytest

from src.domain.briefing import (
    Briefing,
    DadoPendente,
    IndicadorDisponivel,
    Publico,
    Restricao,
    Segmento,
    TensaoEstrategica,
)
from src.domain.campanha import (
    Campanha,
    IdentificacaoCampanha,
    NaturezaLimiteVerba,
    Periodo,
    Praca,
    Verba,
)
from src.domain.common import NaturezaValor, ValorComOrigem, para_primitivos
from src.domain.contrato_estrategico import (
    ContratoEstrategico,
    EstadoContratoEstrategico,
)
from src.domain.objetivos import (
    ObjetivoComunicacaoCandidato,
    ObjetivoMarketing,
    Prioridade,
)


def _ausente():
    return ValorComOrigem(valor=None, natureza=NaturezaValor.NAO_DISPONIVEL)


def _briefing_canonico():
    praca = Praca("Campinas (SP)", "município", _ausente())
    return Briefing(
        campanha=Campanha(
            IdentificacaoCampanha(
                id="campanha-canonica-lume-2026",
                nome="Lume Casa — Primavera 2026",
                marca="Lume Casa",
                produto_ou_servico="assinatura de energia solar residencial",
            )
        ),
        situacao_marca_mercado=(
            "Notoriedade alta, baixa conclusão de proposta e receio sobre retorno."
        ),
        objetivos_marketing=(
            ObjetivoMarketing("aumento de vendas", 1, Prioridade.MUITO_ALTA),
            ObjetivoMarketing("crescimento", 2, Prioridade.ALTA),
        ),
        objetivos_comunicacao_candidatos=(
            ObjetivoComunicacaoCandidato("intenção"),
            ObjetivoComunicacaoCandidato("redução de incerteza"),
            ObjetivoComunicacaoCandidato("notoriedade"),
        ),
        publico_prioritario=Publico(
            "Responsáveis pela decisão de energia residencial",
            "Pessoas de 30 a 55 anos que pesquisaram redução da conta.",
            "Campinas (SP)",
            Prioridade.MUITO_ALTA,
            _ausente(),
        ),
        segmento_secundario=Segmento(
            "Interessados sem pesquisa recente",
            "Interessados em sustentabilidade sem pesquisa recente.",
            "Campinas (SP)",
            Prioridade.MEDIA,
            _ausente(),
        ),
        praca=praca,
        periodo=Periodo(date(2026, 9, 1), date(2026, 10, 31)),
        verba=Verba(
            ValorComOrigem(Decimal("300000"), NaturezaValor.INFORMADO),
            "BRL",
            NaturezaLimiteVerba.RIGIDO,
            _ausente(),
        ),
        prioridade=Prioridade.MUITO_ALTA,
        restricao=Restricao(
            "orçamentária",
            "A verba total não pode ultrapassar BRL 300.000.",
            "campanha",
            Prioridade.MUITO_ALTA,
            Prioridade.MUITO_ALTA,
            "anunciante",
            "Teto financeiro aprovado para o período.",
        ),
        tensao_estrategica=TensaoEstrategica(
            "Dois objetivos disputam a verba rígida.",
            ("aumento de vendas", "crescimento", "verba rígida"),
        ),
        indicadores_disponiveis=(
            IndicadorDisponivel(
                "notoriedade auxiliada",
                ValorComOrigem(Decimal("78"), NaturezaValor.INFORMADO),
                "percentual",
                "Responsáveis pela decisão de energia residencial",
                "Campinas (SP)",
                "2026-06",
                "Pesquisa fictícia Lume Tracking",
                "levantamento amostral declarado pelo anunciante",
                "MEDIA",
            ),
            IndicadorDisponivel(
                "taxa de conclusão do pedido de proposta",
                ValorComOrigem(Decimal("1.1"), NaturezaValor.INFORMADO),
                "percentual",
                "visitantes da página de proposta",
                "Campinas (SP)",
                "2026-06",
                "Analytics fictício Lume Casa",
                "pedidos concluídos divididos por visitas à página",
                "MEDIA",
            ),
        ),
        dados_ausentes=(
            DadoPendente("meta_de_vendas"),
            DadoPendente("linha_de_base_de_vendas"),
            DadoPendente("indicador_de_intencao"),
        ),
    )


def test_cria_briefing_canonico_e_contrato_estrategico_vazio():
    briefing = _briefing_canonico()
    contrato = ContratoEstrategico.vazio(
        id_campanha=briefing.campanha.identificacao.id,
        versao="1",
    )

    assert len(briefing.objetivos_marketing) == 2
    assert len(briefing.objetivos_comunicacao_candidatos) == 3
    assert contrato.estado is EstadoContratoEstrategico.INSUFICIENTE
    assert contrato.objetivos_midia == ()


@pytest.mark.parametrize(
    "construtor",
    [
        lambda: IdentificacaoCampanha("", "Campanha", "Marca", "Produto"),
        lambda: Periodo(date(2026, 10, 31), date(2026, 9, 1)),
        lambda: ObjetivoMarketing("crescimento", 0, Prioridade.ALTA),
        lambda: TensaoEstrategica("Tensão", ("um elemento",)),
        lambda: ValorComOrigem(None, NaturezaValor.INFORMADO),
        lambda: ValorComOrigem(Decimal("1"), NaturezaValor.NAO_DISPONIVEL),
    ],
)
def test_rejeita_dados_estruturalmente_invalidos(construtor):
    with pytest.raises(ValueError):
        construtor()


def test_ausencia_e_diferente_de_zero():
    briefing = _briefing_canonico()

    assert briefing.verba.margem_de_flexibilidade.valor is None
    assert briefing.verba.margem_de_flexibilidade.valor != 0
    assert all(item.valor is None for item in briefing.dados_ausentes)


def test_modelos_e_colecoes_sao_imutaveis():
    briefing = _briefing_canonico()

    with pytest.raises(FrozenInstanceError):
        briefing.prioridade = Prioridade.BAIXA
    with pytest.raises(TypeError):
        briefing.objetivos_marketing[0] = ObjetivoMarketing(
            "crescimento", 1, Prioridade.BAIXA
        )


def test_serializacao_e_previsivel():
    briefing = _briefing_canonico()
    serializado = para_primitivos(briefing)

    assert serializado["periodo"] == {
        "data_inicial": "2026-09-01",
        "data_final": "2026-10-31",
    }
    assert serializado["verba"]["valor_total"] == {
        "valor": "300000",
        "natureza": "INFORMADO",
    }
    assert serializado["dados_ausentes"][0]["valor"] is None
    assert serializado["objetivos_marketing"][0]["prioridade"] == "muito alta"
