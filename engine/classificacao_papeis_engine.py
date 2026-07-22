class ClassificacaoPapeisEngine:

    PESOS = {
        "afinidade": 0.40,
        "consumo": 0.35,
        "cobertura": 0.25,
    }

    def calcular_score(self, afinidade, cobertura, consumo, objetivo=None, jornada=0, pesos=None):

        valores = {
            "afinidade": afinidade,
            "cobertura": cobertura,
            "consumo": consumo,
        }

        pesos = pesos or self.PESOS
        if jornada and "jornada" not in pesos:
            pesos = {"afinidade": .30, "consumo": .25, "cobertura": .25, "jornada": .20}
        valores["jornada"] = jornada
        return round(
            sum(
                valores[criterio] * peso
                for criterio, peso in pesos.items()
            ),
            2,
        )

    def classificar(self, scores):

        ranking = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        resultado = []

        for posicao, (meio, score) in enumerate(ranking, start=1):
            if posicao == 1:
                papel = "Principal"
            elif posicao == 2:
                papel = "Complementar"
            else:
                papel = "Apoio"

            resultado.append(
                {
                    "posicao": posicao,
                    "meio": meio,
                    "papel": papel,
                    "score": score,
                }
            )

        return resultado
