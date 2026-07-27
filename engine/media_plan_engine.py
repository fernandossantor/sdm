"""Cálculos auditáveis de entrega cross-media.

O motor não inventa audiência, alcance ou frequência. Cada item precisa trazer
as premissas mínimas e a interface deve identificar a origem de cada valor.
"""

from dataclasses import dataclass
from datetime import date
from math import ceil

from domain.metric_catalog import (
    ContextoMetrica,
    SituacaoComparabilidade,
    comparar_contextos,
)
from domain.restricoes import resolver_restricoes_compra
from engine.frequency_distribution_engine import FrequencyDistributionEngine


@dataclass(frozen=True)
class DeliveryResult:
    quantidade: float
    investimento: float
    audiencia_percentual: float
    alcance_percentual: float
    alcance_pessoas: int
    frequencia: float
    grp: float
    impressoes: int
    cliques: float
    conversoes: float
    retorno: float
    cpp: float | None
    cpm: float | None
    cpc: float | None
    cpa: float | None
    roi: float | None
    excesso_frequencia: float
    distribuicao_frequencia: dict
    confianca: str
    preco_tabela_unitario: float
    desconto_percentual: float
    preco_liquido_unitario: float
    custo_midia: float
    fee_tecnologia: float
    fee_dados: float
    fee_verificacao: float
    fee_operacao: float
    custo_total: float
    restricoes_ativas: tuple[str, ...]


