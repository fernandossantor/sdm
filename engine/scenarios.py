def distribuir_verba(verba_total, ranking):

    total_score = sum(

        item["score"]

        for item in ranking

    )


    resultado = []


    for item in ranking:


        percentual = (

            item["score"]

            /

            total_score

        )


        verba = (

            percentual

            *

            verba_total

        )


        resultado.append(

            {

                "ambiente":

                    item["ambiente"],


                "score":

                    round(

                        item["score"],

                        2

                    ),


                "papel":

                    item["papel"],


                "participacao":

                    round(

                        percentual * 100,

                        2

                    ),


                "verba":

                    round(

                        verba,

                        2

                    )

            }

        )


    resultado.sort(

        key=lambda x: x["verba"],

        reverse=True

    )


    return resultado