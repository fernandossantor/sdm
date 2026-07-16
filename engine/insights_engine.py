class InsightsEngine:

    # =====================================================
    # GERAR INSIGHTS
    # =====================================================

    def gerar(

        self,

        plano,

        forecast=None

    ):

        insights = []

        itens = plano.itens

        if not itens:

            return [

                "Nenhum inventário selecionado."

            ]

        #
        # Concentração de verba
        #

        maior = max(

            itens,

            key=lambda x: x.verba

        )

        if maior.percentual >= 50:

            insights.append(

                f"Alta concentração de investimento em {maior.inventario} ({maior.percentual:.1f}%)."

            )

        elif maior.percentual >= 35:

            insights.append(

                f"{maior.inventario} concentra parcela relevante da verba."

            )

        #
        # Diversidade
        #

        ambientes = {

            i.ambiente

            for i in itens

        }

        if len(ambientes) == 1:

            insights.append(

                "O plano utiliza apenas um ambiente de mídia."

            )

        elif len(ambientes) == 2:

            insights.append(

                "Diversidade moderada de ambientes."

            )

        else:

            insights.append(

                "Boa diversidade entre ambientes."

            )

        #
        # Papéis
        #

        principais = [

            i

            for i in itens

            if i.papel == "PRINCIPAL"

        ]

        if len(principais) == 1:

            insights.append(

                "Existe dependência de um único canal principal."

            )

        elif len(principais) >= 4:

            insights.append(

                "Plano distribuído entre diversos canais principais."

            )

        #
        # Score
        #

        media = sum(

            i.score

            for i in itens

        ) / len(itens)

        if media >= 90:

            insights.append(

                "Excelente aderência estratégica."

            )

        elif media >= 75:

            insights.append(

                "Boa consistência estratégica."

            )

        else:

            insights.append(

                "Há espaço para melhorar a composição do plano."

            )

        #
        # Forecast
        #

        if forecast:

            conversoes = sum(

                f.conversoes

                for f in forecast

            )

            investimento = sum(

                f.verba

                for f in forecast

            )

            if conversoes > 0:

                cpa = investimento / conversoes

                insights.append(

                    f"CPA médio estimado de R$ {cpa:.2f}."

                )

            else:

                insights.append(

                    "Não foram estimadas conversões."

                )

        #
        # Social
        #

        social = len(

            [

                i

                for i in itens

                if i.ambiente.lower() == "social"

            ]

        )

        if social >= 3:

            insights.append(

                "Forte presença em mídias sociais."

            )

        #
        # Search
        #

        search = len(

            [

                i

                for i in itens

                if i.ambiente.lower() == "search"

            ]

        )

        if search == 0:

            insights.append(

                "Não há canais de Search no plano."

            )

        #
        # Retail
        #

        retail = len(

            [

                i

                for i in itens

                if i.ambiente.lower() == "retail"

            ]

        )

        if retail > 0:

            insights.append(

                "Retail Media pode acelerar conversões de fundo de funil."

            )

        #
        # Vídeo
        #

        video = len(

            [

                i

                for i in itens

                if "video" in i.ambiente.lower()

            ]

        )

        if video == 0:

            insights.append(

                "Não há inventários de vídeo para ampliar alcance."

            )

        return insights