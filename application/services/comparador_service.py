from domain.models.comparacao import ComparacaoResultado


class ComparadorService:

    CRITERIOS = {
        "alcance": ("alcance_liquido_percentual", True),
        "frequencia": ("frequencia_combinada", True),
        "conversoes": ("conversoes", True),
        "roi": ("roi", True),
        "jornada": ("cobertura_jornada", True),
        "saturacao": ("risco_saturacao", False),
        "investimento": ("investimento", False),
    }

    def comparar_configuravel(self, plano1, plano2, pesos):
        dados = [
            dict(plano1.resultados_consolidados or {}),
            dict(plano2.resultados_consolidados or {}),
        ]
        if not dados[0] or not dados[1]:
            raise ValueError("Os dois planos precisam ter cálculos cross-media auditáveis.")
        total = sum(float(valor) for valor in pesos.values())
        if abs(total - 100) > 0.01:
            raise ValueError("Os pesos da comparação devem somar 100%.")
        scores = [0.0, 0.0]
        detalhes = []
        for criterio, peso in pesos.items():
            campo, maior_melhor = self.CRITERIOS[criterio]
            valores = [float(item.get(campo) or 0) for item in dados]
            referencia = max(valores) if maior_melhor else max(valores)
            if maior_melhor:
                notas = [v / referencia * 100 if referencia else 0 for v in valores]
            else:
                notas = [min(valores) / v * 100 if v else 100 for v in valores]
            for indice in range(2):
                scores[indice] += notas[indice] * float(peso) / 100
            detalhes.append({
                "criterio": criterio, "plano_a": valores[0], "plano_b": valores[1],
                "peso": peso, "melhor": "A" if notas[0] > notas[1] else "B" if notas[1] > notas[0] else "Empate",
            })
        vencedor = "Plano A" if scores[0] > scores[1] else "Plano B" if scores[1] > scores[0] else "Empate"
        vantagens = [d["criterio"] for d in detalhes if d["melhor"] == vencedor[-1:]]
        justificativa = (
            f"{vencedor} é mais aderente aos pesos configurados"
            + (f", com vantagem em {', '.join(vantagens)}." if vantagens else ".")
        )
        return {
            "vencedor": vencedor, "scores": [round(s, 2) for s in scores],
            "detalhes": detalhes, "justificativa": justificativa,
        }

    # =====================================================
    # COMPARAÇÃO
    # =====================================================

    def comparar(

        self,

        plano1,

        forecast1,

        plano2,

        forecast2

    ):

        score1 = self._score_medio(

            plano1

        )

        score2 = self._score_medio(

            plano2

        )

        conv1 = self._conversoes(

            forecast1

        )

        conv2 = self._conversoes(

            forecast2

        )

        inv1 = plano1.verba_total

        inv2 = plano2.verba_total

        if (

            score1 > score2

            and

            conv1 >= conv2

        ):

            vencedor = plano1.campanha

            justificativa = (

                "Maior score estratégico e desempenho previsto."

            )

        elif (

            score2 > score1

            and

            conv2 >= conv1

        ):

            vencedor = plano2.campanha

            justificativa = (

                "Maior score estratégico e desempenho previsto."

            )

        elif conv1 > conv2:

            vencedor = plano1.campanha

            justificativa = (

                "Maior potencial de conversão."

            )

        elif conv2 > conv1:

            vencedor = plano2.campanha

            justificativa = (

                "Maior potencial de conversão."

            )

        else:

            vencedor = "Empate"

            justificativa = (

                "Os cenários apresentam desempenho equivalente."

            )

        return ComparacaoResultado(

            vencedor=vencedor,

            score_plano_1=round(

                score1,

                2

            ),

            score_plano_2=round(

                score2,

                2

            ),

            conversoes_plano_1=round(

                conv1,

                2

            ),

            conversoes_plano_2=round(

                conv2,

                2

            ),

            investimento_plano_1=round(

                inv1,

                2

            ),

            investimento_plano_2=round(

                inv2,

                2

            ),

            justificativa=justificativa

        )

    # =====================================================
    # SCORE MÉDIO
    # =====================================================

    def _score_medio(

        self,

        plano

    ):

        if not plano.itens:

            return 0

        return sum(

            item.score

            for item in plano.itens

        ) / len(

            plano.itens

        )

    # =====================================================
    # CONVERSÕES
    # =====================================================

    def _conversoes(

        self,

        forecast

    ):

        return sum(

            item.conversoes

            for item in forecast

        )
