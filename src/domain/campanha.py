from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum

from .common import ValorComOrigem, texto_obrigatorio


class NaturezaLimiteVerba(str, Enum):
    RIGIDO = "rígido"
    FLEXIVEL = "flexível"
    ESTIMADO = "estimado"
    AINDA_NAO_DEFINIDO = "ainda não definido"


@dataclass(frozen=True, slots=True)
class IdentificacaoCampanha:
    id: str
    nome: str
    marca: str
    produto_ou_servico: str

    def __post_init__(self) -> None:
        for campo in ("id", "nome", "marca", "produto_ou_servico"):
            texto_obrigatorio(getattr(self, campo), campo)


@dataclass(frozen=True, slots=True)
class Praca:
    nome: str
    tipo_territorial: str
    universo_populacional: ValorComOrigem[int]

    def __post_init__(self) -> None:
        texto_obrigatorio(self.nome, "nome")
        texto_obrigatorio(self.tipo_territorial, "tipo_territorial")
        if (
            self.universo_populacional.valor is not None
            and self.universo_populacional.valor < 0
        ):
            raise ValueError("universo_populacional não pode ser negativo")


@dataclass(frozen=True, slots=True)
class Periodo:
    data_inicial: date
    data_final: date

    def __post_init__(self) -> None:
        if self.data_final < self.data_inicial:
            raise ValueError("data_final não pode ser anterior à data_inicial")


@dataclass(frozen=True, slots=True)
class Verba:
    valor_total: ValorComOrigem[Decimal]
    moeda: str
    natureza_do_limite: NaturezaLimiteVerba
    margem_de_flexibilidade: ValorComOrigem[Decimal]

    def __post_init__(self) -> None:
        texto_obrigatorio(self.moeda, "moeda")
        for campo, valor in (
            ("valor_total", self.valor_total.valor),
            ("margem_de_flexibilidade", self.margem_de_flexibilidade.valor),
        ):
            if valor is not None and valor < 0:
                raise ValueError(f"{campo} não pode ser negativo")


@dataclass(frozen=True, slots=True)
class Campanha:
    identificacao: IdentificacaoCampanha
