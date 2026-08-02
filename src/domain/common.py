from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Any, Generic, TypeVar


class NaturezaValor(str, Enum):
    INFORMADO = "INFORMADO"
    HERDADO = "HERDADO"
    CALCULADO = "CALCULADO"
    ESTIMADO = "ESTIMADO"
    INFERIDO = "INFERIDO"
    AJUSTADO_PELO_USUARIO = "AJUSTADO_PELO_USUARIO"
    PADRAO_APLICADO = "PADRAO_APLICADO"
    NAO_DISPONIVEL = "NAO_DISPONIVEL"
    NAO_APLICAVEL = "NAO_APLICAVEL"
    INVALIDO = "INVALIDO"


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class ValorComOrigem(Generic[T]):
    valor: T | None
    natureza: NaturezaValor

    def __post_init__(self) -> None:
        naturezas_sem_valor = {
            NaturezaValor.NAO_DISPONIVEL,
            NaturezaValor.NAO_APLICAVEL,
            NaturezaValor.INVALIDO,
        }
        if self.valor is None and self.natureza not in naturezas_sem_valor:
            raise ValueError("valor ausente exige natureza sem valor")
        if self.valor is not None and self.natureza in naturezas_sem_valor:
            raise ValueError("natureza sem valor exige valor ausente")


def texto_obrigatorio(valor: str, campo: str) -> None:
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{campo} deve ser texto não vazio")


def para_primitivos(valor: Any) -> Any:
    """Converte modelos do domínio em estruturas primitivas previsíveis."""
    if is_dataclass(valor) and not isinstance(valor, type):
        return {
            campo.name: para_primitivos(getattr(valor, campo.name))
            for campo in fields(valor)
        }
    if isinstance(valor, Enum):
        return valor.value
    if isinstance(valor, tuple):
        return [para_primitivos(item) for item in valor]
    if isinstance(valor, date):
        return valor.isoformat()
    if isinstance(valor, Decimal):
        return str(valor)
    return valor
