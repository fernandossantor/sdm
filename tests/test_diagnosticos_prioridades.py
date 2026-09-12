from dataclasses import asdict, replace
from uuid import UUID

import pytest

from mediad_planner.application.dto.condicoes_declaradas import SalvarPrioridadeEntrada
from mediad_planner.domain.briefing.condicoes_declaradas import PrioridadeContextual, TipoEntidadePrioridade
from mediad_planner.domain.briefing.jornada import CategoriaEtapaJornada, EtapaJornadaDeclarada, JornadaDeclarada
from mediad_planner.domain.briefing.revisao import avaliar_briefing
from test_aplicabilidade_jornada import _dominio
from test_jornada import _com_publico, _jornada, _etapa
from test_publicos import _preparar


def _contextuais(valores, justificativas):
    original = _dominio()
    estrutura = original.estrutura_territorial_populacional
    alvos = (
        (TipoEntidadePrioridade.PRACA, estrutura.pracas[0].id_praca),
        (TipoEntidadePrioridade.SEGMENTO, estrutura.segmentos[0].id_segmento),
    )
    return replace(original, prioridades_contextuais=tuple(
        PrioridadeContextual(UUID(int=90 + indice), *alvos[indice], valor, None, justificativas[indice])
        for indice, valor in enumerate(valores)
    ))


@pytest.mark.parametrize("valores,justificativas,iguais,sem_justificativa", (
    ((), (), False, 0),
    ((5,), (None,), False, 0),
    ((3, 4), (None, None), False, 0),
    ((3, 3), (None, None), True, 0),
    ((5, 5), (None, None), True, 2),
    ((5, 5), ("Razão declarada", None), True, 1),
    ((5, 5), ("Razão declarada", "Outra razão"), True, 0),
    ((5, 5), (" ", "Outra razão"), True, 1),
))
def test_prioridades_contextuais_explica_igualdade_e_identifica_justificativas_ausentes(
    valores, justificativas, iguais, sem_justificativa,
):
    original = _contextuais(valores, justificativas)
    antes = asdict(original)
    alertas = [item for item in avaliar_briefing(original) if item.referencia_normativa == "02_BRIEFING.md § 13.3"]
    assert sum("mesmo valor" in item.mensagem for item in alertas) == int(iguais)
    lacunas = [item for item in alertas if "sem justificativa" in item.mensagem]
    assert len(lacunas) == sem_justificativa
    for alerta in lacunas:
        prioridade = next(item for item in original.prioridades_contextuais if item.id_prioridade == alerta.id_entidade)
        assert prioridade.justificativa is None
        assert "Praça" in alerta.mensagem or "Segmento" in alerta.mensagem
    assert asdict(original) == antes


def _etapa_dominio(indice, prioridade, ordem):
    return EtapaJornadaDeclarada(
        UUID(int=100 + indice), tuple(CategoriaEtapaJornada)[indice], ordem,
        True, None, None, prioridade, (UUID(int=72),), (), None, None, None,
    )


@pytest.mark.parametrize("prioridades,ordens,esperado", (
    ((), (), False),
    ((5,), (None,), False),
    ((None, None), (None, None), False),
    ((4, 5), (None, None), False),
    ((5, 5), (None, None), True),
    ((5, 5), (1, None), True),
    ((5, 5), (1, 2), False),
))
def test_ordenacao_de_maximas_e_avaliada_por_jornada(prioridades, ordens, esperado):
    etapas = tuple(_etapa_dominio(indice, valor, ordens[indice]) for indice, valor in enumerate(prioridades))
    jornada = JornadaDeclarada(UUID(int=150), "Jornada testada", None, (UUID(int=72),), None, True, etapas)
    original = replace(_dominio(), jornadas=(jornada,))
    antes = asdict(original)
    alertas = [item for item in avaliar_briefing(original) if item.id_entidade == jornada.id_jornada]
    assert bool(alertas) is esperado
    if esperado:
        assert len(alertas) == 1
        assert "Jornada testada" in alertas[0].mensagem
        assert "sem ordenação explícita" in alertas[0].mensagem
        assert alertas[0].referencia_normativa == "02_BRIEFING.md § 10.4"
    assert asdict(original) == antes


