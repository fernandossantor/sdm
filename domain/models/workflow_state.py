from dataclasses import dataclass


@dataclass
class WorkflowState:

    briefing: bool = False

    mcp_papeis: bool = False

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

        return 7

    # =====================================================
    # CONCLUÍDAS
    # =====================================================

    @property
    def concluidas(self):

        return sum(

            [

                self.briefing,

                self.mcp_papeis,

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

            return "Briefing de Mídia"

        if not self.mcp_papeis:

            return "Papéis dos Meios"

        if not self.planejamento:

            return "Plano de Mídia"

        if not self.diagnostico:

            return "Diagnóstico do Plano"

        if not self.forecast:

            return "Projeção de Resultados"

        if not self.dashboard:

            return "Painel de Resultados"

        if not self.exportacao:

            return "Relatório de Mídia"

        return "Concluído"
