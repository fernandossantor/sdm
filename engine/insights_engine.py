class InsightsEngine:

    """
    Geração automática de insights estratégicos.
    """

    # =====================================================
    # INTERFACE
    # =====================================================

    def gerar(self, plano, forecast=None):

        if not plano.itens:
            return ["Nenhum inventário selecionado."]

        insights = []

        insights.extend(self._insights_concentracao(plano))
        insights.extend(self._insights_diversidade(plano))
        insights.extend(self._insights_papeis(plano))
        insights.extend(self._insights_score(plano))
        insights.extend(self._insights_ambientes(plano))

        if forecast:
            insights.extend(
                self._insights_forecast(forecast)
            )

        return insights

    # =====================================================
    # CONCENTRAÇÃO
    # =====================================================

    def _insights_concentracao(self, plano):

        itens = plano.itens

        maior = max(
            itens,
            key=lambda i: i.verba
        )

        if maior.percentual >= 50:
            return [
                f"Alta concentração de investimento em {maior.inventario} ({maior.percentual:.1f}%)."
            ]

        if maior.percentual >= 35:
            return [
                f"{maior.inventario} concentra parcela relevante da verba."
            ]

        return [
            "Boa distribuição de investimento entre os inventários."
        ]

    # =====================================================
    # DIVERSIDADE
    # =====================================================

    def _insights_diversidade(self, plano):

        ambientes = {
            i.ambiente.lower()
            for i in plano.itens
        }

        qtd = len(ambientes)

        if qtd == 1:
            return [
                "O plano utiliza apenas um ambiente de mídia."
            ]

        if qtd == 2:
            return [
                "Diversidade moderada de ambientes."
            ]

        return [
            "Boa diversidade entre ambientes."
        ]

    # =====================================================
    # PAPÉIS
    # =====================================================

    def _insights_papeis(self, plano):

        principais = [
            i
            for i in plano.itens
            if i.papel.upper() == "PRINCIPAL"
        ]

        if len(principais) == 1:
            return [
                "Existe dependência de um único canal principal."
            ]

        if len(principais) >= 4:
            return [
                "Plano distribuído entre diversos canais principais."
            ]

        return []

    # =====================================================
    # SCORE
    # =====================================================

    def _insights_score(self, plano):

        media = (
            sum(i.score for i in plano.itens)
            / len(plano.itens)
        )

        if media >= 90:
            return [
                "Excelente aderência estratégica."
            ]

        if media >= 75:
            return [
                "Boa consistência estratégica."
            ]

        return [
            "Há espaço para melhorar a composição estratégica do plano."
        ]

    # =====================================================
    # AMBIENTES
    # =====================================================

    def _insights_ambientes(self, plano):

        ambientes = [
            i.ambiente.lower()
            for i in plano.itens
        ]

        insights = []

        if ambientes.count("social") >= 3:
            insights.append(
                "Forte presença em mídias sociais."
            )

        if "search" not in ambientes:
            insights.append(
                "Não há canais de Search no plano."
            )

        if "retail" in ambientes:
            insights.append(
                "Retail Media pode acelerar conversões de fundo de funil."
            )

        if not any(
            "video" in a
            for a in ambientes
        ):
            insights.append(
                "Não há inventários de vídeo para ampliar alcance."
            )

        return insights

    # =====================================================
    # FORECAST
    # =====================================================

    def _insights_forecast(self, forecast):

        investimento = sum(
            f.verba
            for f in forecast
        )

        conversoes = sum(
            f.conversoes
            for f in forecast
        )

        impressoes = sum(
            f.impressoes
            for f in forecast
        )

        cliques = sum(
            f.cliques
            for f in forecast
        )

        insights = []

        if conversoes:

            cpa = investimento / conversoes

            insights.append(
                f"CPA médio estimado de R$ {cpa:.2f}."
            )

        else:

            insights.append(
                "Não foram estimadas conversões."
            )

        if impressoes:

            ctr = (
                cliques
                / impressoes
            ) * 100

            insights.append(
                f"CTR médio estimado de {ctr:.2f}%."
            )

        return insights