from infrastructure.database.admin_client import admin


# ---------------------------------------------------
# BRIEFING
# ---------------------------------------------------

def obter_briefing(nome):

    r = (

        admin

        .table("briefings_v3")

        .select("*")

        .eq("nome", nome)

        .execute()

    )

    return r.data[0]


# ---------------------------------------------------
# OBJETIVO
# ---------------------------------------------------

def obter_objetivo_por_id(objetivo_id):

    r = (

        admin

        .table("objetivos_campanha_v3")

        .select("*")

        .eq("id", objetivo_id)

        .execute()

    )

    return r.data[0]


# ---------------------------------------------------
# AUDIÊNCIAS DO BRIEFING
# ---------------------------------------------------

def obter_audiencias_briefing(briefing_id):

    r = (

        admin

        .table("briefing_audiencias_v3")

        .select("*")

        .eq("briefing_id", briefing_id)

        .execute()

    )

    return r.data


# ---------------------------------------------------
# CONSUMO DE MÍDIA
# ---------------------------------------------------

def obter_consumo(audiencia_id):

    r = (

        admin

        .table("consumo_midia_v3")

        .select("*")

        .eq("audiencia_id", audiencia_id)

        .execute()

    )

    return r.data


# ---------------------------------------------------
# OBJETIVO X AMBIENTE
# ---------------------------------------------------

def obter_ambientes_objetivo(objetivo_id):

    r = (

        admin

        .table("objetivos_ambientes_v3")

        .select("*")

        .eq("objetivo_id", objetivo_id)

        .execute()

    )

    return r.data


# ---------------------------------------------------
# AMBIENTE
# ---------------------------------------------------

def obter_nome_ambiente(id_ambiente):

    r = (

        admin

        .table("ambientes_v3")

        .select("nome")

        .eq("id", id_ambiente)

        .execute()

    )

    return r.data[0]["nome"]


# ---------------------------------------------------
# SCORE
# ---------------------------------------------------

def calcular_score_ambiente(

    score_objetivo,

    score_consumo,

    peso_audiencia,

    peso_cenario=1

):

    return (

        score_objetivo

        *

        score_consumo

        *

        peso_audiencia

        *

        peso_cenario

    )


# ---------------------------------------------------
# PAPEL ESTRATÉGICO
# ---------------------------------------------------

def classificar_papel(score):

    if score >= 20:

        return "PRINCIPAL"


    elif score >= 12:

        return "COMPLEMENTAR"


    elif score >= 4:

        return "APOIO"


    return "RESIDUAL"