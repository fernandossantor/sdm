from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum


def _opcional(valor: str | None) -> str | None:
    if valor is None:
        return None
    if not isinstance(valor, str):
        raise TypeError("valor deve ser texto")
    return valor.strip() or None


def _textos(valores: tuple[str, ...], campo: str) -> tuple[str, ...]:
    itens = tuple(_opcional(item) for item in valores)
    if any(item is None for item in itens):
        raise ValueError(f"{campo} contém item vazio")
    return itens  # type: ignore[return-value]


def _decimal(valor: Decimal | None, campo: str) -> None:
    if valor is not None and (
        not isinstance(valor, Decimal) or not valor.is_finite() or valor < 0
    ):
        raise ValueError(f"{campo} deve ser Decimal não negativo")


class NaturezaLimiteVerba(str, Enum):
    RIGIDO = "RIGIDO"
    FLEXIVEL = "FLEXIVEL"
    ESTIMADO = "ESTIMADO"
    AINDA_NAO_DEFINIDO = "AINDA_NAO_DEFINIDO"


ROTULOS_NATUREZA_LIMITE = {
    NaturezaLimiteVerba.RIGIDO: "Rígido",
    NaturezaLimiteVerba.FLEXIVEL: "Flexível",
    NaturezaLimiteVerba.ESTIMADO: "Estimado",
    NaturezaLimiteVerba.AINDA_NAO_DEFINIDO: "Ainda não definido",
}


@dataclass(frozen=True, slots=True)
class IntervaloDeclarado:
    data_inicial: date
    data_final: date
    descricao: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.data_inicial, date) or not isinstance(self.data_final, date):
            raise TypeError("datas do intervalo devem ser date")
        object.__setattr__(self, "descricao", _opcional(self.descricao))


@dataclass(frozen=True, slots=True)
class PeriodoPretendido:
    data_inicial: date | None
    data_final: date | None
    duracao: str | None
    datas_criticas: tuple[date, ...]
    sazonalidades: tuple[str, ...]
    eventos_condicionantes: tuple[str, ...]
    periodos_obrigatorios: tuple[IntervaloDeclarado, ...]
    periodos_vedados: tuple[IntervaloDeclarado, ...]
    observacao: str | None

    def __post_init__(self) -> None:
        for campo in ("data_inicial", "data_final"):
            valor = getattr(self, campo)
            if valor is not None and not isinstance(valor, date):
                raise TypeError(f"{campo} deve ser date")
        criticas = tuple(self.datas_criticas)
        if any(not isinstance(item, date) for item in criticas):
            raise TypeError("datas_criticas deve conter date")
        if len(criticas) != len(set(criticas)):
            raise ValueError("datas_criticas possui duplicatas")
        object.__setattr__(self, "duracao", _opcional(self.duracao))
        object.__setattr__(self, "datas_criticas", criticas)
        object.__setattr__(self, "sazonalidades", _textos(tuple(self.sazonalidades), "sazonalidades"))
        object.__setattr__(self, "eventos_condicionantes", _textos(tuple(self.eventos_condicionantes), "eventos_condicionantes"))
        object.__setattr__(self, "periodos_obrigatorios", tuple(self.periodos_obrigatorios))
        object.__setattr__(self, "periodos_vedados", tuple(self.periodos_vedados))
        object.__setattr__(self, "observacao", _opcional(self.observacao))


@dataclass(frozen=True, slots=True)
class VerbaDeclarada:
    valor_total: Decimal | None
    moeda: str | None
    natureza_limite: NaturezaLimiteVerba
    margem_flexibilidade: str | None
    valor_minimo: Decimal | None
    valor_maximo: Decimal | None
    parcela_comprometida: Decimal | None
    observacao: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.natureza_limite, NaturezaLimiteVerba):
            raise TypeError("natureza_limite inválida")
        for campo in ("valor_total", "valor_minimo", "valor_maximo", "parcela_comprometida"):
            _decimal(getattr(self, campo), campo)
        for campo in ("moeda", "margem_flexibilidade", "observacao"):
            object.__setattr__(self, campo, _opcional(getattr(self, campo)))


@dataclass(frozen=True, slots=True)
class ContextoPeriodoVerba:
    periodo: PeriodoPretendido
    verba: VerbaDeclarada

    def diagnosticos(self) -> tuple[str, ...]:
        alertas: list[str] = []
        periodo, verba = self.periodo, self.verba
        if periodo.data_inicial and periodo.data_final and periodo.data_final < periodo.data_inicial:
            alertas.append("Data final anterior à inicial.")
        if (periodo.data_inicial is None or periodo.data_final is None) and periodo.duracao is None:
            alertas.append("Duração ausente quando as datas não estão definidas.")
        if periodo.sazonalidades and not (
            periodo.data_inicial or periodo.data_final or periodo.datas_criticas
        ):
            alertas.append("Sazonalidade informada sem correspondência temporal.")
        if periodo.data_inicial and periodo.data_final:
            for item in periodo.periodos_obrigatorios:
                if item.data_inicial < periodo.data_inicial or item.data_final > periodo.data_final:
                    alertas.append("Período obrigatório fora do intervalo principal.")
                    break
        if verba.valor_total is None:
            alertas.append("Verba ausente.")
        if any(valor is not None for valor in (verba.valor_total, verba.valor_minimo, verba.valor_maximo, verba.parcela_comprometida)) and not verba.moeda:
            alertas.append("Moeda ausente.")
        if verba.valor_minimo is not None and verba.valor_maximo is not None and verba.valor_maximo < verba.valor_minimo:
            alertas.append("Valor máximo inferior ao mínimo.")
        if verba.parcela_comprometida is not None and verba.valor_total is not None and verba.parcela_comprometida > verba.valor_total:
            alertas.append("Parcela comprometida superior ao total.")
        if verba.natureza_limite is NaturezaLimiteVerba.RIGIDO and verba.margem_flexibilidade:
            alertas.append("Limite rígido com margem de flexibilidade incompatível.")
        return tuple(alertas)
