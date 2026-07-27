"""Tipos canônicos para métricas auditáveis e comparáveis.

Este módulo não persiste dados. Ele fixa o contrato de domínio que será usado
pela migration da Fase 1 e pelos engines, sem alterar os resultados atuais.
"""

from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from typing import Any


class NaturezaMetrica(StrEnum):
    FATO = "FATO"
    PREMISSA = "PREMISSA"
    DECISAO = "DECISAO"
    RESULTADO = "RESULTADO"


class OrigemMetrica(StrEnum):
    MEDIDO = "MEDIDO"
    CONTRATADO = "CONTRATADO"
    INFORMADO = "INFORMADO"
    CALCULADO = "CALCULADO"
    ESTIMADO = "ESTIMADO"


class NivelConfianca(StrEnum):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAIXA = "BAIXA"
    NAO_AVALIADA = "NAO_AVALIADA"


class SituacaoComparabilidade(StrEnum):
    COMPARAVEL = "COMPARAVEL"
    CONVERTIVEL = "CONVERTIVEL"
    NAO_COMPARAVEL = "NAO_COMPARAVEL"
    INDETERMINADO = "INDETERMINADO"


@dataclass(frozen=True, slots=True)
class ContextoMetrica:
    """Dimensões que determinam se duas métricas podem ser agregadas."""

    universo: str | None
    publico_alvo: str | None
    praca: str | None
    inicio_referencia: date | None
    fim_referencia: date | None
    metrica_nativa: str
    metodologia: str | None
    granularidade: str | None

    def campos_ausentes(self) -> tuple[str, ...]:
        campos = (
            "universo",
            "publico_alvo",
            "praca",
            "inicio_referencia",
            "fim_referencia",
            "metrica_nativa",
            "metodologia",
            "granularidade",
        )
        return tuple(nome for nome in campos if not getattr(self, nome))


@dataclass(frozen=True, slots=True)
class ValorMetrica:
    """Valor acompanhado dos metadados mínimos definidos pela DM-001."""

    valor: float
    unidade: str
    natureza: NaturezaMetrica
    origem: OrigemMetrica
    contexto: ContextoMetrica
    confianca: NivelConfianca = NivelConfianca.NAO_AVALIADA
    fonte: str | None = None
    versao_metodo: str | None = None
    entradas: tuple[Any, ...] = ()

    def validar(self) -> tuple[str, ...]:
        erros: list[str] = []
        if not self.unidade.strip():
            erros.append("A unidade da métrica é obrigatória.")
        if self.origem is OrigemMetrica.MEDIDO and not self.fonte:
            erros.append("Uma métrica medida deve informar a fonte.")
        if self.natureza is NaturezaMetrica.RESULTADO:
            if not self.versao_metodo:
                erros.append("Um resultado deve informar a versão do método.")
            if not self.entradas:
                erros.append("Um resultado deve apontar suas entradas.")
        if (
            self.contexto.inicio_referencia
            and self.contexto.fim_referencia
            and self.contexto.fim_referencia < self.contexto.inicio_referencia
        ):
            erros.append("O fim da referência não pode preceder o início.")
        return tuple(erros)


@dataclass(frozen=True, slots=True)
class ResultadoComparabilidade:
    situacao: SituacaoComparabilidade
    divergencias: tuple[str, ...] = ()

    @property
    def permite_agregacao_direta(self) -> bool:
        return self.situacao is SituacaoComparabilidade.COMPARAVEL


def comparar_contextos(
    primeiro: ContextoMetrica,
    segundo: ContextoMetrica,
    *,
    conversao_explicita: bool = False,
) -> ResultadoComparabilidade:
    """Classifica a comparabilidade sem fazer conversões implícitas."""

    ausentes = sorted(
        set(primeiro.campos_ausentes()) | set(segundo.campos_ausentes())
    )
    if ausentes:
        return ResultadoComparabilidade(
            SituacaoComparabilidade.INDETERMINADO,
            tuple(ausentes),
        )

    campos = (
        "universo",
        "publico_alvo",
        "praca",
        "inicio_referencia",
        "fim_referencia",
        "metrica_nativa",
        "metodologia",
        "granularidade",
    )
    divergencias = tuple(
        nome for nome in campos if getattr(primeiro, nome) != getattr(segundo, nome)
    )
    if not divergencias:
        return ResultadoComparabilidade(SituacaoComparabilidade.COMPARAVEL)
    if conversao_explicita:
        return ResultadoComparabilidade(
            SituacaoComparabilidade.CONVERTIVEL,
            divergencias,
        )
    return ResultadoComparabilidade(
        SituacaoComparabilidade.NAO_COMPARAVEL,
        divergencias,
    )
