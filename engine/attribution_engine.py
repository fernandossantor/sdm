"""Atribuição baseada em regras, com crédito auditável por conversão."""

from datetime import datetime, timedelta, timezone
import math


class AttributionEngine:
    MODELOS = {
        "PRIMEIRO_TOQUE",
        "ULTIMO_TOQUE",
        "LINEAR",
        "POSICIONAL",
    }

    @staticmethod
    def _data(valor):
        if isinstance(valor, datetime):
            resultado = valor
        else:
            resultado = datetime.fromisoformat(str(valor).replace("Z", "+00:00"))
        if resultado.tzinfo is not None:
            resultado = (
                resultado.astimezone(timezone.utc).replace(tzinfo=None)
            )
        return resultado

    @staticmethod
    def _texto(valor):
        if valor is None or (
            isinstance(valor, float) and math.isnan(valor)
        ):
            return ""
        return str(valor).strip()

    @staticmethod
    def _pesos(modelo, quantidade):
        if quantidade == 1:
            return [1.0]
        if modelo == "PRIMEIRO_TOQUE":
            return [1.0] + [0.0] * (quantidade - 1)
        if modelo == "ULTIMO_TOQUE":
            return [0.0] * (quantidade - 1) + [1.0]
        if modelo == "POSICIONAL":
            if quantidade == 2:
                return [0.5, 0.5]
            intermediario = 0.2 / (quantidade - 2)
            return [0.4] + [intermediario] * (quantidade - 2) + [0.4]
        return [1.0 / quantidade] * quantidade

    def calcular(self, conversoes, modelo="LINEAR", janela_dias=30):
        if modelo not in self.MODELOS:
            raise ValueError("Modelo de atribuição inválido.")
        if int(janela_dias) <= 0:
            raise ValueError("A janela de atribuição deve ser positiva.")

        creditos = []
        excluidas = []
        limite = timedelta(days=int(janela_dias))
        for conversao in conversoes:
            identificador = self._texto(conversao.get("id"))
            if not identificador:
                excluidas.append({
                    "conversao_id": "",
                    "motivo": "Conversão sem identificador.",
                })
                continue
            try:
                instante_conversao = self._data(conversao["instante"])
            except (KeyError, TypeError, ValueError):
                excluidas.append({
                    "conversao_id": identificador,
                    "motivo": "Data da conversão ausente ou inválida.",
                })
                continue

            elegiveis = []
            for toque in conversao.get("toques") or []:
                try:
                    instante_toque = self._data(toque["instante"])
                except (KeyError, TypeError, ValueError):
                    continue
                canal = self._texto(toque.get("canal"))
                if (
                    canal
                    and instante_toque <= instante_conversao
                    and instante_conversao - instante_toque <= limite
                ):
                    elegiveis.append((instante_toque, canal))
            elegiveis.sort(key=lambda item: item[0])
            if not elegiveis:
                excluidas.append({
                    "conversao_id": identificador,
                    "motivo": "Nenhum toque elegível dentro da janela.",
                })
                continue

            pesos = self._pesos(modelo, len(elegiveis))
            pesos = [round(peso, 10) for peso in pesos]
            pesos[-1] = round(pesos[-1] + 1.0 - sum(pesos), 10)
            receita_bruta = conversao.get("receita")
            receita = (
                0.0
                if receita_bruta is None
                or (
                    isinstance(receita_bruta, float)
                    and math.isnan(receita_bruta)
                )
                else float(receita_bruta)
            )
            tipo = "DIRETA" if len(elegiveis) == 1 else "ASSISTIDA"
            receitas = [round(receita * peso, 2) for peso in pesos]
            receitas[-1] = round(
                receitas[-1] + receita - sum(receitas),
                2,
            )
            for (instante, canal), peso, receita_atribuida in zip(
                elegiveis, pesos, receitas
            ):
                creditos.append({
                    "conversao_id": identificador,
                    "canal": canal,
                    "instante_toque": instante.isoformat(),
                    "credito": round(peso, 10),
                    "receita_atribuida": receita_atribuida,
                    "tipo_conversao": tipo,
                })

        reconciliacao = []
        for conversao_id in {
            linha["conversao_id"] for linha in creditos
        }:
            total = sum(
                linha["credito"]
                for linha in creditos
                if linha["conversao_id"] == conversao_id
            )
            reconciliacao.append({
                "conversao_id": conversao_id,
                "credito_total": round(total, 10),
                "reconciliado": abs(total - 1.0) <= 1e-9,
            })

        return {
            "modelo": modelo,
            "janela_dias": int(janela_dias),
            "creditos": creditos,
            "conversoes_excluidas": excluidas,
            "reconciliacao": reconciliacao,
            "todos_creditos_reconciliados": all(
                item["reconciliado"] for item in reconciliacao
            ),
            "limitacoes": [
                "O resultado depende da identidade e dos eventos disponíveis.",
                "Canais offline ou não observáveis podem estar sub-representados.",
                "Receita atribuída distribui crédito e não mede incrementalidade.",
            ],
        }
