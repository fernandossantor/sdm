from domain.models.forecast import (
    Forecast
)

from engine.forecast_engine import (
    ForecastEngine
)
from application.services.context_service import ContextService


class ForecastService:

    def __init__(self):

        self.engine = ForecastEngine()
        self.context_service = ContextService()

    def gerar_itens(self, plano, metricas=None):

        if metricas is None:
            metricas = self.context_service.metricas()

        return self.engine.calcular(plano, metricas)

    # =====================================================
    # FORECAST
    # =====================================================

    def gerar(

        self,

        plano,

        metricas

    ):

        itens = self.gerar_itens(plano, metricas)

        forecast = Forecast()

        for item in itens:

            forecast.adicionar(

                item

            )

        return forecast

    # =====================================================
    # RESUMO
    # =====================================================

    def resumo(

        self,

        forecast

    ):

        return {

            "verba": forecast.verba_total,

            "impressoes": forecast.impressoes,

            "alcance": forecast.alcance,

            "cliques": forecast.cliques,

            "conversoes": forecast.conversoes,

            "ctr": forecast.ctr_medio,

            "cpm": forecast.cpm_medio,

            "cpc": forecast.cpc_medio,

            "cpa": forecast.cpa_medio

        }

    # =====================================================
    # DATAFRAME
    # =====================================================

    def dataframe(

        self,

        forecast

    ):

        import pandas as pd

        return pd.DataFrame(

            [

                {

                    "Inventário": i.inventario,

                    "Verba": i.verba,

                    "Impressões": i.impressoes,

                    "Alcance": i.alcance,

                    "Cliques": i.cliques,

                    "Conversões": i.conversoes,

                    "CTR": i.ctr,

                    "CPM": i.cpm,

                    "CPC": i.cpc,

                    "CPA": i.cpa

                }

                for i in forecast.itens

            ]

        )
