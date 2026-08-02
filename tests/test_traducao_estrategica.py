from datetime import datetime, timezone
from uuid import uuid4

import pytest

from domain.briefing import BriefingInicial, ConteudoBriefing, EstadoBriefing
from domain.contracts import Confianca
from domain.traducao import EstadoContratoEstrategico, traduzir_briefing


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
            sem_restricoes_declaradas=True,
        ),
    }
    dados.update(ajustes)
    return BriefingInicial(**dados)


def test_traducao_provisoria_preserva_origens_e_nao_escolhe_canais():
    briefing = briefing_concluido()
    contrato = traduzir_briefing(
        briefing, contrato_id=uuid4(), criado_por=briefing.criado_por,
        criado_em=briefing.criado_em,
    )
    assert contrato.estado is EstadoContratoEstrategico.PROVISORIO
    assert contrato.briefing_id == briefing.id
    assert contrato.briefing_versao == 1
    assert [item.categoria for item in contrato.objetivos_midia_derivados] == [
        "construir alcance", "ampliar cobertura"
    ]
    assert contrato.objetivos_midia_derivados[0].regra == (
        "MAPA_COMUNICACAO_MIDIA:conhecimento"
    )
    assert contrato.confianca is Confianca.BAIXA
    serializado = contrato.model_dump(mode="json")
    assert "inventarios" not in serializado
    assert "distribuicao_verba" not in serializado


def test_sem_regra_produz_parcial_e_lacuna_sem_inventar_objetivo():
    briefing = briefing_concluido(conteudo=ConteudoBriefing(
        objetivos_marketing=({"categoria": "Diversificação"},),
        objetivos_comunicacao=({"categoria": "fidelização"},),
    ))
    contrato = traduzir_briefing(
        briefing, contrato_id=uuid4(), criado_por=briefing.criado_por,
        criado_em=briefing.criado_em,
    )
    assert contrato.estado is EstadoContratoEstrategico.PARCIAL
    assert contrato.objetivos_midia_derivados == ()
    assert any("regra de derivação" in item for item in contrato.lacunas)


def test_rejeita_briefing_nao_concluido():
    briefing = briefing_concluido(estado=EstadoBriefing.EM_PREENCHIMENTO)
    with pytest.raises(ValueError, match="concluído"):
        traduzir_briefing(
            briefing, contrato_id=uuid4(), criado_por=briefing.criado_por,
            criado_em=briefing.criado_em,
        )