def test_nao_combina_prioridades_de_jornadas_diferentes():
    jornadas = tuple(
        JornadaDeclarada(UUID(int=150 + indice), f"Jornada {indice}", None, (UUID(int=72),), None, True, (_etapa_dominio(indice, 5, None),))
        for indice in range(2)
    )
    alertas = avaliar_briefing(replace(_dominio(), jornadas=jornadas))
    assert not any("sem ordenação" in item.mensagem for item in alertas)


def test_aplicacao_recalcula_prioridades_apos_justificar_editar_e_remover():
    ambiente, campanha, _, pracas = _preparar()
    for praca in pracas:
        resumo = ambiente.briefings.salvar_prioridade(campanha, SalvarPrioridadeEntrada("PRACA", praca, 5, None, None))
    assert sum("sem justificativa" in item.mensagem for item in resumo.apontamentos_revisao) == 2
    primeiro, segundo = resumo.prioridades_contextuais
    resumo = ambiente.briefings.salvar_prioridade(campanha, SalvarPrioridadeEntrada("PRACA", pracas[0], 5, None, "Lançamento"), primeiro.id_prioridade)
    assert sum("sem justificativa" in item.mensagem for item in resumo.apontamentos_revisao) == 1
    resumo = ambiente.briefings.salvar_prioridade(campanha, SalvarPrioridadeEntrada("PRACA", pracas[1], 4, None, None), segundo.id_prioridade)
    assert not any(item.referencia_normativa.endswith("13.3") for item in resumo.apontamentos_revisao)
    resumo = ambiente.briefings.remover_prioridade(campanha, segundo.id_prioridade)
    assert not any(item.referencia_normativa.endswith("13.3") for item in resumo.apontamentos_revisao)


def test_aplicacao_recalcula_ordenacao_apos_edicao_e_preserva_demais_alertas():
    ambiente, campanha, publico = _com_publico()
    resumo = ambiente.briefings.adicionar_jornada(campanha, _jornada(publico))
    jornada = resumo.jornadas[0]
    for categoria in ("CONSIDERACAO", "DECISAO"):
        resumo = ambiente.briefings.adicionar_etapa_jornada(campanha, jornada.id_jornada, _etapa(publico, categoria=categoria, ordem=None))
    assert any(item.id_entidade == jornada.id_jornada for item in resumo.apontamentos_revisao)
    for ordem, etapa in enumerate(resumo.jornadas[0].etapas, 1):
        resumo = ambiente.briefings.editar_etapa_jornada(campanha, jornada.id_jornada, etapa.id_etapa, _etapa(publico, categoria=etapa.categoria, ordem=ordem))
    assert not any(item.id_entidade == jornada.id_jornada for item in resumo.apontamentos_revisao)
    assert sum("sem relação com objetivo de comunicação" in item.mensagem for item in resumo.apontamentos_revisao) == 2


def _com_prioridades(grupo, valores, justificativas):
    from mediad_planner.domain.briefing.objetivos_declarados import (
        ObjetivoMarketingDeclarado, ObjetivoComunicacaoDeclarado, ObjetivosDeclarados,
    )
    original = _dominio()
    if grupo == "publicos":
        estrutura = original.estrutura_territorial_populacional
        return replace(original, estrutura_territorial_populacional=replace(
            estrutura, segmentos=tuple(
                replace(estrutura.segmentos[0], id_segmento=UUID(int=300 + i), definicao=f"Segmento {i}")
                for i in range(max(1, len(valores)))
            ), publicos=tuple(
                replace(estrutura.publicos[0], id_publico=UUID(int=200 + i),
                        ids_segmentos_origem=(UUID(int=300 + i),),
                        nome=f"Público {i}", prioridade=valor, justificativa=justificativas[i])
                for i, valor in enumerate(valores)
            ),
        ))
    classe = ObjetivoMarketingDeclarado if grupo == "marketing" else ObjetivoComunicacaoDeclarado
    itens = tuple(classe(UUID(int=200 + i), None, f"Objetivo {i}", (), valor, 3, justificativas[i])
                  for i, valor in enumerate(valores))
    return replace(original, objetivos_declarados=ObjetivosDeclarados(
        itens if grupo == "marketing" else (), itens if grupo == "comunicacao" else (),
    ))


