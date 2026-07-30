from datetime import datetime, timezone
from uuid import uuid4

from application.services.campanha_runtime import (
    AutorizadorCampanhaPorEspaco,
    GeradorCodigoTemporal,
)


def test_autorizador_exige_usuario_e_papel_com_escrita():
    usuario = uuid4()
    autorizador = AutorizadorCampanhaPorEspaco(
        usuario_id=usuario, papel_espaco="EDITOR"
    )
    assert autorizador.pode_criar(usuario)
    assert not autorizador.pode_criar(uuid4())
    assert not AutorizadorCampanhaPorEspaco(
        usuario_id=usuario, papel_espaco="LEITOR"
    ).pode_criar(usuario)


def test_codigo_temporal_respeita_contrato():
    instante = datetime(2026, 7, 30, 12, 34, 56, 789, tzinfo=timezone.utc)
    assert GeradorCodigoTemporal().proximo(instante) == "MP-202607-30123456000789"
