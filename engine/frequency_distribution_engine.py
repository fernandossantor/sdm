"""Distribuição auditável de frequência a partir de alcances N+ informados."""


class FrequencyDistributionEngine:

    @staticmethod
    def calcular(
        alcances,
        frequencia_minima_eficiente,
        frequencia_maxima_eficiente,
        alcance_total=None,
    ):
        if not alcances:
            return {
                "situacao": "INDISPONIVEL",
                "motivo": "Alcances por frequência (N+) não informados.",
            }

        try:
            faixas = {
                int(str(chave).replace("+", "")): float(valor)
                for chave, valor in alcances.items()
            }
        except (TypeError, ValueError):
            raise ValueError("As faixas de frequência devem usar limiares N+.")

        minimo = int(frequencia_minima_eficiente)
        maximo = int(frequencia_maxima_eficiente)
        if minimo < 1 or maximo < minimo:
            raise ValueError("A faixa eficiente de frequência é inválida.")
        necessarias = {1, minimo, maximo + 1}
        ausentes = sorted(necessarias - set(faixas))
        if ausentes:
            raise ValueError(
                "Informe os alcances "
                + ", ".join(f"{valor}+" for valor in ausentes)
                + " para calcular a distribuição."
            )
        if any(valor < 0 or valor > 100 for valor in faixas.values()):
            raise ValueError("Alcances N+ devem estar entre 0% e 100%.")

        ordenadas = sorted(faixas.items())
        for (limiar_anterior, anterior), (limiar, atual) in zip(
            ordenadas, ordenadas[1:]
        ):
            if atual > anterior:
                raise ValueError(
                    f"Alcance {limiar}+ não pode superar {limiar_anterior}+."
                )
        if (
            alcance_total is not None
            and abs(faixas[1] - float(alcance_total)) > 0.01
        ):
            raise ValueError(
                "Alcance 1+ deve ser igual ao alcance do meio informado."
            )

        alcance_1mais = faixas[1]
        subexposta = alcance_1mais - faixas[minimo]
        sobre_exposta = faixas[maximo + 1]
        faixa_eficiente = faixas[minimo] - sobre_exposta

        def entre_alcancados(valor):
            return round(valor / alcance_1mais * 100, 2) if alcance_1mais else 0

        return {
            "situacao": "CALCULADA",
            "metodo": "DISTRIBUICAO_ALCANCE_N_MAIS",
            "alcances_percentuais": dict(sorted(faixas.items())),
            "frequencia_minima_eficiente": minimo,
            "frequencia_maxima_eficiente": maximo,
            "subexposta_percentual": round(subexposta, 2),
            "faixa_eficiente_percentual": round(faixa_eficiente, 2),
            "sobre_exposta_percentual": round(sobre_exposta, 2),
            "entre_alcancados": {
                "subexposta_percentual": entre_alcancados(subexposta),
                "faixa_eficiente_percentual": entre_alcancados(faixa_eficiente),
                "sobre_exposta_percentual": entre_alcancados(sobre_exposta),
            },
            "saturacao_economica": None,
        }
