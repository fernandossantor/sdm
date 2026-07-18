from domain.models.dashboard import (
    DashboardResult,
    DashboardSummary,
    DashboardIndicator,
    DashboardVisualization
)


class DashboardEngine:

    # =====================================================
    # DASHBOARD
    # =====================================================

    def gerar(

        self,

        decision=None,

        plano=None,

        forecast=None,

        insights=None,

        recommendations=None,

        scenarios=None

    ):

        dashboard = DashboardResult()

        dashboard.resumo = self._resumo(

            decision,

            plano

        )

        dashboard.indicadores = self._indicadores(

            decision,

            plano,

            forecast

        )

        dashboard.score = self._score(

            decision

        )

        dashboard.plano = self._plano(

            plano

        )

        dashboard.forecast = self._forecast(

            forecast

        )

        dashboard.cenarios = self._cenarios(

            scenarios

        )

        dashboard.insights = self._insights(

            insights

        )

        dashboard.recomendacoes = self._recommendations(

            recommendations

        )

        dashboard.alertas = self._alertas(

            decision

        )

        dashboard.riscos = self._riscos(

            recommendations

        )

        dashboard.visualizacoes = self._visualizacoes(

            decision,

            plano,

            forecast,

            scenarios

        )

        return dashboard

    # =====================================================
    # RESUMO
    # =====================================================

    def _resumo(

        self,

        decision,

        plano

    ):

        resumo = DashboardSummary()

        if decision:

            resumo.score_global = getattr(

                decision,

                "score_global",

                0

            )

            itens = getattr(

                decision,

                "decisoes",

                []

            )

            resumo.quantidade_inventarios = len(

                itens

            )

            for item in itens:

                papel = item.papel.upper()

                if papel == "PRINCIPAL":

                    resumo.principais += 1

                elif papel == "COMPLEMENTAR":

                    resumo.complementares += 1

                elif papel == "APOIO":

                    resumo.apoio += 1

                else:

                    resumo.opcionais += 1

        if plano:

            resumo.verba_total = getattr(

                plano,

                "verba_total",

                0

            )

        return resumo

    # =====================================================
    # INDICADORES
    # =====================================================

    def _indicadores(

        self,

        decision,

        plano,

        forecast

    ):

        indicadores = []

        if decision:

            indicadores.append(

                DashboardIndicator(

                    nome="Score Global",

                    valor=getattr(

                        decision,

                        "score_global",

                        0

                    ),

                    unidade="%"

                )

            )

        if plano:

            indicadores.append(

                DashboardIndicator(

                    nome="Verba",

                    valor=getattr(

                        plano,

                        "verba_total",

                        0

                    ),

                    unidade="R$"

                )

            )

        if forecast:

            indicadores.append(

                DashboardIndicator(

                    nome="Forecast",

                    valor=len(

                        getattr(

                            forecast,

                            "itens",

                            []

                        )

                    )

                )

            )

        return indicadores

    # =====================================================
    # SCORE
    # =====================================================

    def _score(

        self,

        decision

    ):

        if not decision:

            return {}

        return {

            "global": getattr(

                decision,

                "score_global",

                0

            ),

            "inventarios": getattr(

                decision,

                "decisoes",

                []

            )

        }

    # =====================================================
    # PLANO
    # =====================================================

    def _plano(

        self,

        plano

    ):

        if not plano:

            return {}

        return {

            "verba_total": plano.verba_total,

            "itens": plano.itens

        }

    # =====================================================
    # FORECAST
    # =====================================================

    def _forecast(

        self,

        forecast

    ):

        if not forecast:

            return {}

        return {

            "itens": getattr(

                forecast,

                "itens",

                []

            )

        }

    # =====================================================
    # CENÁRIOS
    # =====================================================

    def _cenarios(

        self,

        scenarios

    ):

        if not scenarios:

            return {}

        return scenarios

    # =====================================================
    # INSIGHTS
    # =====================================================

    def _insights(

        self,

        insights

    ):

        if not insights:

            return []

        return insights

    # =====================================================
    # RECOMENDAÇÕES
    # =====================================================

    def _recommendations(

        self,

        recommendations

    ):

        if not recommendations:

            return []

        return recommendations

    # =====================================================
    # ALERTAS
    # =====================================================

    def _alertas(

        self,

        decision

    ):

        if not decision:

            return []

        return getattr(

            decision,

            "alertas",

            []

        )

    # =====================================================
    # RISCOS
    # =====================================================

    def _riscos(

        self,

        recommendations

    ):

        if not recommendations:

            return []

        if hasattr(

            recommendations,

            "riscos"

        ):

            return recommendations.riscos

        return []

    # =====================================================
    # VISUALIZAÇÕES
    # =====================================================

    def _visualizacoes(

        self,

        decision,

        plano,

        forecast,

        scenarios

    ):

        visualizacoes = []

        if decision:

            visualizacoes.append(

                DashboardVisualization(

                    nome="Score por Inventário",

                    tipo="bar",

                    dados=getattr(

                        decision,

                        "decisoes",

                        []

                    )

                )

            )

        if plano:

            visualizacoes.append(

                DashboardVisualization(

                    nome="Distribuição de Verba",

                    tipo="pie",

                    dados=plano.itens

                )

            )

        if forecast:

            visualizacoes.append(

                DashboardVisualization(

                    nome="Forecast",

                    tipo="line",

                    dados=getattr(

                        forecast,

                        "itens",

                        []

                    )

                )

            )

        if scenarios:

            visualizacoes.append(

                DashboardVisualization(

                    nome="Comparação de Cenários",

                    tipo="radar",

                    dados=scenarios

                )

            )

        return visualizacoes