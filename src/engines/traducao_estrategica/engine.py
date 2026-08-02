from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from src.domain.briefing import Briefing
from src.domain.contrato_estrategico import (
    ContratoEstrategico,
    EstadoContratoEstrategico,
)
from src.domain.objetivos import Prioridade
from src.engines.traducao_estrategica.matriz_comunicacao_midia import (
    ContextoDerivacaoMidia,
    ObjetivoComunicacaoPriorizado,
    ObjetivoMidiaDerivado,
    derivar_objetivos_midia,
)
from src.engines.traducao_estrategica.matriz_marketing_comunicacao import (
    AvaliacaoCandidato,
    CandidatoComunicacao,
    ContextoMatriz,
    SituacaoMercadologica,
    avaliar_matriz_marketing_comunicacao,
)
from src.engines.traducao_estrategica.mensurabilidade import (
    EstadoMensurabilidade,
    ObjetivoDeclarado,
    ResultadoMensurabilidade,
    classificar_mensurabilidade,
)
from src.knowledge.loader import carregar_conhecimento


class ModoTraducao(str, Enum):
    TRADUZIR_BRIEFING = "TRADUZIR_BRIEFING"


@dataclass(frozen=True, slots=True)
class ComandoTraducao:
    id_comando: str
    modo: ModoTraducao
    briefing: Briefing
    objetivos_mensuraveis: tuple[ObjetivoDeclarado, ...]
    jornada: str
    pressao_competitiva: float
    verba_disponivel_percentual_do_necessario: float
    observacao_nao_decisoria: str | None = None


@dataclass(frozen=True, slots=True)
class ComunicacaoPriorizada:
    codigo: str
    ordem: int
    forca_contextual: float
    prioridade: str
    contribuicoes_por_objetivo_marketing: tuple[tuple[str, float], ...]
    condicao: str


@dataclass(frozen=True, slots=True)
class ContratoEstrategicoProduzido:
    identidade: ContratoEstrategico
    mensurabilidade: tuple[tuple[str, ResultadoMensurabilidade], ...]
    objetivos_comunicacao: tuple[ComunicacaoPriorizada, ...]
    objetivos_midia: tuple[ObjetivoMidiaDerivado, ...]
    restricoes: tuple[str, ...]
    tensoes: tuple[str, ...]
    confianca: float
    explicacoes: tuple[str, ...]
    rastreabilidade: tuple[str, ...]
    dependencias: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ResultadoExecucaoTraducao:
    id_execucao: str
    id_comando: str
    motor: str
    modo_execucao: str
    estado_execucao: str
    resultado_principal: ContratoEstrategicoProduzido
    validacoes: tuple[str, ...]
    alertas: tuple[str, ...]
    restricoes: tuple[str, ...]
    confianca: float
    explicacao: tuple[str, ...]
    rastreabilidade: tuple[str, ...]
    dependencias: tuple[str, ...]
    versao_do_contrato: str


