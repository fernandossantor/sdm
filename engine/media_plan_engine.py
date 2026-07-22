"""Cálculos auditáveis de entrega cross-media.

O motor não inventa audiência, alcance ou frequência. Cada item precisa trazer
as premissas mínimas e a interface deve identificar a origem de cada valor.
"""

from dataclasses import dataclass
from math import ceil
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
    confianca: str


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
        if quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa.")
        minimo = float(premissa.get("quantidade_minima") or 0)
        maximo = premissa.get("quantidade_maxima")
        if quantidade < minimo:
            if modo == "METAS":
                quantidade = minimo
            else:
                raise ValueError("A quantidade está abaixo do piso informado.")
        verba_minima = float(premissa.get("verba_minima") or 0)
        if modo == "METAS" and verba_minima > 0:
            if preco <= 0:
                raise ValueError(
                    "Informe um preço maior que zero para aplicar o piso de verba."
                )
            quantidade = max(quantidade, ceil(verba_minima / preco))
        if maximo is not None and quantidade > float(maximo):
            if modo == "METAS":
                quantidade = float(maximo)
            else:
                raise ValueError("A quantidade excede o teto informado.")
        quantidade = int(ceil(quantidade)) if modo == "METAS" else int(quantidade)
        investimento = quantidade * preco
        verba_maxima = premissa.get("verba_maxima")
        if investimento < verba_minima:
            raise ValueError(f"O investimento {investimento:.2f} está abaixo do piso {verba_minima:.2f}.")
        if verba_maxima is not None and investimento > float(verba_maxima):
            raise ValueError(f"O investimento {investimento:.2f} excede o teto {float(verba_maxima):.2f}.")
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
            confianca=str(premissa.get("confianca") or "INFORMADO").upper(),
        )

    @staticmethod
    def alcance_combinado(premissas):
        """Alcance líquido sequencial: incremental explícito ou independência."""
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
            else:
                incremento = alcance * (1 - acumulado / 100)
                metodo = "estimativa por independência"
            antes = acumulado
            acumulado = min(100.0, acumulado + max(0, incremento))
            auditoria.append({
                "alcance_proprio": alcance, "alcance_anterior": round(antes, 2),
                "incremental": round(acumulado - antes, 2), "metodo": metodo,
            })
        return round(acumulado, 2), auditoria

    @staticmethod
    def consolidar(resultados, premissas):
        alcance, auditoria = MediaPlanEngine.alcance_combinado(premissas)
        grp = round(sum(item.grp for item in resultados), 2)
        frequencia = round(grp / alcance, 2) if alcance else 0
        investimento = round(sum(item.investimento for item in resultados), 2)
        retorno = round(sum(item.retorno for item in resultados), 2)
        return {
            "alcance_liquido_percentual": alcance,
            "frequencia_combinada": frequencia,
            "grp_total": grp,
            "investimento": investimento,
            "impressoes": sum(item.impressoes for item in resultados),
            "cliques": round(sum(item.cliques for item in resultados), 2),
            "conversoes": round(sum(item.conversoes for item in resultados), 2),
            "retorno": retorno,
            "roi": round((retorno - investimento) / investimento, 4) if investimento else None,
            "risco_saturacao": round(sum(item.excesso_frequencia for item in resultados), 2),
            "cobertura_jornada": round(
                sum(float(item.get("cobertura_jornada") or 0) for item in premissas)
                / len(premissas), 2
            ) if premissas else 0,
            "auditoria_alcance": auditoria,
        }
