class ClassificacaoPapeisEngine:

    PESOS = {
        "afinidade": 0.40,
        "consumo": 0.35,
        "cobertura": 0.25,
    }

    def calcular_score(self, afinidade, cobertura, consumo, objetivo=None):

        valores = {
            "afinidade": afinidade,
            "cobertura": cobertura,
            "consumo": consumo,
        }

        return round(
            sum(
                valores[criterio] * peso
                for criterio, peso in self.PESOS.items()
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
