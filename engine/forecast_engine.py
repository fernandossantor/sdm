from domain.models.forecast import ForecastItem


class ForecastEngine:

    """
    Projeta os principais indicadores da campanha
    a partir do plano de mídia.
    """

    # =====================================================
    # FORECAST
    # =====================================================

    def calcular(
        self,
        plano,
        metricas,
    ):

        metricas_indexadas = {
            m.get("inventario"): m
            for m in metricas
        }

        metricas = metricas or []

        resultado = []

        for item in plano.itens:

            m = metricas_indexadas.get(
                item.inventario
            )

            if not m:
                continue

            forecast = self._calcular_item(
                item,
                m,
            )

            resultado.append(forecast)

        return resultado

    # =====================================================
    # ITEM
    # =====================================================

    def _calcular_item(
        self,
        item,
        metrica,
    ):

        verba = float(item.verba)

        cpm = max(
            float(
                metrica.get(
                    "cpm",
                    1,
                )
            ),
            0.01,
        )

        ctr = max(
            float(
                metrica.get(
                    "ctr",
                    0,
                )
            ),
            0,
        )

        taxa = max(
            float(
                metrica.get(
                    "taxa_conversao",
                    0.02,
                )
            ),
            0,
        )

        frequencia = max(
            float(
                metrica.get(
                    "frequencia_media",
                    2,
                )
            ),
            1,
        )

        impressoes = (
            verba / cpm
        ) * 1000

        alcance = (
            impressoes / frequencia
        )

        cliques = (
            impressoes
            * ctr
            / 100
        )

        conversoes = (
            cliques
            * taxa
        )

        cpc = (
            verba / cliques
            if cliques > 0
            else 0
        )

        cpa = (
            verba / conversoes
            if conversoes > 0
            else 0
        )

        return ForecastItem(

            inventario=item.inventario,

            verba=round(verba, 2),

            impressoes=round(impressoes),

            alcance=round(alcance),

            cliques=round(cliques),

            conversoes=round(conversoes),

            ctr=round(ctr, 2),

            cpm=round(cpm, 2),

            cpc=round(cpc, 2),

            cpa=round(cpa, 2),

        )