class RecommendationEngine:

    # ==========================================================
    # RECOMENDAÇÕES
    # ==========================================================

    def recomendar(

        self,

        item

    ):

        recomendacoes = []

        #
        # Objetivo
        #

        if item["objetivo"] >= 90:

            recomendacoes.append(

                "Elevada aderência ao objetivo da campanha."

            )

        elif item["objetivo"] >= 70:

            recomendacoes.append(

                "Boa aderência ao objetivo."

            )

        else:

            recomendacoes.append(

                "Contribuição limitada para o objetivo."

            )

        #
        # KPI
        #

        if item["kpi"] >= 90:

            recomendacoes.append(

                "Excelente potencial para o KPI principal."

            )

        elif item["kpi"] >= 70:

            recomendacoes.append(

                "Bom desempenho esperado para o KPI."

            )

        else:

            recomendacoes.append(

                "Impacto reduzido sobre o KPI."

            )

        #
        # Audiência
        #

        if item["audiencia"] >= 90:

            recomendacoes.append(

                "Excelente afinidade com a audiência."

            )

        elif item["audiencia"] >= 70:

            recomendacoes.append(

                "Boa cobertura da audiência."

            )

        else:

            recomendacoes.append(

                "Cobertura limitada da audiência."

            )

        #
        # Métricas
        #

        if item["metricas"] >= 105:

            recomendacoes.append(

                "Indicadores operacionais acima da média."

            )

        elif item["metricas"] >= 100:

            recomendacoes.append(

                "Boas métricas operacionais."

            )

        else:

            recomendacoes.append(

                "Métricas operacionais medianas."

            )

        #
        # Papel
        #

        papel = item["papel"]

        if papel == "PRINCIPAL":

            recomendacoes.append(

                "Recomendado como canal principal do plano."

            )

        elif papel == "COMPLEMENTAR":

            recomendacoes.append(

                "Recomendado para ampliar cobertura e frequência."

            )

        elif papel == "APOIO":

            recomendacoes.append(

                "Utilizar como reforço tático."

            )

        else:

            recomendacoes.append(

                "Utilização opcional."

            )

        return recomendacoes

    # ==========================================================
    # RESUMO EXECUTIVO
    # ==========================================================

    def resumo(

        self,

        ranking

    ):

        principais = len(

            [

                i

                for i in ranking

                if i["papel"] == "PRINCIPAL"

            ]

        )

        complementares = len(

            [

                i

                for i in ranking

                if i["papel"] == "COMPLEMENTAR"

            ]

        )

        media = round(

            sum(

                i["score"]

                for i in ranking

            )

            /

            len(ranking),

            2

        )

        texto = []

        texto.append(

            f"Score médio do plano: {media}."

        )

        texto.append(

            f"{principais} inventários classificados como PRINCIPAIS."

        )

        texto.append(

            f"{complementares} inventários classificados como COMPLEMENTARES."

        )

        if media >= 90:

            texto.append(

                "Plano altamente recomendado."

            )

        elif media >= 75:

            texto.append(

                "Plano consistente."

            )

        else:

            texto.append(

                "Plano necessita otimização."

            )

        return texto

    # ==========================================================
    # RISCOS
    # ==========================================================

    def riscos(

        self,

        ranking

    ):

        riscos = []

        if len(ranking) < 3:

            riscos.append(

                "Baixa diversidade de inventários."

            )

        principais = len(

            [

                i

                for i in ranking

                if i["papel"] == "PRINCIPAL"

            ]

        )

        if principais == 1:

            riscos.append(

                "Dependência excessiva de um único canal."

            )

        media = (

            sum(

                i["score"]

                for i in ranking

            )

            /

            len(ranking)

        )

        if media < 70:

            riscos.append(

                "Baixa aderência estratégica do plano."

            )

        return riscos