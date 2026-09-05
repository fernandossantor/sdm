from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NaturezaLimiteVerbaResumo:
    codigo: str
    rotulo: str


@dataclass(frozen=True, slots=True)
class IntervaloDeclaradoEntrada:
    data_inicial: str
    data_final: str
    descricao: str | None


@dataclass(frozen=True, slots=True)
class SalvarPeriodoVerbaEntrada:
    data_inicial: str | None
    data_final: str | None
    duracao: str | None
    datas_criticas: tuple[str, ...]
    sazonalidades: tuple[str, ...]
    eventos_condicionantes: tuple[str, ...]
    periodos_obrigatorios: tuple[IntervaloDeclaradoEntrada, ...]
    periodos_vedados: tuple[IntervaloDeclaradoEntrada, ...]
    observacao_periodo: str | None
    valor_total: str | None
    moeda: str | None
    natureza_limite: str
    margem_flexibilidade: str | None
    valor_minimo: str | None
    valor_maximo: str | None
    parcela_comprometida: str | None
    observacao_verba: str | None


@dataclass(frozen=True, slots=True)
class IntervaloDeclaradoResumo:
    data_inicial: str
    data_final: str
    descricao: str | None


@dataclass(frozen=True, slots=True)
class PeriodoVerbaResumo:
    data_inicial: str | None
    data_final: str | None
    duracao: str | None
    datas_criticas: tuple[str, ...]
    sazonalidades: tuple[str, ...]
    eventos_condicionantes: tuple[str, ...]
    periodos_obrigatorios: tuple[IntervaloDeclaradoResumo, ...]
    periodos_vedados: tuple[IntervaloDeclaradoResumo, ...]
    observacao_periodo: str | None
    valor_total: str | None
    moeda: str | None
    natureza_limite: str
    rotulo_natureza_limite: str
    margem_flexibilidade: str | None
    valor_minimo: str | None
    valor_maximo: str | None
    parcela_comprometida: str | None
    observacao_verba: str | None
    diagnosticos: tuple[str, ...]
