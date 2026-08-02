from datetime import datetime, timezone
from uuid import uuid4

import pytest

from domain.briefing import BriefingInicial, ConteudoBriefing, EstadoBriefing
from domain.contracts import Confianca
from domain.traducao import traduzir_briefing
from engines.traducao_estrategica import CatalogoTraducaoInicial


def _briefing(*, comunicacao="notoriedade", notoriedade="baixa", fontes=True,
              prioridade="alta", restrita=False, motivo=None):
    restricoes = ({"categoria": "orçamentária"},) if restrita else ()
    return BriefingInicial(
        id=uuid4(), campanha_id=uuid4(), criado_por=uuid4(),
        criado_em=datetime(2026, 8, 2, tzinfo=timezone.utc),
        estado=EstadoBriefing.CONCLUIDO,
        motivo_ultima_alteracao=motivo,
        conteudo=ConteudoBriefing(
            situacao_mercadologica={
                "notoriedade": notoriedade,
                "intensidade_competitiva": "alta",
            },
            objetivos_marketing=(
                {"categoria": "Crescimento", "prioridade": prioridade},
            ),
            objetivos_comunicacao=(
                {"categoria": comunicacao, "prioridade": prioridade},
            ),
            publicos=({"nome": "Compradores"},),
            pracas=({"nome": "Brasil"},),
            jornadas=({"etapa": "consideração"},),
            jornada_aplicavel=True,
            periodo={"inicio": "2026-09-01", "fim": "2026-10-31"},
            verba={
                "natureza": "rígido" if restrita else "flexível",
                "valor_total": 100000,
            },
            restricoes=restricoes,
            sem_restricoes_declaradas=not restrita,
            fontes=({"descricao": "Pesquisa declarada"},) if fontes else (),
        ),
    )


def _traduzir(briefing, catalogo=None):
    return traduzir_briefing(
        briefing, contrato_id=uuid4(), criado_por=briefing.criado_por,
        criado_em=briefing.criado_em,
        catalogo=catalogo or CatalogoTraducaoInicial(),
    )


def _objetivo(contrato, categoria):
    return next(
        item for item in contrato.objetivos_midia_derivados
        if item.categoria == categoria
    )


def _relacao(contrato, destino):
    return next(
        item for item in contrato.relacoes_estrategicas
        if item.destino_nivel == "MIDIA" and item.destino == destino
    )


def test_baixa_notoriedade_aumenta_prioridade_de_construcao_de_alcance():
    baixa = _traduzir(_briefing(notoriedade="baixa"))
    alta = _traduzir(_briefing(notoriedade="muito alta"))

    assert _objetivo(baixa, "construir alcance").pontuacao_contextual > (
        _objetivo(alta, "construir alcance").pontuacao_contextual
    )
    assert baixa.objetivos_midia_derivados[0].categoria == "construir alcance"


def test_lembranca_eleva_frequencia_e_continuidade():
    contrato = _traduzir(_briefing(comunicacao="lembrança"))

    assert {item.categoria for item in contrato.objetivos_midia_derivados[:2]} == {
        "gerar frequência", "sustentar continuidade",
    }
    assert all(item.pontuacao_contextual >= 65 for item in contrato.objetivos_midia_derivados)


def test_verba_restrita_penaliza_sem_zerar_objetivo():
    livre = _traduzir(_briefing(restrita=False))
    restrita = _traduzir(_briefing(restrita=True))
    relacao = _relacao(restrita, "construir alcance")

    assert relacao.penalizacoes
    assert relacao.pontuacao_contextual > 0
    assert relacao.pontuacao_contextual < _relacao(livre, "construir alcance").pontuacao_contextual


def test_ausencia_de_fonte_reduz_confianca_sem_zerar_pontuacao():
    com_fonte = _traduzir(_briefing(fontes=True))
    sem_fonte = _traduzir(_briefing(fontes=False))

    assert _relacao(com_fonte, "construir alcance").confianca in {
        Confianca.MEDIA, Confianca.ALTA,
    }
    assert _relacao(sem_fonte, "construir alcance").confianca is Confianca.BAIXA
    assert _relacao(sem_fonte, "construir alcance").pontuacao_contextual == (
        _relacao(com_fonte, "construir alcance").pontuacao_contextual
    )


def test_prioridade_declarada_altera_peso_efetivo():
    alta = _traduzir(_briefing(prioridade="muito alta"))
    baixa = _traduzir(_briefing(prioridade="baixa"))

    assert _objetivo(alta, "construir alcance").peso_efetivo != pytest.approx(
        _objetivo(baixa, "construir alcance").peso_efetivo
    )


def test_objetivos_diferentes_podem_empatar_tecnicamente():
    contrato = _traduzir(_briefing(comunicacao="conhecimento"))
    frequencia = _relacao(contrato, "gerar frequência")
    continuidade = _relacao(contrato, "sustentar continuidade")

    assert frequencia.ordem_contextual == continuidade.ordem_contextual
    assert frequencia.condicao == continuidade.condicao == "EMPATE_TECNICO"


def test_valor_ajustado_preserva_o_calculado():
    calculado = _objetivo(_traduzir(_briefing()), "construir alcance")
    ajustado = calculado.model_copy(update={
        "peso_ajustado": 0.4,
        "peso_efetivo": 0.4,
    })

    assert ajustado.peso_calculado == calculado.peso_calculado
    assert ajustado.peso_ajustado == ajustado.peso_efetivo == 0.4


def test_texto_nao_decisorio_nao_muda_pesos():
    antes = _traduzir(_briefing(motivo="nota A"))
    depois = _traduzir(_briefing(motivo="texto completamente diferente"))

    assert tuple(item.peso_efetivo for item in antes.objetivos_midia_derivados) == (
        tuple(item.peso_efetivo for item in depois.objetivos_midia_derivados)
    )


def test_ordem_contextual_nao_depende_da_ordem_da_regra():
    class CatalogoInvertido(CatalogoTraducaoInicial):
        def regra_para(self, objetivo_comunicacao):
            regra = super().regra_para(objetivo_comunicacao)
            return regra.model_copy(update={
                "objetivos_midia": tuple(reversed(regra.objetivos_midia)),
                "indicadores": tuple(reversed(regra.indicadores)),
            })

    normal = _traduzir(_briefing())
    invertido = _traduzir(_briefing(), CatalogoInvertido())

    assert tuple(item.categoria for item in normal.objetivos_midia_derivados) == (
        tuple(item.categoria for item in invertido.objetivos_midia_derivados)
    )
    assert normal.objetivos_midia_derivados[0].categoria == "construir alcance"


def test_todo_peso_tem_explicacao_de_origem():
    contrato = _traduzir(_briefing())

    assert contrato.versao_composicao == "1.0.0"
    assert all(item.peso_calculado is not None for item in contrato.objetivos_midia_derivados)
    assert all(item.peso_efetivo is not None for item in contrato.objetivos_midia_derivados)
    assert all(item.explicacao_peso for item in contrato.objetivos_midia_derivados)
    assert sum(item.peso_efetivo for item in contrato.objetivos_midia_derivados) == pytest.approx(1.0, abs=1e-5)
