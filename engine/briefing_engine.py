from infrastructure.database.admin_client import admin

from engine.models import (

    Briefing,

    Objetivo,

    AudienciaBriefing

)


# =====================================================
# BRIEFING
# =====================================================

def obter_briefing(nome: str) -> Briefing:

    r = (

        admin

        .table("briefings_v3")

        .select("*")

        .eq("nome", nome)

        .execute()

    )


    if not r.data:

        raise Exception(

            f"Briefing '{nome}' não encontrado."

        )


    b = r.data[0]


    return Briefing(

        id=b["id"],

        nome=b["nome"],

        anunciante=b["anunciante"],

        objetivo_id=b["objetivo_id"],

        orcamento=float(b["orcamento"]),

        publico=b["publico"],

        faixa_etaria=b["faixa_etaria"],

        praca=b["praca"],

        periodo_inicio=b["periodo_inicio"],

        periodo_fim=b["periodo_fim"],

        kpi=b["kpi"],

        observacoes=b["observacoes"]

    )


# =====================================================
# OBJETIVO
# =====================================================

def obter_objetivo(objetivo_id: str) -> Objetivo:

    r = (

        admin

        .table("objetivos_campanha_v3")

        .select("*")

        .eq("id", objetivo_id)

        .execute()

    )


    if not r.data:

        raise Exception(

            "Objetivo não encontrado."

        )


    o = r.data[0]


    return Objetivo(

        id=o["id"],

        nome=o["nome"],

        descricao=o["descricao"]

    )


# =====================================================
# AUDIÊNCIAS
# =====================================================

def obter_audiencias(briefing_id: str):

    r = (

        admin

        .table("briefing_audiencias_v3")

        .select("*")

        .eq("briefing_id", briefing_id)

        .execute()

    )


    audiencias = []


    for a in r.data:

        audiencias.append(

            AudienciaBriefing(

                audiencia_id=a["audiencia_id"],

                peso=float(a["peso"])

            )

        )


    return audiencias