from dataclasses import dataclass
from decimal import Decimal

from .campanha import Campanha, Periodo, Praca, Verba
from .common import ValorComOrigem, texto_obrigatorio
from .objetivos import (
    ObjetivoComunicacaoCandidato,
    ObjetivoMarketing,
    Prioridade,
)


@dataclass(frozen=True, slots=True)
class Publico:
    nome: str
    descricao: str
    praca: str
    prioridade: Prioridade
    tamanho_estimado: ValorComOrigem[int]

    def __post_init__(self) -> None:
        for campo in ("nome", "descricao", "praca"):
            texto_obrigatorio(getattr(self, campo), campo)
        if self.tamanho_estimado.valor is not None and self.tamanho_estimado.valor < 0:
            raise ValueError("tamanho_estimado não pode ser negativo")


@dataclass(frozen=True, slots=True)
class Segmento:
    nome: str
    descricao: str
    praca: str
    prioridade: Prioridade
    tamanho_estimado: ValorComOrigem[int]

    def __post_init__(self) -> None:
        for campo in ("nome", "descricao", "praca"):
            texto_obrigatorio(getattr(self, campo), campo)
        if self.tamanho_estimado.valor is not None and self.tamanho_estimado.valor < 0:
            raise ValueError("tamanho_estimado não pode ser negativo")


@dataclass(frozen=True, slots=True)
class Restricao:
    categoria: str
    descricao: str
    entidade_afetada: str
    intensidade: Prioridade
    prioridade: Prioridade
    origem: str
    justificativa: str

    def __post_init__(self) -> None:
        for campo in (
            "categoria",
            "descricao",
            "entidade_afetada",
            "origem",
            "justificativa",
        ):
            texto_obrigatorio(getattr(self, campo), campo)


@dataclass(frozen=True, slots=True)
class TensaoEstrategica:
    descricao: str
    elementos: tuple[str, ...]

    def __post_init__(self) -> None:
        texto_obrigatorio(self.descricao, "descricao")
        if len(self.elementos) < 2:
            raise ValueError("tensão exige ao menos dois elementos")
        for elemento in self.elementos:
            texto_obrigatorio(elemento, "elemento")


@dataclass(frozen=True, slots=True)
class IndicadorDisponivel:
    metrica: str
    valor: ValorComOrigem[Decimal]
    unidade_de_mensuracao: str
    publico_ou_target: str
    territorio: str
    periodo_de_referencia: str
    fonte: str
    metodologia: str
    nivel_de_confianca: str

    def __post_init__(self) -> None:
        for campo in (
            "metrica",
            "unidade_de_mensuracao",
            "publico_ou_target",
            "territorio",
            "periodo_de_referencia",
            "fonte",
            "metodologia",
            "nivel_de_confianca",
        ):
            texto_obrigatorio(getattr(self, campo), campo)


@dataclass(frozen=True, slots=True)
class DadoPendente:
    nome: str
    valor: None = None

    def __post_init__(self) -> None:
        texto_obrigatorio(self.nome, "nome")
        if self.valor is not None:
            raise ValueError("dado pendente deve permanecer ausente")


@dataclass(frozen=True, slots=True)
class Briefing:
    campanha: Campanha
    situacao_marca_mercado: str
    objetivos_marketing: tuple[ObjetivoMarketing, ...]
    objetivos_comunicacao_candidatos: tuple[ObjetivoComunicacaoCandidato, ...]
    publico_prioritario: Publico
    segmento_secundario: Segmento
    praca: Praca
    periodo: Periodo
    verba: Verba
    prioridade: Prioridade
    restricao: Restricao
    tensao_estrategica: TensaoEstrategica
    indicadores_disponiveis: tuple[IndicadorDisponivel, ...]
    dados_ausentes: tuple[DadoPendente, ...]

    def __post_init__(self) -> None:
        texto_obrigatorio(self.situacao_marca_mercado, "situacao_marca_mercado")
        if not self.objetivos_marketing:
            raise ValueError("briefing exige objetivo de Marketing")
        if not self.objetivos_comunicacao_candidatos:
            raise ValueError("briefing exige objetivo de Comunicação candidato")
        ordens = tuple(item.ordem_declarada for item in self.objetivos_marketing)
        if len(ordens) != len(set(ordens)):
            raise ValueError("ordens de objetivos de Marketing devem ser únicas")
