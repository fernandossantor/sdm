from engine.models import PlanoMidia

from engine.briefing_engine import (

    obter_briefing,

    obter_objetivo,

    obter_audiencias

)

from engine.score_engine import (

    calcular_scores

)

from engine.allocation_engine import (

    AllocationEngine

)


class PlannerEngine:


    def gerar_plano(


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


        ranking = calcular_scores(

            objetivo,

            audiencias

        )


        allocation = AllocationEngine()


        distribuicao = allocation.distribuir(

            ranking,

            briefing.orcamento

        )


        plano = PlanoMidia(

            briefing=briefing,

            objetivo=objetivo,

            audiencias=audiencias,

            ambientes=distribuicao

        )


        plano.indicadores = {

            "verba_total":

                briefing.orcamento,

            "principal":

                len(

                    [

                        a

                        for a in distribuicao

                        if a.papel == "PRINCIPAL"

                    ]

                ),

            "complementar":

                len(

                    [

                        a

                        for a in distribuicao

                        if a.papel == "COMPLEMENTAR"

                    ]

                ),

            "apoio":

                len(

                    [

                        a

                        for a in distribuicao

                        if a.papel == "APOIO"

                    ]

                )

        }


        plano.justificativas = [

            "Distribuição baseada na aderência ao objetivo da campanha.",

            "Considerado o perfil de consumo da audiência.",

            "Os percentuais representam um cenário estratégico inicial."

        ]


        return plano