class MotorTraducaoEstrategica:
    def __init__(self, diretorio_conhecimento: str | Path | None = None) -> None:
        self._raiz = (
            Path(diretorio_conhecimento)
            if diretorio_conhecimento is not None
            else Path(__file__).parents[2] / "knowledge"
        )

    def executar(self, comando: ComandoTraducao) -> ResultadoExecucaoTraducao:
        self._validar_comando(comando)
        configuracao = self._carregar_configuracao()
        base = carregar_conhecimento(self._raiz)
        mensurabilidade = tuple(
            (objetivo.codigo, classificar_mensurabilidade(objetivo))
            for objetivo in comando.objetivos_mensuraveis
        )
        confianca = self._calcular_confianca(
            comando.objetivos_mensuraveis, mensurabilidade, configuracao
        )
        situacao = self._resolver_situacao(comando.briefing)
        avaliacoes = self._avaliar_marketing_comunicacao(
            comando, base, situacao, configuracao
        )
        comunicacao = self._propagar_comunicacao(avaliacoes, configuracao)
        midia = derivar_objetivos_midia(
            ContextoDerivacaoMidia(
                objetivos_comunicacao=tuple(
                    ObjetivoComunicacaoPriorizado(
                        codigo=item.codigo,
                        ordem=item.ordem,
                        forca_contextual=item.forca_contextual,
                        prioridade=Prioridade(item.prioridade),
                        confianca=confianca,
                    )
                    for item in comunicacao
                ),
                publico=comando.briefing.publico_prioritario.nome,
                praca=comando.briefing.praca.nome,
                jornada=comando.jornada,
                periodo=(
                    f"{comando.briefing.periodo.data_inicial.isoformat()}/"
                    f"{comando.briefing.periodo.data_final.isoformat()}"
                ),
                verba=str(comando.briefing.verba.valor_total.valor),
                intensidade_restricao_orcamentaria=max(
                    0.0,
                    100.0 - comando.verba_disponivel_percentual_do_necessario,
                ),
                restricoes=(comando.briefing.restricao.descricao,),
            ),
            self._raiz,
        )
        alertas = self._alertas(comando, mensurabilidade, midia, configuracao)
        estado = (
            EstadoContratoEstrategico.PROVISORIO
            if alertas
            else EstadoContratoEstrategico.DEFINITIVO
        )
        explicacoes = self._explicar(comunicacao, midia, confianca, alertas)
        rastreabilidade = self._rastreabilidade(comando, mensurabilidade, midia)
        dependencias = (
            "briefing",
            "objetivos.yaml@1.0",
            "relacoes_marketing_comunicacao.yaml@1.0",
            "relacoes_comunicacao_midia.yaml@1.0",
            "relacoes_comunicacao_midia_contrastes.yaml@1.0",
            "configuracao_matriz_marketing_comunicacao.yaml@1.0",
            "configuracao_matriz_comunicacao_midia.yaml@1.0",
            "configuracao_engine_traducao_estrategica.yaml@1.0",
        )
        identidade = ContratoEstrategico(
            id_campanha=comando.briefing.campanha.identificacao.id,
            versao="1.0",
            estado=estado,
            objetivos_marketing=tuple(
                item.categoria for item in comando.briefing.objetivos_marketing
            ),
            objetivos_comunicacao=tuple(item.codigo for item in comunicacao),
            objetivos_midia=tuple(item.codigo for item in midia),
            restricoes=(comando.briefing.restricao.descricao,),
            tensoes=(comando.briefing.tensao_estrategica.descricao,),
            lacunas=tuple(
                dado.nome for dado in comando.briefing.dados_ausentes
            ),
            explicacoes=explicacoes,
        )
        contrato = ContratoEstrategicoProduzido(
            identidade=identidade,
            mensurabilidade=mensurabilidade,
            objetivos_comunicacao=comunicacao,
            objetivos_midia=midia,
            restricoes=identidade.restricoes,
            tensoes=identidade.tensoes,
            confianca=confianca,
            explicacoes=explicacoes,
            rastreabilidade=rastreabilidade,
            dependencias=dependencias,
        )
        return ResultadoExecucaoTraducao(
            id_execucao=f"execucao:{comando.id_comando}",
            id_comando=comando.id_comando,
            motor="TRADUCAO_ESTRATEGICA",
            modo_execucao=comando.modo.value,
            estado_execucao=(
                "CONCLUIDA_COM_RESSALVAS" if alertas else "CONCLUIDA"
            ),
            resultado_principal=contrato,
            validacoes=("comando_valido", "contexto_minimo_resolvido"),
            alertas=alertas,
            restricoes=contrato.restricoes,
            confianca=confianca,
            explicacao=explicacoes,
            rastreabilidade=rastreabilidade,
            dependencias=dependencias,
            versao_do_contrato="1.0",
        )

    def _validar_comando(self, comando: ComandoTraducao) -> None:
        if comando.modo is not ModoTraducao.TRADUZIR_BRIEFING:
            raise ValueError("modo não suportado")
        if not comando.id_comando.strip():
            raise ValueError("id_comando é obrigatório")
        if not comando.objetivos_mensuraveis:
            raise ValueError("objetivos para mensurabilidade são obrigatórios")
        if not 0 <= comando.pressao_competitiva <= 100:
            raise ValueError("pressão competitiva deve estar entre 0 e 100")
        if not 0 <= comando.verba_disponivel_percentual_do_necessario <= 100:
            raise ValueError("relação da verba deve estar entre 0 e 100")

    def _carregar_configuracao(self) -> dict[str, Any]:
        caminho = self._raiz / "configuracao_engine_traducao_estrategica.yaml"
        configuracao = json.loads(caminho.read_text(encoding="utf-8"))
        if not configuracao.get("ativo") or not configuracao.get("versao"):
            raise ValueError("configuração do motor deve estar ativa e versionada")
        return configuracao

    @staticmethod
    def _resolver_situacao(briefing: Briefing) -> SituacaoMercadologica:
        notoriedade = None
        conversao = None
        for indicador in briefing.indicadores_disponiveis:
            nome = indicador.metrica.casefold()
            valor = indicador.valor.valor
            if valor is None:
                continue
            if nome == "notoriedade auxiliada":
                notoriedade = float(valor)
            elif nome == "taxa de conclusão do pedido de proposta":
                conversao = float(valor)
        return SituacaoMercadologica(notoriedade, conversao)

    def _avaliar_marketing_comunicacao(
        self,
        comando: ComandoTraducao,
        base: dict[str, tuple[dict[str, Any], ...]],
        situacao: SituacaoMercadologica,
        configuracao: dict[str, Any],
    ) -> tuple[tuple[str, AvaliacaoCandidato], ...]:
        objetivos = {item["nome"].casefold(): item for item in base["objetivos"]}
        candidatos_declarados = {
            objetivos[item.categoria.casefold()]["codigo"]
            for item in comando.briefing.objetivos_comunicacao_candidatos
        }
        relacoes = base["relacoes_marketing_comunicacao"]
        saidas: list[tuple[str, AvaliacaoCandidato]] = []
        for objetivo in comando.briefing.objetivos_marketing:
            origem = objetivos[objetivo.categoria.casefold()]["codigo"]
            aplicaveis = [
                item
                for item in relacoes
                if item["origem"] == origem and item["destino"] in candidatos_declarados
            ]
            candidatos = tuple(
                CandidatoComunicacao(
                    codigo=item["destino"],
                    nome=next(
                        obj["nome"]
                        for obj in base["objetivos"]
                        if obj["codigo"] == item["destino"]
                    ),
                    forca_padrao_minima=item["faixa_forca_padrao"]["minimo"],
                    forca_padrao_maxima=item["faixa_forca_padrao"]["maximo"],
                    condicao=item["condicao"],
                    adequacao_publico=configuracao["adequacao_contextual_neutra"],
                    adequacao_praca=configuracao["adequacao_contextual_neutra"],
                    adequacao_jornada=configuracao["adequacao_contextual_neutra"],
                    adequacao_periodo=configuracao["adequacao_contextual_neutra"],
                    adequacao_restricoes=configuracao["adequacao_contextual_neutra"],
                )
                for item in aplicaveis
            )
            if not candidatos:
                continue
            resultado = avaliar_matriz_marketing_comunicacao(
                ContextoMatriz(
                    objetivo_marketing=origem,
                    prioridade_declarada=objetivo.prioridade,
                    candidatos=candidatos,
                    situacao_mercadologica=situacao,
                    pressao_competitiva=comando.pressao_competitiva,
                    publico=comando.briefing.publico_prioritario.nome,
                    praca=comando.briefing.praca.nome,
                    jornada=comando.jornada,
                    periodo=str(comando.briefing.periodo),
                    verba_disponivel_percentual_do_necessario=(
                        comando.verba_disponivel_percentual_do_necessario
                    ),
                    restricoes=(comando.briefing.restricao.descricao,),
                    confianca=self._calcular_confianca_declarada(
                        comando.objetivos_mensuraveis, configuracao
                    ),
                )
            )
            saidas.extend((origem, item) for item in resultado)
        return tuple(saidas)

    @staticmethod
    def _propagar_comunicacao(
        avaliacoes: tuple[tuple[str, AvaliacaoCandidato], ...],
        configuracao: dict[str, Any],
    ) -> tuple[ComunicacaoPriorizada, ...]:
        agrupadas: dict[str, list[tuple[str, AvaliacaoCandidato]]] = {}
        for origem, avaliacao in avaliacoes:
            agrupadas.setdefault(avaliacao.candidato, []).append((origem, avaliacao))
        provisoria = []
        for codigo, itens in agrupadas.items():
            forca = round(sum(item[1].forca_contextual for item in itens) / len(itens), 2)
            melhor = max(itens, key=lambda item: item[1].forca_contextual)[1]
            provisoria.append((codigo, forca, melhor.condicao, itens))
        provisoria.sort(key=lambda item: (-item[1], item[0]))
        prioridades = configuracao["prioridade_por_ordem"]
        return tuple(
            ComunicacaoPriorizada(
                codigo=codigo,
                ordem=ordem,
                forca_contextual=forca,
                prioridade=prioridades.get(str(ordem), prioridades["demais"]),
                contribuicoes_por_objetivo_marketing=tuple(
                    (origem, avaliacao.forca_contextual)
                    for origem, avaliacao in itens
                ),
                condicao=condicao,
            )
            for ordem, (codigo, forca, condicao, itens) in enumerate(provisoria, 1)
        )

    @staticmethod
    def _calcular_confianca_declarada(
        objetivos: tuple[ObjetivoDeclarado, ...], configuracao: dict[str, Any]
    ) -> float:
        valores = [
            configuracao["confianca_declarada"].get(
                (objetivo.confianca or "INDETERMINADA").upper(), 20
            )
            for objetivo in objetivos
        ]
        return sum(valores) / len(valores)

    def _calcular_confianca(
        self,
        objetivos: tuple[ObjetivoDeclarado, ...],
        resultados: tuple[tuple[str, ResultadoMensurabilidade], ...],
        configuracao: dict[str, Any],
    ) -> float:
        declarada = self._calcular_confianca_declarada(objetivos, configuracao)
        estados = [
            configuracao["confianca_por_estado_mensurabilidade"][resultado.estado.value]
            for _, resultado in resultados
        ]
        return round(min(declarada, sum(estados) / len(estados)), 2)

    @staticmethod
    def _alertas(comando, mensurabilidade, midia, configuracao):
        alertas = [
            f"{codigo}: {resultado.alerta}"
            for codigo, resultado in mensurabilidade
            if resultado.alerta
        ]
        if (
            comando.verba_disponivel_percentual_do_necessario
            <= configuracao["limiar_verba_restrita"]
        ):
            alertas.append("verba muito restrita; viabilidade não determinada")
        alertas.extend(alerta for item in midia for alerta in item.alertas)
        return tuple(dict.fromkeys(alertas))

    @staticmethod
    def _explicar(comunicacao, midia, confianca, alertas):
        explicacoes = []
        if comunicacao:
            explicacoes.append(
                f"Comunicação prioritária: {comunicacao[0].codigo}, por maior força contextual."
            )
        if midia:
            explicacoes.append(
                f"Objetivo de Mídia prioritário: {midia[0].codigo}, derivado de relações versionadas."
            )
        explicacoes.append(f"Confiança geral: {confianca:.2f}.")
        if alertas:
            explicacoes.append("A saída é provisória e preserva as ressalvas registradas.")
        return tuple(explicacoes)

    @staticmethod
    def _rastreabilidade(comando, mensurabilidade, midia):
        rastros = [f"briefing:{comando.briefing.campanha.identificacao.id}"]
        rastros.extend(f"mensurabilidade:{codigo}:{resultado.estado.value}" for codigo, resultado in mensurabilidade)
        rastros.extend(
            f"relacao:{rastro.codigo_relacao}@{rastro.versao_relacao}"
            for objetivo in midia
            for rastro in objetivo.rastreabilidade
        )
        return tuple(dict.fromkeys(rastros))
