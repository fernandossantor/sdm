from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from mediad_planner.domain.campanha.codigo import (
    CodigoCampanha,
    gerar_codigo_campanha,
)


@pytest.mark.parametrize(
    "valor",
    (
        "MP-202607-0001",
        "MP-202612-9999",
        "MP-202701-10000",
    ),
)
def test_codigo_aceita_estrutura_valida(valor: str) -> None:
    assert CodigoCampanha(valor).valor == valor


@pytest.mark.parametrize(
    "valor",
    (
        "MP-202600-0001",
        "MP-202613-0001",
        "MP-202607-001",
        "MP-202607-ABCD",
        "mp-202607-0001",
        " MP-202607-0001",
        "MP-202607-0001 ",
        "MP-２０２６０７-0001",
        "MP-202607-٠٠٠١",
    ),
)
def test_codigo_rejeita_estrutura_invalida(valor: str) -> None:
    with pytest.raises(ValueError):
        CodigoCampanha(valor)


@pytest.mark.parametrize(
    ("data", "sequencial", "esperado"),
    (
        (datetime(2026, 7, 1, tzinfo=timezone.utc), 1, "MP-202607-0001"),
        (datetime(2026, 7, 31, tzinfo=timezone.utc), 2, "MP-202607-0002"),
        (datetime(2026, 8, 1, tzinfo=timezone.utc), 3, "MP-202608-0003"),
    ),
)
def test_gera_codigo_com_mes_e_sequencial_global(
    data: datetime,
    sequencial: int,
    esperado: str,
) -> None:
    assert gerar_codigo_campanha(data, sequencial).valor == esperado


@pytest.mark.parametrize("sequencial", (0, -1, 1.5, True, "1"))
def test_rejeita_sequencial_invalido(sequencial: object) -> None:
    with pytest.raises(ValueError):
        gerar_codigo_campanha(datetime.now(timezone.utc), sequencial)


def test_rejeita_data_sem_fuso_e_codigo_e_imutavel() -> None:
    with pytest.raises(ValueError, match="fuso"):
        gerar_codigo_campanha(datetime.now(), 1)
    codigo = gerar_codigo_campanha(datetime.now(timezone.utc), 1)
    with pytest.raises(FrozenInstanceError):
        codigo.valor = "MP-202608-0002"
