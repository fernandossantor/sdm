from engine.models import DecisionContext

from engine.briefing_engine import (

    obter_briefing,

    obter_objetivo,

    obter_audiencias

)


class DecisionEngine:


    def construir(

        self,

        nome_briefing

    ):

        briefing = obter_briefing(

            nome_briefing

        )

        objetivo = obter_objetivo(

            briefing.objetivo_id

        )

        audiencias = obter_audiencias(

            briefing.id

        )

        return DecisionContext(

            briefing=briefing,

            objetivo=objetivo,

            audiencias=audiencias,

            kpi=briefing.kpi

        )