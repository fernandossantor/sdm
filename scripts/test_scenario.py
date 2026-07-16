from engine.mcp_engine import *

from engine.scenarios import distribuir_verba



briefing = obter_briefing(

    "Lançamento SDM"

)


objetivo = obter_objetivo_por_id(

    briefing["objetivo_id"]

)



audiencias = obter_audiencias_briefing(

    briefing["id"]

)



ambientes_obj = obter_ambientes_objetivo(

    objetivo["id"]

)



ranking = []



for aud in audiencias:


    peso_audiencia = float(

        aud["peso"]

    )


    consumo = obter_consumo(

        aud["audiencia_id"]

    )



    for c in consumo:


        ambiente_id = c["ambiente_id"]


        score_consumo = float(

            c["score"]

        )


        score_obj = 0


        for a in ambientes_obj:


            if (

                a["ambiente_id"]

                == ambiente_id

            ):


                score_obj = float(

                    a["score_base"]

                )


                break


        if score_obj == 0:

            continue


        score = calcular_score_ambiente(

            score_obj,

            score_consumo,

            peso_audiencia

        )


        ambiente = obter_nome_ambiente(

            ambiente_id

        )


        papel = classificar_papel(

            score

        )


        ranking.append(

            {

                "ambiente":

                    ambiente,


                "score":

                    score,


                "papel":

                    papel

            }

        )




cenario = distribuir_verba(

    briefing["orcamento"],

    ranking

)



print()

print("=" * 80)

print("MCP - CENÁRIO IDEAL")

print("=" * 80)

print()


for r in cenario:


    print(

        f"{r['ambiente']:20}",

        f"{r['score']:7.2f}",

        f"{r['participacao']:8.2f}%",

        f"R$ {r['verba']:12,.2f}",

        r["papel"]

    )