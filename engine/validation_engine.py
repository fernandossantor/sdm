from dataclasses import dataclass, field


# ==========================================================
# RESULTADO
# ==========================================================

@dataclass
class ValidationResult:

    valido: bool = True

    erros: list = field(default_factory=list)

    avisos: list = field(default_factory=list)

    informacoes: list = field(default_factory=list)


# ==========================================================
# ENGINE
# ==========================================================

class ValidationEngine:

    # =====================================================
    # VALIDAR
    # =====================================================

    def validar(

        self,

        briefing=None,

        decision=None,

        plano=None,

        forecast=None,

        dashboard=None

    ):

        resultado = ValidationResult()

        self._validar_decision(

            decision,

            resultado

        )

        self._validar_plano(

            plano,

            resultado

        )

        self._validar_forecast(

            forecast,

            resultado

        )

        self._validar_dashboard(

            dashboard,

            resultado

        )

        self._validar_briefing(

            briefing,

            decision,

            resultado

        )

        resultado.valido = (

            len(resultado.erros) == 0

        )

        return resultado

    # =====================================================
    # DECISION
    # =====================================================

    def _validar_decision(

        self,

        decision,

        resultado

    ):

        if decision is None:

            return

        decisoes = getattr(

            decision,

            "decisoes",

            []

        )

        if not decisoes:

            resultado.erros.append(

                "Nenhuma decisão foi gerada."

            )

            return

        for item in decisoes:

            score = getattr(

                item,

                "score",

                0

            )

            if score < 0:

                resultado.erros.append(

                    f"Score negativo em {item.inventario}."

                )

            elif score > 100:

                resultado.avisos.append(

                    f"Score acima de 100 em {item.inventario}."

                )

    # =====================================================
    # PLANO
    # =====================================================

    def _validar_plano(

        self,

        plano,

        resultado

    ):

        if plano is None:

            return

        itens = getattr(

            plano,

            "itens",

            []

        )

        verba_total = getattr(

            plano,

            "verba_total",

            0

        )

        soma_verba = round(

            sum(

                item.verba

                for item in itens

            ),

            2

        )

        if round(

            verba_total,

            2

        ) != soma_verba:

            resultado.erros.append(

                f"Verba total ({verba_total}) diferente da soma ({soma_verba})."

            )

        percentual = round(

            sum(

                item.percentual

                for item in itens

            ),

            2

        )

        if abs(

            percentual - 100

        ) > 0.1:

            resultado.erros.append(

                f"Percentuais totalizam {percentual}%."

            )

        for item in itens:

            if item.verba < 0:

                resultado.erros.append(

                    f"Verba negativa em {item.inventario}."

                )

    # =====================================================
    # FORECAST
    # =====================================================

    def _validar_forecast(

        self,

        forecast,

        resultado

    ):

        if forecast is None:

            return

        itens = getattr(

            forecast,

            "itens",

            []

        )

        if not itens:

            resultado.avisos.append(

                "Forecast vazio."

            )

    # =====================================================
    # DASHBOARD
    # =====================================================

    def _validar_dashboard(

        self,

        dashboard,

        resultado

    ):

        if dashboard is None:

            return

        if not getattr(

            dashboard,

            "visualizacoes",

            []

        ):

            resultado.avisos.append(

                "Dashboard sem visualizações."

            )

    # =====================================================
    # BRIEFING
    # =====================================================

    def _validar_briefing(

        self,

        briefing,

        decision,

        resultado

    ):

        if briefing is None:

            return

        if decision is None:

            return

        obrigatorios = getattr(

            briefing,

            "inventarios_obrigatorios",

            []

        )

        if not obrigatorios:

            return

        selecionados = []

        for item in getattr(

            decision,

            "decisoes",

            []

        ):

            identificador = getattr(

                item,

                "inventario",

                None

            )

            if isinstance(

                identificador,

                dict

            ):

                identificador = identificador.get(

                    "id"

                )

            selecionados.append(

                identificador

            )

        for inventario in obrigatorios:

            if inventario not in selecionados:

                resultado.erros.append(

                    f"Inventário obrigatório {inventario} não selecionado."

                )