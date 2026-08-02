"""Caso de uso da demonstracao vertical da Traducao Estrategica."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Protocol

from src.domain.briefing import Briefing, DadoPendente, IndicadorDisponivel, Publico, Restricao, Segmento, TensaoEstrategica
from src.domain.campanha import Campanha, IdentificacaoCampanha, NaturezaLimiteVerba, Periodo, Praca, Verba
from src.domain.common import NaturezaValor, ValorComOrigem
from src.domain.objetivos import ObjetivoComunicacaoCandidato, ObjetivoMarketing, Prioridade
from src.engines.traducao_estrategica.engine import ComandoTraducao, ModoTraducao, MotorTraducaoEstrategica, ResultadoExecucaoTraducao
from src.engines.traducao_estrategica.mensurabilidade import ObjetivoDeclarado


class MotorTraducao(Protocol):
    def executar(self, comando: ComandoTraducao) -> ResultadoExecucaoTraducao: ...


@dataclass(frozen=True, slots=True)
class EntradaTraducaoVertical:
    id_comando: str
    campanha_id: str
    campanha_nome: str
    marca: str
    produto_ou_servico: str
    situacao_marca_mercado: str
    objetivos_marketing: tuple[str, ...]
    objetivos_comunicacao_candidatos: tuple[str, ...]
    publico_prioritario: str
    segmento_secundario: str
    praca: str
    data_inicial: date
    data_final: date
    verba: Decimal
    prioridade: str
    restricao: str
    tensao_estrategica: str
    notoriedade_auxiliada: Decimal | None
    taxa_conclusao_proposta: Decimal | None
    pressao_competitiva: float
    verba_disponivel_percentual_do_necessario: float
    jornada: str
    linha_de_base_vendas: float | None = None
    meta_vendas: float | None = None
    observacao_nao_decisoria: str | None = None


def _ausente():
    return ValorComOrigem(None, NaturezaValor.NAO_DISPONIVEL)


class ExecutarTraducaoVertical:
    def __init__(self, motor: MotorTraducao | None = None) -> None:
        self._motor = motor or MotorTraducaoEstrategica()

    def executar(self, entrada: EntradaTraducaoVertical) -> ResultadoExecucaoTraducao:
        comando = ComandoTraducao(
            id_comando=entrada.id_comando,
            modo=ModoTraducao.TRADUZIR_BRIEFING,
            briefing=self._briefing(entrada),
            objetivos_mensuraveis=self._objetivos(entrada),
            jornada=entrada.jornada,
            pressao_competitiva=entrada.pressao_competitiva,
            verba_disponivel_percentual_do_necessario=entrada.verba_disponivel_percentual_do_necessario,
            observacao_nao_decisoria=entrada.observacao_nao_decisoria,
        )
        return self._motor.executar(comando)

    @staticmethod
    def _indicadores(entrada: EntradaTraducaoVertical):
        itens = []
        for nome, valor in (("notoriedade auxiliada", entrada.notoriedade_auxiliada), ("taxa de conclusão do pedido de proposta", entrada.taxa_conclusao_proposta)):
            if valor is not None:
                itens.append(IndicadorDisponivel(nome, ValorComOrigem(valor, NaturezaValor.INFORMADO), "percentual", entrada.publico_prioritario, entrada.praca, "informado para esta análise", "informada pelo planejador", "não detalhada", "INDETERMINADA"))
        return tuple(itens)

    @classmethod
    def _briefing(cls, entrada: EntradaTraducaoVertical) -> Briefing:
        prioridade = Prioridade(entrada.prioridade)
        pendentes = []
        if entrada.linha_de_base_vendas is None:
            pendentes.append(DadoPendente("linha_de_base_de_vendas"))
        if entrada.meta_vendas is None:
            pendentes.append(DadoPendente("meta_de_vendas"))
        return Briefing(
            campanha=Campanha(IdentificacaoCampanha(entrada.campanha_id, entrada.campanha_nome, entrada.marca, entrada.produto_ou_servico)),
            situacao_marca_mercado=entrada.situacao_marca_mercado,
            objetivos_marketing=tuple(ObjetivoMarketing(nome, ordem, prioridade) for ordem, nome in enumerate(entrada.objetivos_marketing, 1)),
            objetivos_comunicacao_candidatos=tuple(ObjetivoComunicacaoCandidato(nome) for nome in entrada.objetivos_comunicacao_candidatos),
            publico_prioritario=Publico(entrada.publico_prioritario, entrada.publico_prioritario, entrada.praca, prioridade, _ausente()),
            segmento_secundario=Segmento(entrada.segmento_secundario, entrada.segmento_secundario, entrada.praca, Prioridade.MEDIA, _ausente()),
            praca=Praca(entrada.praca, "praça declarada", _ausente()),
            periodo=Periodo(entrada.data_inicial, entrada.data_final),
            verba=Verba(ValorComOrigem(entrada.verba, NaturezaValor.INFORMADO), "BRL", NaturezaLimiteVerba.RIGIDO, _ausente()),
            prioridade=prioridade,
            restricao=Restricao("orçamentária", entrada.restricao, "campanha", prioridade, prioridade, "planejamento", entrada.restricao),
            tensao_estrategica=TensaoEstrategica(entrada.tensao_estrategica, (entrada.objetivos_marketing[0], entrada.restricao)),
            indicadores_disponiveis=cls._indicadores(entrada),
            dados_ausentes=tuple(pendentes),
        )

    @staticmethod
    def _objetivos(entrada: EntradaTraducaoVertical):
        codigos = {"aumento de vendas": "mkt_aumento_vendas", "crescimento": "mkt_crescimento"}
        return tuple(ObjetivoDeclarado(
            codigo=codigos[nome], texto_original=nome, objeto_da_mudanca="vendas",
            publico=entrada.publico_prioritario, praca=entrada.praca, direcao="aumentar",
            indicador="vendas", unidade_ou_escala="quantidade",
            linha_de_base=entrada.linha_de_base_vendas, meta_ou_intensidade=entrada.meta_vendas,
            horizonte_temporal=f"{entrada.data_inicial.isoformat()}/{entrada.data_final.isoformat()}",
            fonte=None, confianca="INDETERMINADA", forma_mensuracao="METRICA_DIRETA",
        ) for nome in entrada.objetivos_marketing)
