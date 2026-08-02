from __future__ import annotations

import json
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from src.domain.objetivos import Prioridade


@dataclass(frozen=True, slots=True)
class CandidatoComunicacao:
    codigo: str
    nome: str
    forca_padrao_minima: int
    forca_padrao_maxima: int
    condicao: str
    adequacao_publico: float
    adequacao_praca: float
    adequacao_jornada: float
    adequacao_periodo: float
    adequacao_restricoes: float


@dataclass(frozen=True, slots=True)
class SituacaoMercadologica:
    notoriedade_percentual: float | None
    conversao_percentual: float | None


@dataclass(frozen=True, slots=True)
class ContextoMatriz:
    objetivo_marketing: str
    prioridade_declarada: Prioridade
    candidatos: tuple[CandidatoComunicacao, ...]
    situacao_mercadologica: SituacaoMercadologica
    pressao_competitiva: float
    publico: str
    praca: str
    jornada: str
    periodo: str
    verba_disponivel_percentual_do_necessario: float
    restricoes: tuple[str, ...]
    confianca: float


@dataclass(frozen=True, slots=True)
class ContribuicaoDimensao:
    dimensao: str
    valor: float
    peso: float
    contribuicao: float


@dataclass(frozen=True, slots=True)
class Penalizacao:
    codigo: str
    valor: float
    motivo: str


@dataclass(frozen=True, slots=True)
class AvaliacaoCandidato:
    candidato: str
    forca_contextual: float
    ordem: int
    condicao: str
    contribuicoes_por_dimensao: tuple[ContribuicaoDimensao, ...]
    penalizacoes: tuple[Penalizacao, ...]
    confianca: float
    justificativa_estruturada: tuple[str, ...]
    alertas: tuple[str, ...]
    versao_configuracao: str


def _carregar_configuracao(caminho: str | Path | None) -> dict[str, Any]:
    arquivo = (
        Path(caminho)
        if caminho is not None
        else Path(__file__).parents[2]
        / "knowledge"
        / "configuracao_matriz_marketing_comunicacao.yaml"
    )
    configuracao = json.loads(arquivo.read_text(encoding="utf-8"))
    if not configuracao.get("ativo") or not configuracao.get("versao"):
        raise ValueError("configuração da matriz deve estar ativa e versionada")
    if abs(sum(configuracao["pesos"].values()) - 1.0) > 1e-9:
        raise ValueError("pesos da matriz devem somar 1,00")
    return configuracao


def _limitar(valor: float) -> float:
    return max(0.0, min(100.0, valor))


def _validar_entrada(contexto: ContextoMatriz) -> None:
    if not contexto.candidatos:
        raise ValueError("ao menos um candidato de Comunicação é obrigatório")
    if len({item.codigo for item in contexto.candidatos}) != len(contexto.candidatos):
        raise ValueError("códigos de candidatos devem ser únicos")
    valores = (
        contexto.pressao_competitiva,
        contexto.verba_disponivel_percentual_do_necessario,
        contexto.confianca,
    )
    if any(valor < 0 or valor > 100 for valor in valores):
        raise ValueError("valores contextuais devem estar entre 0 e 100")
    for candidato in contexto.candidatos:
        if not 0 <= candidato.forca_padrao_minima <= candidato.forca_padrao_maxima <= 100:
            raise ValueError("faixa de força padrão inválida")
        adequacoes = (
            candidato.adequacao_publico,
            candidato.adequacao_praca,
            candidato.adequacao_jornada,
            candidato.adequacao_periodo,
            candidato.adequacao_restricoes,
        )
        if any(valor < 0 or valor > 100 for valor in adequacoes):
            raise ValueError("adequações devem estar entre 0 e 100")


