"""Preparação e consolidação de eventos para atribuição."""

from collections import defaultdict
import math

from engine.attribution_engine import AttributionEngine


class AttributionService:
    def __init__(self):
        self.engine = AttributionEngine()

    def calcular(self, eventos, modelo="LINEAR", janela_dias=30):
        conversoes = {}
        toques = defaultdict(list)
        for evento in eventos:
            valor_id = evento.get("conversao_id")
            identificador = (
                ""
                if valor_id is None
                or (isinstance(valor_id, float) and math.isnan(valor_id))
                else str(valor_id).strip()
            )
            toques[identificador].append({
                "canal": evento.get("canal"),
                "instante": evento.get("instante_toque"),
            })
            if identificador not in conversoes:
                conversoes[identificador] = {
                    "id": identificador,
                    "instante": evento.get("instante_conversao"),
                    "receita": evento.get("receita") or 0,
                }

        entrada = [
            {**conversao, "toques": toques[identificador]}
            for identificador, conversao in conversoes.items()
        ]
        resultado = self.engine.calcular(entrada, modelo, janela_dias)
        por_canal = defaultdict(
            lambda: {"credito": 0.0, "receita_atribuida": 0.0}
        )
        for linha in resultado["creditos"]:
            canal = por_canal[linha["canal"]]
            canal["credito"] += linha["credito"]
            canal["receita_atribuida"] += linha["receita_atribuida"]
        resultado["por_canal"] = [
            {
                "canal": canal,
                "credito_em_conversoes": round(valores["credito"], 10),
                "receita_atribuida": round(valores["receita_atribuida"], 2),
            }
            for canal, valores in por_canal.items()
        ]
        resultado["conversoes_elegiveis"] = len({
            linha["conversao_id"] for linha in resultado["creditos"]
        })
        tipos = defaultdict(set)
        for linha in resultado["creditos"]:
            tipos[linha["tipo_conversao"]].add(linha["conversao_id"])
        resultado["conversoes_diretas"] = len(tipos["DIRETA"])
        resultado["conversoes_assistidas"] = len(tipos["ASSISTIDA"])
        return resultado