class MediaPlanEngine:
    REQUIRED = ("audiencia_percentual", "alcance_percentual", "frequencia")

    @staticmethod
    def validar(premissa):
        ausentes = [campo for campo in MediaPlanEngine.REQUIRED if premissa.get(campo) is None]
        if ausentes:
            raise ValueError("Informe " + ", ".join(ausentes) + ".")
        audiencia = float(premissa["audiencia_percentual"])
        alcance = float(premissa["alcance_percentual"])
        frequencia = float(premissa["frequencia"])
        if not 0 < audiencia <= 100 or not 0 < alcance <= 100:
            raise ValueError("Audiência e alcance devem estar entre 0% e 100%.")
        if frequencia <= 0:
            raise ValueError("A frequência deve ser maior que zero.")

    @staticmethod
    def calcular_item(premissa, publico_referencia, preco_unitario):
        MediaPlanEngine.validar(premissa)
        preco = float(preco_unitario or 0)
        unidade = str(premissa.get("unidade_compra") or "").casefold()
        audiencia = float(premissa["audiencia_percentual"])
        alcance = float(premissa["alcance_percentual"])
        frequencia_meta = float(premissa["frequencia"])
        modo = str(premissa.get("modo_calculo") or "METAS").upper()
        contatos_meta = float(publico_referencia or 0) * alcance / 100 * frequencia_meta
        if modo == "METAS":
            if "mil impress" in unidade:
                quantidade = contatos_meta / 1000
            elif "impress" in unidade:
                quantidade = contatos_meta
            else:
                # Rating por unidade: inserções necessárias para entregar o GRP.
                quantidade = ceil(alcance * frequencia_meta / audiencia)
        else:
            quantidade = float(premissa.get("quantidade") or 0)
        restricoes = resolver_restricoes_compra(
            quantidade,
            modo,
            premissa,
            preco,
        )
        quantidade = restricoes.quantidade
        custo = restricoes.custo
        investimento = custo.custo_total
        pessoas = round(float(publico_referencia or 0) * alcance / 100)

        if "mil impress" in unidade:
            impressoes = round(quantidade * 1000)
        elif "impress" in unidade:
            impressoes = round(quantidade)
        else:
            # Para inserções e períodos, audiência é o rating médio da unidade.
            impressoes = round(float(publico_referencia or 0) * audiencia / 100 * quantidade)
        if publico_referencia:
            grp = round(impressoes / float(publico_referencia) * 100, 2)
        else:
            grp = round(audiencia * quantidade, 2)
        frequencia = round(grp / alcance, 2) if alcance else 0
        ctr = float(premissa.get("ctr") or 0) / 100
        taxa_conversao = float(premissa.get("taxa_conversao") or 0) / 100
        cliques = impressoes * ctr
        conversoes = cliques * taxa_conversao
        retorno = conversoes * float(premissa.get("valor_conversao") or 0)
        maximo_frequencia = float(premissa.get("frequencia_maxima") or frequencia)
        distribuicao_frequencia = FrequencyDistributionEngine.calcular(
            premissa.get("alcances_frequencia"),
            premissa.get("frequencia_minima_eficiente", 1),
            premissa.get("frequencia_maxima_eficiente", maximo_frequencia),
            alcance,
        )

        def dividir(numerador, denominador):
            return round(numerador / denominador, 2) if denominador else None

        return DeliveryResult(
            quantidade=quantidade, investimento=round(investimento, 2),
            audiencia_percentual=audiencia, alcance_percentual=alcance,
            alcance_pessoas=pessoas, frequencia=frequencia, grp=grp,
            impressoes=impressoes, cliques=round(cliques, 2),
            conversoes=round(conversoes, 2), retorno=round(retorno, 2),
            cpp=dividir(investimento, grp),
            cpm=dividir(investimento * 1000, impressoes),
            cpc=dividir(investimento, cliques), cpa=dividir(investimento, conversoes),
            roi=dividir(retorno - investimento, investimento),
            excesso_frequencia=round(max(0, frequencia - maximo_frequencia), 2),
            distribuicao_frequencia=distribuicao_frequencia,
            confianca=str(premissa.get("confianca") or "INFORMADO").upper(),
            preco_tabela_unitario=custo.preco_tabela_unitario,
            desconto_percentual=custo.desconto_percentual,
            preco_liquido_unitario=custo.preco_liquido_unitario,
            custo_midia=custo.custo_midia,
            fee_tecnologia=custo.fee_tecnologia,
            fee_dados=custo.fee_dados,
            fee_verificacao=custo.fee_verificacao,
            fee_operacao=custo.fee_operacao,
            custo_total=custo.custo_total,
            restricoes_ativas=restricoes.limites_ativos,
        )

    @staticmethod
    def alcance_combinado(premissas):
        """Alcance sequencial sem aplicar independência silenciosamente."""
        acumulado = 0.0
        auditoria = []
        for indice, item in enumerate(premissas):
            alcance = float(item.get("alcance_percentual") or 0)
            incremental = item.get("alcance_incremental")
            if indice == 0:
                incremento = alcance
                metodo = "primeiro meio"
            elif incremental is not None:
                incremento = float(incremental)
                metodo = "incremental informado"
            elif item.get("permitir_independencia") is True:
                incremento = alcance * (1 - acumulado / 100)
                metodo = "hipótese de independência"
            else:
                auditoria.append({
                    "alcance_proprio": alcance,
                    "alcance_anterior": round(acumulado, 2),
                    "incremental": None,
                    "metodo": "indisponível sem superposição ou hipótese aprovada",
                    "confianca": "NAO_AVALIADA",
                })
                return None, auditoria
            antes = acumulado
            acumulado = min(100.0, acumulado + max(0, incremento))
            auditoria.append({
                "alcance_proprio": alcance, "alcance_anterior": round(antes, 2),
                "incremental": round(acumulado - antes, 2), "metodo": metodo,
                "confianca": (
                    "BAIXA"
                    if metodo == "hipótese de independência"
                    else str(item.get("confianca") or "NAO_AVALIADA").upper()
                ),
            })
        return round(acumulado, 2), auditoria

    @staticmethod
    def _data_contexto(valor):
        if isinstance(valor, date):
            return valor
        if valor:
            try:
                return date.fromisoformat(str(valor)[:10])
            except ValueError:
                return None
        return None

    @staticmethod
    def _contexto_grp(premissa):
        return ContextoMetrica(
            universo=premissa.get("universo"),
            publico_alvo=premissa.get("publico_alvo"),
            praca=premissa.get("praca"),
            inicio_referencia=MediaPlanEngine._data_contexto(
                premissa.get("inicio_referencia")
            ),
            fim_referencia=MediaPlanEngine._data_contexto(
                premissa.get("fim_referencia")
            ),
            metrica_nativa=str(premissa.get("metrica_nativa") or "GRP"),
            metodologia=premissa.get("metodologia"),
            granularidade=premissa.get("granularidade"),
        )

    @staticmethod
    def consolidar_grp(resultados, premissas):
        componentes = [
            {
                "inventario_id": premissa.get("inventario_id"),
                "grp": resultado.grp,
            }
            for resultado, premissa in zip(resultados, premissas)
        ]
        if len(resultados) <= 1:
            return (
                round(sum(item.grp for item in resultados), 2),
                {
                    "situacao": "COMPARAVEL",
                    "divergencias": [],
                    "componentes": componentes,
                },
            )

        contextos = [
            MediaPlanEngine._contexto_grp(premissa)
            for premissa in premissas
        ]
        situacao = SituacaoComparabilidade.COMPARAVEL
        divergencias = set()
        primeiro = contextos[0]
        for contexto in contextos[1:]:
            comparacao = comparar_contextos(primeiro, contexto)
            divergencias.update(comparacao.divergencias)
            if comparacao.situacao is SituacaoComparabilidade.INDETERMINADO:
                situacao = SituacaoComparabilidade.INDETERMINADO
            elif (
                comparacao.situacao is SituacaoComparabilidade.NAO_COMPARAVEL
                and situacao is not SituacaoComparabilidade.INDETERMINADO
            ):
                situacao = SituacaoComparabilidade.NAO_COMPARAVEL

        total = (
            round(sum(item.grp for item in resultados), 2)
            if situacao is SituacaoComparabilidade.COMPARAVEL
            else None
        )
        return total, {
            "situacao": situacao.value,
            "divergencias": sorted(divergencias),
            "componentes": componentes,
        }

    @staticmethod
    def consolidar(resultados, premissas):
        alcance, auditoria = MediaPlanEngine.alcance_combinado(premissas)
        grp, comparabilidade_grp = MediaPlanEngine.consolidar_grp(
            resultados,
            premissas,
        )
        frequencia = (
            round(grp / alcance, 2)
            if grp is not None and alcance
            else None
        )
        investimento = round(sum(item.investimento for item in resultados), 2)
        retorno = round(sum(item.retorno for item in resultados), 2)
        return {
            "alcance_liquido_percentual": alcance,
            "frequencia_combinada": frequencia,
            "grp_total": grp,
            "grp_por_meio": comparabilidade_grp["componentes"],
            "comparabilidade_grp": comparabilidade_grp,
            "investimento": investimento,
            "custo_midia": round(sum(item.custo_midia for item in resultados), 2),
            "fees": {
                "tecnologia": round(
                    sum(item.fee_tecnologia for item in resultados), 2
                ),
                "dados": round(sum(item.fee_dados for item in resultados), 2),
                "verificacao": round(
                    sum(item.fee_verificacao for item in resultados), 2
                ),
                "operacao": round(
                    sum(item.fee_operacao for item in resultados), 2
                ),
            },
            "custo_total": investimento,
            "impressoes": sum(item.impressoes for item in resultados),
            "cliques": round(sum(item.cliques for item in resultados), 2),
            "conversoes": round(sum(item.conversoes for item in resultados), 2),
            "retorno": retorno,
            "roi": round((retorno - investimento) / investimento, 4) if investimento else None,
            "excesso_frequencia_total": round(
                sum(item.excesso_frequencia for item in resultados), 2
            ),
            "saturacao_economica": None,
            "modelo_saturacao": {
                "situacao": "INDISPONIVEL",
                "motivo": (
                    "Excesso de frequência não equivale a saturação econômica; "
                    "é necessária uma curva de resposta calibrada."
                ),
            },
            "distribuicao_frequencia_por_meio": [
                {
                    "inventario_id": premissa.get("inventario_id"),
                    **item.distribuicao_frequencia,
                }
                for item, premissa in zip(resultados, premissas)
            ],
            "cobertura_jornada": round(
                sum(float(item.get("cobertura_jornada") or 0) for item in premissas)
                / len(premissas), 2
            ) if premissas else 0,
            "auditoria_alcance": auditoria,
        }
