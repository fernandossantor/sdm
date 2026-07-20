from datetime import datetime


class ReportEngine:

    # =====================================================
    # RELATÓRIO
    # =====================================================

    def gerar(

        self,

        dashboard

    ):

        return {

            "titulo": "Relatório de Plano de Mídia",

            "data": datetime.now(),

            "resumo": self._resumo(

                dashboard

            ),

            "indicadores": self._indicadores(

                dashboard

            ),

            "plano": self._plano(

                dashboard

            ),

            "forecast": self._forecast(

                dashboard

            ),

            "cenarios": self._cenarios(

                dashboard

            ),

            "insights": self._insights(

                dashboard

            ),

            "recomendacoes": self._recomendacoes(

                dashboard

            ),

            "riscos": self._riscos(

                dashboard

            ),

            "alertas": self._alertas(

                dashboard

            ),

            "conclusao": self._conclusao(

                dashboard

            )

        }

    # =====================================================
    # RESUMO
    # =====================================================

    def _resumo(

        self,

        dashboard

    ):

        return dashboard.resumo

    # =====================================================
    # INDICADORES
    # =====================================================

    def _indicadores(

        self,

        dashboard

    ):

        return dashboard.indicadores

    # =====================================================
    # PLANO
    # =====================================================

    def _plano(

        self,

        dashboard

    ):

        return dashboard.plano

    # =====================================================
    # FORECAST
    # =====================================================

    def _forecast(

        self,

        dashboard

    ):

        return dashboard.forecast

    # =====================================================
    # CENÁRIOS
    # =====================================================

    def _cenarios(

        self,

        dashboard

    ):

        return dashboard.cenarios

    # =====================================================
    # INSIGHTS
    # =====================================================

    def _insights(

        self,

        dashboard

    ):

        return dashboard.insights

    # =====================================================
    # RECOMENDAÇÕES
    # =====================================================

    def _recomendacoes(

        self,

        dashboard

    ):

        return dashboard.recomendacoes

    # =====================================================
    # RISCOS
    # =====================================================

    def _riscos(

        self,

        dashboard

    ):

        return dashboard.riscos

    # =====================================================
    # ALERTAS
    # =====================================================

    def _alertas(

        self,

        dashboard

    ):

        return dashboard.alertas

    # =====================================================
    # CONCLUSÃO
    # =====================================================

    def _conclusao(

        self,

        dashboard

    ):

        score = dashboard.resumo.score_global

        if score >= 85:

            avaliacao = "Plano altamente recomendado."

        elif score >= 70:

            avaliacao = "Plano recomendado."

        elif score >= 50:

            avaliacao = "Plano aceitável com ajustes."

        else:

            avaliacao = "Plano necessita revisão."

        return {

            "score_global": score,

            "avaliacao": avaliacao,

            "gerado_em": datetime.now()

        }