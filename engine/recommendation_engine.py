class RecommendationEngine:

    """
    Geração de recomendações estratégicas,
    resumo executivo e análise de riscos.
    """

    # =====================================================
    # RECOMENDAÇÕES
    # =====================================================

    def _valor(
        self,
        item,
        campo,
        default=None,
    ):

        if isinstance(
            item,
            dict,
        ):

            return item.get(
                campo,
                default,
            )

        return getattr(
            item,
            campo,
            default,
        )


    def recomendar(self, decisao):

        recomendacoes = []

        score = self._valor(
            decisao,
            "score",
            0,
        )

        papel = self._valor(
            decisao,
            "papel",
            "",
        )

        confianca = self._valor(
            decisao,
            "confianca",
            score,
        )

        riscos = self._valor(
            decisao,
            "riscos",
            [],
        ) or []

        # ---------------------------------------------
        # Score
        # ---------------------------------------------

        if score >= 90:

            recomendacoes.append(
                "Inventário altamente recomendado para este planejamento."
            )

        elif score >= 75:

            recomendacoes.append(
                "Inventário recomendado para compor o plano."
            )

        else:

            recomendacoes.append(
                "Utilização recomendada apenas em situações específicas."
            )

        # ---------------------------------------------
        # Papel
        # ---------------------------------------------

        papel = str(papel).upper()

        if papel == "PRINCIPAL":

            recomendacoes.append(
                "Priorizar investimento neste inventário."
            )

        elif papel == "COMPLEMENTAR":

            recomendacoes.append(
                "Utilizar para ampliar cobertura e frequência."
            )

        elif papel == "APOIO":

            recomendacoes.append(
                "Utilizar como reforço tático."
            )

        elif papel == "TATICO":

            recomendacoes.append(
                "Aplicação recomendada em ações específicas."
            )

        # ---------------------------------------------
        # Confiança
        # ---------------------------------------------

        if confianca >= 90:

            recomendacoes.append(
                "Elevado grau de confiança na recomendação."
            )

        elif confianca < 60:

            recomendacoes.append(
                "Recomendação sujeita a maior incerteza."
            )

        # ---------------------------------------------
        # Riscos

        # ---------------------------------------------

        if riscos:

            recomendacoes.extend(riscos)

        return recomendacoes

    # =====================================================
    # RESUMO EXECUTIVO
    # =====================================================

    def resumo(self, resultado):

        decisoes = resultado.decisoes

        if not decisoes:

            return [
                "Nenhum inventário recomendado."
            ]

        media = round(
            sum(
                d.score
                for d in decisoes
            )
            / len(decisoes),
            2,
        )

        principais = len([
            d
            for d in decisoes
            if d.papel.upper() == "PRINCIPAL"
        ])

        complementares = len([
            d
            for d in decisoes
            if d.papel.upper() == "COMPLEMENTAR"
        ])

        texto = [

            f"Score médio do plano: {media}.",

            f"{principais} inventários classificados como PRINCIPAIS.",

            f"{complementares} inventários classificados como COMPLEMENTARES."

        ]

        if media >= 90:

            texto.append(
                "Plano altamente consistente."
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

    # =====================================================
    # RISCOS
    # =====================================================

    def riscos(self, resultado):

        decisoes = resultado.decisoes

        riscos = []

        if not decisoes:

            riscos.append(
                "Nenhum inventário selecionado."
            )

            return riscos

        principais = len([
            d
            for d in decisoes
            if d.papel.upper() == "PRINCIPAL"
        ])

        if principais == 1:

            riscos.append(
                "Dependência excessiva de um único canal principal."
            )

        if len(decisoes) < 3:

            riscos.append(
                "Baixa diversidade de inventários."
            )

        media = (
            sum(
                d.score
                for d in decisoes
            )
            / len(decisoes)
        )

        if media < 70:

            riscos.append(
                "Baixa aderência estratégica do plano."
            )

        alta_concentracao = any(
            d.percentual >= 50
            for d in decisoes
        )

        if alta_concentracao:

            riscos.append(
                "Alta concentração de investimento em um único inventário."
            )

        return riscos