"""Visões reconciliadas do cronograma de mídia."""

from collections import defaultdict
from datetime import datetime


class ScheduleService:
    CAMPOS_FIXOS = {
        "Inventário",
        "ID do inventário",
        "Meio",
        "Ambiente",
        "Papel",
        "Unidade",
        "Total",
        "Investimento total",
    }

    @staticmethod
    def _inicio_semana(rotulo):
        try:
            trecho = str(rotulo).split("·", 1)[1].split("–", 1)[0].strip()
            return datetime.strptime(trecho, "%d/%m/%Y").date()
        except (IndexError, ValueError):
            return None

    def consolidar(self, plano):
        semanal = defaultdict(
            lambda: {"Quantidade": 0, "Investimento": 0.0}
        )
        mensal = defaultdict(
            lambda: {"Quantidade": 0, "Investimento": 0.0}
        )
        por_meio = defaultdict(
            lambda: {"Quantidade": 0, "Investimento": 0.0}
        )

        for linha in plano.cronograma or []:
            semanas = [
                chave
                for chave in linha
                if chave not in self.CAMPOS_FIXOS
                and str(chave).startswith("S")
            ]
            quantidade_total = int(linha.get("Total") or 0)
            investimento_total = float(linha.get("Investimento total") or 0)
            quantidades = [int(linha.get(chave) or 0) for chave in semanas]
            investimentos = []
            acumulado = 0.0
            for indice, quantidade in enumerate(quantidades):
                if indice == len(quantidades) - 1:
                    valor = investimento_total - acumulado
                elif quantidade_total:
                    valor = round(
                        investimento_total * quantidade / quantidade_total,
                        2,
                    )
                    acumulado += valor
                else:
                    valor = 0.0
                investimentos.append(round(valor, 2))

            for chave, quantidade, investimento in zip(
                semanas, quantidades, investimentos
            ):
                semanal[chave]["Quantidade"] += quantidade
                semanal[chave]["Investimento"] += investimento
                inicio = self._inicio_semana(chave)
                mes = inicio.strftime("%Y-%m") if inicio else "Sem período"
                mensal[mes]["Quantidade"] += quantidade
                mensal[mes]["Investimento"] += investimento

            meio = linha.get("Meio") or "Sem meio"
            por_meio[meio]["Quantidade"] += quantidade_total
            por_meio[meio]["Investimento"] += investimento_total

        def linhas(agrupado, campo):
            return [
                {
                    campo: chave,
                    "Quantidade": valores["Quantidade"],
                    "Investimento": round(valores["Investimento"], 2),
                }
                for chave, valores in agrupado.items()
            ]

        quantidade_plano = sum(
            int(round(float(item.quantidade_estimada or 0)))
            for item in plano.itens
        )
        investimento_plano = round(
            sum(float(item.custo_total or item.verba or 0) for item in plano.itens),
            2,
        )
        quantidade_cronograma = sum(
            valores["Quantidade"] for valores in semanal.values()
        )
        investimento_cronograma = round(
            sum(valores["Investimento"] for valores in semanal.values()),
            2,
        )
        return {
            "semanal": linhas(semanal, "Semana"),
            "mensal": linhas(mensal, "Mês"),
            "por_meio": linhas(por_meio, "Meio"),
            "reconciliacao": {
                "quantidade_plano": quantidade_plano,
                "quantidade_cronograma": quantidade_cronograma,
                "investimento_plano": investimento_plano,
                "investimento_cronograma": investimento_cronograma,
                "quantidade_reconciliada": (
                    quantidade_plano == quantidade_cronograma
                ),
                "investimento_reconciliado": (
                    abs(investimento_plano - investimento_cronograma) <= 0.01
                ),
            },
        }
