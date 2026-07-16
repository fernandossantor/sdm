from dataclasses import dataclass


@dataclass
class WorkflowState:

    briefing: bool = False

    planejamento: bool = False

    diagnostico: bool = False

    forecast: bool = False

    dashboard: bool = False

    exportacao: bool = False

    # =====================================================
    # TOTAL
    # =====================================================

    @property
    def total(self):

        return 6

    # =====================================================
    # CONCLUÍDAS
    # =====================================================

    @property
    def concluidas(self):

        return sum(

            [

                self.briefing,

                self.planejamento,

                self.diagnostico,

                self.forecast,

                self.dashboard,

                self.exportacao

            ]

        )

    # =====================================================
    # PROGRESSO
    # =====================================================

    @property
    def percentual(self):

        return round(

            self.concluidas

            /

            self.total

            *

            100,

            1

        )

    # =====================================================
    # PRÓXIMA ETAPA
    # =====================================================

    @property
    def proxima_etapa(self):

        if not self.briefing:

            return "Briefing"

        if not self.planejamento:

            return "Planejamento"

        if not self.diagnostico:

            return "Diagnóstico"

        if not self.forecast:

            return "Forecast"

        if not self.dashboard:

            return "Dashboard"

        if not self.exportacao:

            return "Exportação"

        return "Concluído"