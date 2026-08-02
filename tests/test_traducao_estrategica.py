from datetime import datetime, timezone
from uuid import uuid4

import pytest

from domain.briefing import BriefingInicial, ConteudoBriefing, EstadoBriefing
from domain.contracts import Confianca
from domain.traducao import (
    EstadoContratoEstrategico, objetivos_midia_efetivos,
    revisar_traducao, traduzir_briefing,
)
from engines.traducao_estrategica import CatalogoTraducaoInicial


CATALOGO = CatalogoTraducaoInicial()


def briefing_concluido(**ajustes):
    dados = {
        "id": uuid4(), "campanha_id": uuid4(), "criado_por": uuid4(),
        "criado_em": datetime(2026, 8, 2, tzinfo=timezone.utc),
        "estado": EstadoBriefing.CONCLUIDO,
        "conteudo": ConteudoBriefing(
            objetivos_marketing=({"categoria": "Crescimento"},),
            objetivos_comunicacao=({"categoria": "conhecimento"},),
            publicos=({"nome": "Compradores"},), pracas=({"nome": "Brasil"},),
            periodo={"inicio": "2026-09-01", "fim": "2026-10-31"},
            jornada_aplicavel=False,
            sem_restricoes_declaradas=True,
        ),
    }
    dados.update(ajustes)
    return BriefingInicial(**dados)


def test_traducao_provisoria_preserva_origens_e_nao_escolhe_canais():
    briefing = briefing_concluido()
    contrato = traduzir_briefing(
        briefing, contrato_id=uuid4(), criado_por=briefing.criado_por,
        criado_em=briefing.criado_em, catalogo=CATALOGO,
    )
    assert contrato.estado is EstadoContratoEstrategico.PROVISORIO
    assert contrato.briefing_id == briefing.id
    assert contrato.briefing_versao == 1
    assert [item.categoria for item in contrato.objetivos_midia_derivados] == [
        "construir alcance", "gerar frequência", "sustentar continuidade"
    ]
    assert contrato.objetivos_midia_derivados[0].regra == "B15-CM-CONHECIMENTO"
    assert contrato.objetivos_midia_derivados[0].indicador_codigo == "B15-ALCANCE"
    assert {item.biblioteca for item in contrato.referencias_bibliotecas} == {
        14, 15, 16, 17, 18
    }
    assert contrato.dependencias_estrategicas
    assert contrato.confianca is Confianca.BAIXA
    serializado = contrato.model_dump(mode="json")
    assert "inventarios" not in serializado
    assert "distribuicao_verba" not in serializado


def test_sem_regra_produz_parcial_e_lacuna_sem_inventar_objetivo():
    briefing = briefing_concluido(conteudo=ConteudoBriefing(
        objetivos_marketing=({"categoria": "Diversificação"},),
        objetivos_comunicacao=({"categoria": "imagem"},),
    ))
    contrato = traduzir_briefing(
        briefing, contrato_id=uuid4(), criado_por=briefing.criado_por,
        criado_em=briefing.criado_em, catalogo=CATALOGO,
    )
    assert contrato.estado is EstadoContratoEstrategico.PARCIAL
    assert contrato.objetivos_midia_derivados == ()
    assert any("regra de derivação" in item for item in contrato.lacunas)


def test_rejeita_briefing_nao_concluido():
    briefing = briefing_concluido(estado=EstadoBriefing.EM_PREENCHIMENTO)
    with pytest.raises(ValueError, match="concluído"):
        traduzir_briefing(
            briefing, contrato_id=uuid4(), criado_por=briefing.criado_por,
            criado_em=briefing.criado_em, catalogo=CATALOGO,
        )


def test_revisao_cria_versao_e_preserva_derivacao_calculada():
    briefing = briefing_concluido()
    original = traduzir_briefing(
        briefing, contrato_id=uuid4(), criado_por=briefing.criado_por,
        criado_em=briefing.criado_em, catalogo=CATALOGO,
    )
    nova = revisar_traducao(
        original, contrato_id=uuid4(),
        categorias_aceitas=("construir alcance",),
        justificativa="Cobertura não é prioritária neste ciclo.",
        criado_por=briefing.criado_por, criado_em=briefing.criado_em,
        catalogo=CATALOGO,
    )

    assert nova.versao == 2
    assert nova.objetivos_midia_derivados == original.objetivos_midia_derivados
    assert [item.categoria for item in objetivos_midia_efetivos(nova)] == [
        "construir alcance"
    ]
    assert nova.intervencoes_humanas[-1].valor_calculado == "DERIVADO"
    assert nova.intervencoes_humanas[-1].valor_efetivo == "REJEITADO"


def test_revisao_exige_mudanca_e_justificativa():
    briefing = briefing_concluido()
    original = traduzir_briefing(
        briefing, contrato_id=uuid4(), criado_por=briefing.criado_por,
        criado_em=briefing.criado_em, catalogo=CATALOGO,
    )
    categorias = tuple(
        item.categoria for item in original.objetivos_midia_derivados
    )
    with pytest.raises(ValueError, match="justificativa"):
        revisar_traducao(
            original, contrato_id=uuid4(), categorias_aceitas=(),
            justificativa="", criado_por=briefing.criado_por,
            criado_em=briefing.criado_em, catalogo=CATALOGO,
        )
    with pytest.raises(ValueError, match="não altera"):
        revisar_traducao(
            original, contrato_id=uuid4(), categorias_aceitas=categorias,
            justificativa="Revisão", criado_por=briefing.criado_por,
            criado_em=briefing.criado_em, catalogo=CATALOGO,
        )


def test_planejador_pode_incluir_objetivo_da_biblioteca_com_justificativa():
    briefing = briefing_concluido(conteudo=ConteudoBriefing(
        objetivos_marketing=({"categoria": "Crescimento"},),
        objetivos_comunicacao=({"categoria": "imagem"},),
        publicos=({"nome": "Compradores"},), jornada_aplicavel=False,
    ))
    original = traduzir_briefing(
        briefing, contrato_id=uuid4(), criado_por=briefing.criado_por,
        criado_em=briefing.criado_em, catalogo=CATALOGO,
    )
    assert original.objetivos_midia_derivados == ()

    nova = revisar_traducao(
        original, contrato_id=uuid4(),
        categorias_aceitas=("produzir impacto",),
        justificativa="Imagem será observada por proxy de atenção.",
        criado_por=briefing.criado_por, criado_em=briefing.criado_em,
        catalogo=CATALOGO,
    )

    assert objetivos_midia_efetivos(nova)[0].categoria == "produzir impacto"
    assert objetivos_midia_efetivos(nova)[0].natureza == "AJUSTADO_PELO_USUARIO"
    assert nova.intervencoes_humanas[-1].valor_calculado == "NAO_DERIVADO"