def _situacao_mercadologica(
    codigo: str, situacao: SituacaoMercadologica, configuracao: dict[str, Any]
) -> tuple[float, tuple[str, ...]]:
    valor = float(configuracao["valor_neutro"])
    justificativas: list[str] = []
    limiares = configuracao["limiares"]
    ajustes = configuracao["ajustes_mercadologicos"]
    if situacao.notoriedade_percentual is not None:
        if situacao.notoriedade_percentual < limiares["notoriedade_baixa_abaixo_de"]:
            valor += ajustes["notoriedade_baixa"].get(codigo, 0)
            justificativas.append("notoriedade_baixa")
        elif situacao.notoriedade_percentual >= limiares["notoriedade_alta_a_partir_de"]:
            valor += ajustes["notoriedade_alta"].get(codigo, 0)
            justificativas.append("notoriedade_alta")
    if (
        situacao.conversao_percentual is not None
        and situacao.conversao_percentual <= limiares["conversao_baixa_ate"]
    ):
        valor += ajustes["conversao_baixa"].get(codigo, 0)
        justificativas.append("conversao_baixa")
    return _limitar(valor), tuple(justificativas)


def _avaliar_candidato(
    candidato: CandidatoComunicacao,
    contexto: ContextoMatriz,
    configuracao: dict[str, Any],
) -> AvaliacaoCandidato:
    mercado, justificativas = _situacao_mercadologica(
        candidato.codigo, contexto.situacao_mercadologica, configuracao
    )
    valores = {
        "forca_padrao": (candidato.forca_padrao_minima + candidato.forca_padrao_maxima) / 2,
        "prioridade": configuracao["prioridades"][contexto.prioridade_declarada.value],
        "situacao_mercadologica": mercado,
        "situacao_competitiva": contexto.pressao_competitiva,
        "publico": candidato.adequacao_publico,
        "praca": candidato.adequacao_praca,
        "jornada": candidato.adequacao_jornada,
        "periodo": candidato.adequacao_periodo,
        "verba": _limitar(contexto.verba_disponivel_percentual_do_necessario),
        "restricoes": candidato.adequacao_restricoes,
        "confianca": contexto.confianca,
    }
    contribuicoes = tuple(
        ContribuicaoDimensao(
            dimensao=dimensao,
            valor=valor,
            peso=configuracao["pesos"][dimensao],
            contribuicao=round(valor * configuracao["pesos"][dimensao], 4),
        )
        for dimensao, valor in valores.items()
    )
    penalizacoes: list[Penalizacao] = []
    if (
        contexto.verba_disponivel_percentual_do_necessario
        <= configuracao["limiares"]["verba_muito_restrita_ate"]
    ):
        valor = configuracao["penalizacoes_verba_muito_restrita"].get(
            candidato.codigo, 0
        )
        if valor:
            penalizacoes.append(
                Penalizacao(
                    codigo="verba_muito_restrita",
                    valor=float(valor),
                    motivo="A verba declarada é muito restrita para o escopo.",
                )
            )
    forca = sum(item.contribuicao for item in contribuicoes) - sum(
        item.valor for item in penalizacoes
    )
    alertas = tuple(
        alerta
        for alerta, condicao in (
            ("notoriedade ausente", contexto.situacao_mercadologica.notoriedade_percentual is None),
            ("conversão ausente", contexto.situacao_mercadologica.conversao_percentual is None),
            ("há restrições declaradas", bool(contexto.restricoes)),
        )
        if condicao
    )
    return AvaliacaoCandidato(
        candidato=candidato.codigo,
        forca_contextual=round(_limitar(forca), 2),
        ordem=0,
        condicao=candidato.condicao,
        contribuicoes_por_dimensao=contribuicoes,
        penalizacoes=tuple(penalizacoes),
        confianca=contexto.confianca,
        justificativa_estruturada=justificativas,
        alertas=alertas,
        versao_configuracao=configuracao["versao"],
    )


def avaliar_matriz_marketing_comunicacao(
    contexto: ContextoMatriz,
    caminho_configuracao: str | Path | None = None,
) -> tuple[AvaliacaoCandidato, ...]:
    """Avalia e ordena candidatos sem derivar objetivos de Mídia."""
    _validar_entrada(contexto)
    configuracao = _carregar_configuracao(caminho_configuracao)
    avaliacoes = tuple(
        _avaliar_candidato(candidato, contexto, configuracao)
        for candidato in contexto.candidatos
    )
    ordenadas = sorted(avaliacoes, key=lambda item: (-item.forca_contextual, item.candidato))
    return tuple(replace(item, ordem=ordem) for ordem, item in enumerate(ordenadas, 1))
