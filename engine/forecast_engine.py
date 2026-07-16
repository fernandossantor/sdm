from domain.models.forecast import (
    ForecastItem
)


class ForecastEngine:

    # =====================================================
    # FORECAST
    # =====================================================

    def calcular(

        self,

        plano,

        metricas

    ):

        idx = {

            m["inventario_id"]: m

            for m in metricas

        }

        resultado = []

        for item in plano.itens:

            m = None

            for metrica in metricas:

                if (

                    metrica.get("inventario")

                    == item.inventario

                ):

                    m = metrica

                    break

            if m is None:

                continue

            verba = item.verba

            cpm = float(

                m.get("cpm", 1)

            )

            ctr = float(

                m.get("ctr", 1)

            )

            taxa = float(

                m.get(

                    "taxa_conversao",

                    0.02

                )

            )

            impressoes = (

                verba

                / cpm

            ) * 1000

            cliques = (

                impressoes

                * ctr

                / 100

            )

            conversoes = (

                cliques

                * taxa

            )

            alcance = (

                impressoes

                /

                max(

                    1,

                    float(

                        m.get(

                            "frequencia_media",

                            2

                        )

                    )

                )

            )

            resultado.append(

                ForecastItem(

                    inventario=item.inventario,

                    verba=round(

                        verba,

                        2

                    ),

                    impressoes=round(

                        impressoes

                    ),

                    alcance=round(

                        alcance

                    ),

                    cliques=round(

                        cliques

                    ),

                    conversoes=round(

                        conversoes

                    ),

                    ctr=ctr,

                    cpm=cpm,

                    cpc=round(

                        verba

                        /

                        max(

                            cliques,

                            1

                        ),

                        2

                    ),

                    cpa=round(

                        verba

                        /

                        max(

                            conversoes,

                            1

                        ),

                        2

                    )

                )

            )

        return resultado