@pytest.mark.parametrize("grupo", ("marketing", "comunicacao", "publicos"))
@pytest.mark.parametrize("valores,justificativas,iguais,lacunas", (
    ((), (), False, ()),
    ((5,), (None,), False, ()),
    ((3, 4), (None, None), False, ()),
    ((3, 3), (None, None), True, ()),
    ((4, 4), (None, None), True, ()),
    ((5, 5), (None, None), True, (0, 1)),
    ((5, 5), ("Motivo", None), True, (1,)),
    ((5, 5), ("Motivo", "Outro"), True, ()),
    ((5, 5, 3), (" ", "Motivo", None), False, (0,)),
))
def test_prioridades_por_conjunto_preservam_declaracoes(grupo, valores, justificativas, iguais, lacunas):
    original = _com_prioridades(grupo, valores, justificativas)
    antes = asdict(original)
    alertas = [a for a in avaliar_briefing(original) if a.referencia_normativa.endswith("13.3")]
    assert sum("mesmo valor" in a.mensagem for a in alertas) == int(iguais)
    assert {a.id_entidade for a in alertas if "sem justificativa" in a.mensagem} == {
        UUID(int=200 + i) for i in lacunas
    }
    subetapa = "Segmentos e públicos" if grupo == "publicos" else "Objetivos declarados"
    assert all(a.subetapa == subetapa for a in alertas)
    assert asdict(original) == antes


@pytest.mark.parametrize("valores,lacunas", (((None, None), 0), ((5, None), 0), ((5, 5, None), 2)))
def test_prioridades_ausentes_nao_sao_iguais_nem_ocultam_maximas(valores, lacunas):
    alertas = avaliar_briefing(_com_prioridades("publicos", valores, (None,) * len(valores)))
    assert not any("mesmo valor" in a.mensagem for a in alertas)
    assert sum("sem justificativa" in a.mensagem for a in alertas) == lacunas
    assert sum("prioridade não informada" in a.mensagem for a in alertas) == valores.count(None)


def test_nao_combina_marketing_comunicacao_e_publicos():
    marketing = _com_prioridades("marketing", (5,), (None,))
    comunicacao = _com_prioridades("comunicacao", (5,), (None,))
    publico = _com_prioridades("publicos", (5,), (None,))
    original = replace(marketing,
        objetivos_declarados=replace(marketing.objetivos_declarados,
                                    comunicacao=(replace(comunicacao.objetivos_declarados.comunicacao[0], id_objetivo=UUID(int=500)),)),
        estrutura_territorial_populacional=publico.estrutura_territorial_populacional)
    assert not any(a.referencia_normativa.endswith("13.3") for a in avaliar_briefing(original))


def test_publicos_recalculam_apos_justificativa_prioridade_e_remocao():
    from test_publicos import _entrada
    ambiente, campanha, segmentos, pracas = _preparar()
    for i in range(2):
        resumo = ambiente.briefings.adicionar_publico(campanha, _entrada(
            (segmentos[i],), (pracas[i],), justificativa=None))
    primeiro, segundo = resumo.publicos
    assert sum("sem justificativa" in a.mensagem for a in resumo.apontamentos_revisao) == 2
    resumo = ambiente.briefings.editar_publico(campanha, primeiro.id_publico,
        _entrada((segmentos[0],), (pracas[0],), justificativa="Motivo"))
    assert [a.id_entidade for a in resumo.apontamentos_revisao if "sem justificativa" in a.mensagem] == [segundo.id_publico]
    resumo = ambiente.briefings.editar_publico(campanha, segundo.id_publico,
        _entrada((segmentos[1],), (pracas[1],), prioridade=4, justificativa=None))
    assert not any(a.referencia_normativa.endswith("13.3") for a in resumo.apontamentos_revisao)
    resumo = ambiente.briefings.remover_publico(campanha, segundo.id_publico)
    assert not any(a.referencia_normativa.endswith("13.3") for a in resumo.apontamentos_revisao)
