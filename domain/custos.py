"""Contrato monetário auditável para itens de mídia."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


CENTAVOS = Decimal("0.01")


def _decimal(valor) -> Decimal:
    return Decimal(str(valor or 0))


def _moeda(valor: Decimal) -> float:
    return float(valor.quantize(CENTAVOS, rounding=ROUND_HALF_UP))


@dataclass(frozen=True)
class CustoCompra:
    preco_tabela_unitario: float
    desconto_percentual: float
    preco_liquido_unitario: float
    custo_midia: float
    fee_tecnologia: float
    fee_dados: float
    fee_verificacao: float
    fee_operacao: float
    custo_total: float


def calcular_custo_compra(
    quantidade: float,
    preco_unitario_liquido: float,
    premissa: dict,
) -> CustoCompra:
    """Calcula o custo sem inferir desconto ou fee ausente.

    Por compatibilidade, ``preco_unitario_liquido`` continua sendo o preço
    efetivo quando ``preco_tabela_unitario`` não é informado.
    """

    quantidade_decimal = _decimal(quantidade)
    desconto = _decimal(premissa.get("desconto_percentual"))
    if desconto < 0 or desconto > 100:
        raise ValueError("O desconto percentual deve estar entre 0 e 100.")

    tabela_informada = premissa.get("preco_tabela_unitario")
    if tabela_informada is None:
        preco_tabela = _decimal(preco_unitario_liquido)
        preco_liquido = preco_tabela
        desconto = Decimal("0")
    else:
        preco_tabela = _decimal(tabela_informada)
        preco_liquido = preco_tabela * (Decimal("1") - desconto / Decimal("100"))

    if preco_tabela < 0 or preco_liquido < 0:
        raise ValueError("Os preços não podem ser negativos.")

    custo_midia = quantidade_decimal * preco_liquido
    fees = {}
    for nome in ("tecnologia", "dados", "verificacao", "operacao"):
        percentual = _decimal(premissa.get(f"fee_{nome}_percentual"))
        fixo = _decimal(premissa.get(f"fee_{nome}_fixo"))
        if percentual < 0 or fixo < 0:
            raise ValueError("Fees percentuais e fixos não podem ser negativos.")
        fees[nome] = custo_midia * percentual / Decimal("100") + fixo

    custo_total = custo_midia + sum(fees.values(), Decimal("0"))
    return CustoCompra(
        preco_tabela_unitario=_moeda(preco_tabela),
        desconto_percentual=float(desconto),
        preco_liquido_unitario=_moeda(preco_liquido),
        custo_midia=_moeda(custo_midia),
        fee_tecnologia=_moeda(fees["tecnologia"]),
        fee_dados=_moeda(fees["dados"]),
        fee_verificacao=_moeda(fees["verificacao"]),
        fee_operacao=_moeda(fees["operacao"]),
        custo_total=_moeda(custo_total),
    )
