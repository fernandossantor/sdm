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

            m = idx.get(getattr(item, "inventario_id", ""))

            for metrica in metricas if m is None else []:

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

                m.get("cpm") or 1

            )

            ctr = float(

                m.get("ctr") or 0

            )

            taxa = float(

                m.get(

                    "taxa_conversao",

                    0.02

                ) or 0.02

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

            frequencia_plano = float(
                getattr(plano, "frequencia_alvo", 0) or 0
            )

            frequencia = frequencia_plano or float(
                m.get("frequencia_media") or 2
            )

            alcance = (

                impressoes

                /

                max(

                    1,

                    frequencia

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
