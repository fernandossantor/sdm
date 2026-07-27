"""Cenários condicionais e auditáveis para entrega e resposta."""


class SensitivityEngine:
    VERSAO = "sensibilidade-multiplicativa-v1"
    VARIAVEIS = ("impressoes", "ctr", "taxa_conversao")

    @staticmethod
    def _fator(configuracao, variavel):
        variacao = float(configuracao.get(variavel, 0))
        if variacao < -100:
            raise ValueError(
                f"A variação de {variavel} não pode ser menor que -100%."
            )
        return 1 + variacao / 100

    @staticmethod
    def _taxa_base(item, campo_premissa, numerador, denominador):
        premissas = getattr(item, "premissas", None) or {}
        informado = premissas.get(campo_premissa)
        if informado is not None:
            return float(informado) / 100
        if numerador is not None and denominador is not None and denominador > 0:
            return float(numerador) / float(denominador)
        return None

    def simular_item(self, item, configuracao):
        impressoes_base = getattr(item, "impressoes_estimadas", None)
        cliques_base = getattr(item, "cliques_estimados", None)
        conversoes_base = getattr(item, "conversoes_estimadas", None)
        ctr_base = self._taxa_base(
            item, "ctr", cliques_base, impressoes_base
        )
        conversao_base = self._taxa_base(
            item, "taxa_conversao", conversoes_base, cliques_base
        )
        lacunas = []

        impressoes = (
            float(impressoes_base)
            * self._fator(configuracao, "impressoes")
            if impressoes_base is not None
            else None
        )
        if impressoes is None:
            lacunas.append("impressões do plano")
        ctr = (
            ctr_base * self._fator(configuracao, "ctr")
            if ctr_base is not None
            else None
        )
        if ctr is None:
            lacunas.append("CTR explícito")
        cliques = impressoes * ctr if impressoes is not None and ctr is not None else None
        taxa_conversao = (
            conversao_base * self._fator(configuracao, "taxa_conversao")
            if conversao_base is not None
            else None
        )
        if taxa_conversao is None:
            lacunas.append("taxa de conversão explícita")
        conversoes = (
            cliques * taxa_conversao
            if cliques is not None and taxa_conversao is not None
            else None
        )
        return {
            "inventario": item.inventario,
            "investimento": float(item.verba),
            "impressoes": round(impressoes) if impressoes is not None else None,
            "ctr_percentual": round(ctr * 100, 4) if ctr is not None else None,
            "cliques": round(cliques, 2) if cliques is not None else None,
            "taxa_conversao_percentual": (
                round(taxa_conversao * 100, 4)
                if taxa_conversao is not None else None
            ),
            "conversoes": (
                round(conversoes, 2) if conversoes is not None else None
            ),
            "lacunas": lacunas,
        }

    @staticmethod
    def _total_completo(itens, campo):
        valores = [item[campo] for item in itens]
        if not valores or any(valor is None for valor in valores):
            return None
        return round(sum(valores), 2)

    def simular(self, plano, cenarios):
        resultado = {}
        for nome, configuracao in cenarios.items():
            configuracao = {
                variavel: float(configuracao.get(variavel, 0))
                for variavel in self.VARIAVEIS
            }
            itens = [
                self.simular_item(item, configuracao)
                for item in plano.itens
            ]
            resultado[nome] = {
                "cenario": nome,
                "metodo": "CENARIO_CONDICIONAL_MULTIPLICATIVO",
                "versao": self.VERSAO,
                "premissas_variacao_percentual": configuracao,
                "itens": itens,
                "investimento": round(sum(item["investimento"] for item in itens), 2),
                "impressoes": self._total_completo(itens, "impressoes"),
                "cliques": self._total_completo(itens, "cliques"),
                "conversoes": self._total_completo(itens, "conversoes"),
                "limitacoes": [
                    "Cenário condicional, não intervalo estatístico.",
                    "Variações são premissas do usuário, não benchmarks universais.",
                    "Não modela saturação nem interação entre variáveis.",
                ],
            }
        return resultado
