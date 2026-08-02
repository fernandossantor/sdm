from dataclasses import dataclass
from datetime import datetime
import re


_PADRAO_CODIGO = re.compile(
    r"MP-([0-9]{4})([0-9]{2})-([0-9]{4,})"
)


@dataclass(frozen=True, slots=True)
class CodigoCampanha:
    valor: str

    def __post_init__(self) -> None:
        correspondencia = _PADRAO_CODIGO.fullmatch(self.valor)
        if correspondencia is None:
            raise ValueError("Código da Campanha inválido")
        mes = int(correspondencia.group(2))
        if not 1 <= mes <= 12:
            raise ValueError("Mês do Código da Campanha inválido")


def gerar_codigo_campanha(
    criado_em: datetime,
    sequencial_global: int,
) -> CodigoCampanha:
    if criado_em.tzinfo is None or criado_em.utcoffset() is None:
        raise ValueError("criado_em deve possuir fuso horário")
    if type(sequencial_global) is not int or sequencial_global <= 0:
        raise ValueError("sequencial_global deve ser inteiro positivo")
    valor = f"MP-{criado_em:%Y%m}-{sequencial_global:04d}"
    return CodigoCampanha(valor)
