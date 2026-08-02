import pytest

from src.domain.objetivos import Prioridade
from src.engines.traducao_estrategica.matriz_comunicacao_midia import (
    ContextoDerivacaoMidia,
    ObjetivoComunicacaoPriorizado,
    derivar_objetivos_midia,
)


def _objetivo(codigo, *, forca=90, prioridade=Prioridade.MUITO_ALTA):
    return ObjetivoComunicacaoPriorizado(
        codigo=codigo,
        ordem=1,
        forca_contextual=forca,
        prioridade=prioridade,
        confianca=90,
    )


def _contexto(codigo, *, restricao_orcamentaria=20):
    return ContextoDerivacaoMidia(
        objetivos_comunicacao=(_objetivo(codigo),),
        publico="Responsáveis pela decisão de energia residencial",
        praca="Campinas (SP)",
        jornada="etapa pertinente ao objetivo",
        periodo="2026-09-01/2026-10-31",
        verba="BRL 300.000",
        intensidade_restricao_orcamentaria=restricao_orcamentaria,
        restricoes=("teto orçamentário rígido",),
    )


def test_notoriedade_prioriza_construcao_de_alcance_e_cobertura():
    resultado = derivar_objetivos_midia(_contexto("com_notoriedade"))

    assert tuple(item.codigo for item in resultado[:2]) == (
        "mid_construir_alcance",
        "mid_ampliar_cobertura",
    )
    assert resultado[0].indicadores_possiveis == ("Alcance da campanha",)
    assert resultado[1].indicadores_possiveis == ("cobertura da campanha",)
    assert resultado[0].rastreabilidade[0].versao_relacao == "1.0"


def test_lembranca_eleva_frequencia_e_continuidade():
    resultado = derivar_objetivos_midia(_contexto("com_lembranca"))

    assert tuple(item.codigo for item in resultado) == (
        "mid_gerar_frequencia",
        "mid_sustentar_continuidade",
    )
    assert resultado[0].prioridade == "muito alta"
    assert resultado[1].prioridade == "alta"


def test_resposta_direta_eleva_resposta_e_conversao_sem_prometer_resultado():
    resultado = derivar_objetivos_midia(_contexto("com_resposta"))

    assert tuple(item.codigo for item in resultado) == (
        "mid_favorecer_resposta",
        "mid_favorecer_conversao",
    )
    assert "taxa de resposta" in resultado[0].indicadores_possiveis
    assert "taxa de conversão" in resultado[1].indicadores_possiveis
    assert not any("viável" in alerta for item in resultado for alerta in item.alertas)


def test_restricao_orcamentaria_altera_intensidade_e_condicao_sem_inventar_viabilidade():
    sem_restricao = derivar_objetivos_midia(
        _contexto("com_notoriedade", restricao_orcamentaria=20)
    )[0]
    restrito = derivar_objetivos_midia(
        _contexto("com_notoriedade", restricao_orcamentaria=90)
    )[0]

    assert sem_restricao.intensidade == "muito alta"
    assert restrito.intensidade == "alta"
    assert restrito.condicao == "COMPENSAVEL"
    assert restrito.adequacao_contextual < sem_restricao.adequacao_contextual
    assert "viabilidade econômica não foi determinada" in restrito.alertas


def test_pesos_sao_normalizados_e_componentes_permanecem_reconstituiveis():
    resultado = derivar_objetivos_midia(_contexto("com_lembranca"))

    assert sum(item.peso for item in resultado) == pytest.approx(1.0, abs=1e-6)
    assert resultado[0].adequacao_contextual == round(
        sum(item.contribuicao for item in resultado[0].componentes), 2
    )
    assert resultado[0].versao_configuracao == "1.0"


def test_rejeita_contexto_sem_objetivo_de_comunicacao():
    contexto = ContextoDerivacaoMidia(
        objetivos_comunicacao=(),
        publico="público",
        praca="praça",
        jornada="jornada",
        periodo="período",
        verba="verba",
        intensidade_restricao_orcamentaria=0,
        restricoes=(),
    )

    with pytest.raises(ValueError, match="ao menos um objetivo"):
        derivar_objetivos_midia(contexto)
