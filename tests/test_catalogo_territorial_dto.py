from dataclasses import FrozenInstanceError

import pytest

from mediad_planner.application.dto.catalogo_territorial import (
    EstadoCatalogoResumo,
    MunicipioCatalogoResumo,
    RegiaoGeograficaImediataCatalogoResumo,
    RegiaoGeograficaIntermediariaCatalogoResumo,
)


def _estado(**alteracoes: object) -> EstadoCatalogoResumo:
    dados = dict(
        codigo="43",
        sigla="rs",
        nome=" Rio Grande do Sul ",
        codigo_regiao="4",
        sigla_regiao="S",
        nome_regiao="Sul",
    )
    dados.update(alteracoes)
    return EstadoCatalogoResumo(**dados)


def test_estado_normaliza_campos_e_e_congelado() -> None:
    estado = _estado()
    assert (estado.codigo, estado.sigla, estado.nome) == (
        "43",
        "RS",
        "Rio Grande do Sul",
    )
    with pytest.raises(FrozenInstanceError):
        estado.nome = "Outro"  # type: ignore[misc]


@pytest.mark.parametrize("codigo", ["4", "043", "RS", 43])
def test_estado_rejeita_codigo_invalido(codigo: object) -> None:
    with pytest.raises((TypeError, ValueError), match="Código de UF inválido"):
        _estado(codigo=codigo)


@pytest.mark.parametrize("sigla", ["R", "RGS", "4S", ""])
def test_estado_rejeita_sigla_invalida(sigla: str) -> None:
    with pytest.raises(ValueError, match="Sigla de UF inválida"):
        _estado(sigla=sigla)


def test_estado_rejeita_nome_vazio_e_aceita_regiao_ausente() -> None:
    with pytest.raises(ValueError, match="Nome de UF inválido"):
        _estado(nome="  ")
    estado = _estado(codigo_regiao=None, sigla_regiao=None, nome_regiao=None)
    assert estado.codigo_regiao is None


def test_municipio_normaliza_e_valida_codigos() -> None:
    municipio = MunicipioCatalogoResumo("4318002", " São Borja ", "43")
    assert municipio.nome == "São Borja"
    for codigo in ("431800", "43180020", "abc8002"):
        with pytest.raises(ValueError, match="Código de Município inválido"):
            MunicipioCatalogoResumo(codigo, "São Borja", "43")
    with pytest.raises(ValueError, match="Código de UF inválido"):
        MunicipioCatalogoResumo("4318002", "São Borja", "RS")


def test_dto_intermediario_normaliza_e_e_congelado() -> None:
    regiao = RegiaoGeograficaIntermediariaCatalogoResumo(
        "4304", " Uruguaiana ", "43"
    )
    assert regiao.nome == "Uruguaiana"
    with pytest.raises(FrozenInstanceError):
        regiao.nome = "Outro"  # type: ignore[misc]


@pytest.mark.parametrize("codigo", ["430", "43045", "ABCD", 4304])
def test_dto_intermediario_rejeita_codigo_invalido(codigo: object) -> None:
    with pytest.raises(ValueError, match="Intermediária inválido"):
        RegiaoGeograficaIntermediariaCatalogoResumo(
            codigo, "Uruguaiana", "43"  # type: ignore[arg-type]
        )


def test_dto_intermediario_rejeita_nome_e_uf_invalidos() -> None:
    with pytest.raises(ValueError, match="Nome inválido"):
        RegiaoGeograficaIntermediariaCatalogoResumo("4304", " ", "43")
    with pytest.raises(ValueError, match="Código de UF inválido"):
        RegiaoGeograficaIntermediariaCatalogoResumo("4304", "Uruguaiana", "RS")


def test_dto_imediato_normaliza_e_e_congelado() -> None:
    regiao = RegiaoGeograficaImediataCatalogoResumo(
        "430017", " São Borja ", "43", "4304"
    )
    assert regiao.nome == "São Borja"
    with pytest.raises(FrozenInstanceError):
        regiao.nome = "Outro"  # type: ignore[misc]


@pytest.mark.parametrize("codigo", ["43017", "4300017", "ABC017", 430017])
def test_dto_imediato_rejeita_codigo_invalido(codigo: object) -> None:
    with pytest.raises(ValueError, match="Imediata inválido"):
        RegiaoGeograficaImediataCatalogoResumo(
            codigo, "São Borja", "43", "4304"  # type: ignore[arg-type]
        )


def test_dto_imediato_valida_intermediaria() -> None:
    with pytest.raises(ValueError, match="Intermediária inválido"):
        RegiaoGeograficaImediataCatalogoResumo(
            "430017", "São Borja", "43", "430"
        )
