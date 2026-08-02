from dataclasses import FrozenInstanceError

import pytest

from src.engines.traducao_estrategica.mensurabilidade import (
    EstadoMensurabilidade,
    ObjetivoDeclarado,
    classificar_mensurabilidade,
)


def _objetivo_direto(**alteracoes):
    dados = {
        "codigo": "mkt_aumento_vendas",
        "texto_original": "Aumentar vendas.",
        "objeto_da_mudanca": "vendas",
        "publico": "público prioritário",
        "praca": "Campinas (SP)",
        "direcao": "aumentar",
        "indicador": "vendas",
        "unidade_ou_escala": "quantidade",
        "linha_de_base": 120,
        "meta_ou_intensidade": 150,
        "horizonte_temporal": "2026-09-01/2026-10-31",
        "fonte": "sistema comercial declarado",
        "confianca": "MEDIA",
        "forma_mensuracao": "METRICA_DIRETA",
    }
    dados.update(alteracoes)
    return ObjetivoDeclarado(**dados)


def test_objetivo_completamente_operacionalizado():
    resultado = classificar_mensurabilidade(_objetivo_direto())

    assert resultado.estado is EstadoMensurabilidade.OPERACIONALIZADO
    assert resultado.dados_ausentes == ()
    assert resultado.possibilidade_de_pontuacao is True
    assert resultado.alerta is None


def test_objetivo_com_linha_de_base_ausente():
    resultado = classificar_mensurabilidade(_objetivo_direto(linha_de_base=None))

    assert resultado.estado is EstadoMensurabilidade.OPERACIONALIZAVEL_COM_DADOS_PENDENTES
    assert resultado.dados_ausentes == ("linha_de_base",)
    assert resultado.possibilidade_de_pontuacao is True
    assert resultado.alerta is not None


def test_objetivo_mensuravel_por_proxy():
    objetivo = _objetivo_direto(
        indicador="visitas qualificadas",
        unidade_ou_escala="quantidade",
        linha_de_base=None,
        meta_ou_intensidade=None,
        forma_mensuracao="PROXY_DECLARADO",
        proxy_de="intenção de solicitar proposta",
        limitacao_do_proxy="Visita não equivale a intenção nem a venda.",
    )

    resultado = classificar_mensurabilidade(objetivo)

    assert resultado.estado is EstadoMensurabilidade.OPERACIONALIZAVEL_POR_PROXY
    assert "proxy_de" in resultado.evidencias
    assert resultado.possibilidade_de_pontuacao is True


def test_objetivo_qualitativo_estruturado():
    objetivo = _objetivo_direto(
        indicador="percepção de clareza",
        unidade_ou_escala="muito baixa a muito alta",
        linha_de_base=None,
        meta_ou_intensidade="alta",
        forma_mensuracao="ESCALA_ORDINAL_ESTRUTURADA",
    )

    resultado = classificar_mensurabilidade(objetivo)

    assert resultado.estado is EstadoMensurabilidade.QUALITATIVO_ESTRUTURADO
    assert resultado.possibilidade_de_pontuacao is True


def test_objetivo_subjetivo_nao_operacionalizado():
    objetivo = ObjetivoDeclarado(
        codigo="subjetivo",
        texto_original="Melhorar bastante a imagem da marca.",
    )

    resultado = classificar_mensurabilidade(objetivo)

    assert resultado.estado is EstadoMensurabilidade.NAO_OPERACIONALIZADO
    assert resultado.possibilidade_de_pontuacao is False
    assert "indicador" in resultado.dados_ausentes
    assert resultado.alerta is not None


def test_objetivo_com_valor_zero_valido():
    resultado = classificar_mensurabilidade(
        _objetivo_direto(linha_de_base=0, meta_ou_intensidade=10)
    )

    assert resultado.estado is EstadoMensurabilidade.OPERACIONALIZADO
    assert "linha_de_base" in resultado.dados_presentes
    assert "linha_de_base" not in resultado.dados_ausentes


def test_entrada_e_resultado_sao_imutaveis():
    objetivo = _objetivo_direto()
    resultado = classificar_mensurabilidade(objetivo)

    with pytest.raises(FrozenInstanceError):
        objetivo.indicador = "outro"
    with pytest.raises(FrozenInstanceError):
        resultado.estado = EstadoMensurabilidade.NAO_OPERACIONALIZADO
