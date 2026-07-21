"""Auditoria somente leitura das permissões públicas e administrativas."""

import os

from dotenv import load_dotenv
from supabase import create_client

from infrastructure.database.database_schema import (
    AMBIENTES,
    AUDIENCIAS,
    BRIEFINGS,
    BRIEFING_AUDIENCIAS,
    BIBLIOTECA_PUBLICOS,
    BIBLIOTECA_PUBLICOS_INTERESSES,
    BIBLIOTECA_PUBLICOS_JORNADAS,
    BIBLIOTECA_PUBLICOS_SEGMENTOS,
    CANAIS,
    CENARIOS,
    CONSUMO,
    ESTRUTURAS,
    FORMATOS,
    INTERESSES,
    INVENTARIOS,
    INVENTARIOS_KPIS,
    INVENTARIOS_METRICAS,
    INVENTARIOS_OBJETIVOS,
    JORNADAS,
    KPIS,
    MODALIDADES,
    MODELOS_COMERCIAIS,
    OBJETIVOS,
    PERFIS,
    PLATAFORMAS,
    SEGMENTOS,
    TECNOLOGIAS,
    UNIDADES,
    UNIVERSOS,
)


TABELAS = (
    CANAIS,
    AMBIENTES,
    ESTRUTURAS,
    FORMATOS,
    TECNOLOGIAS,
    PERFIS,
    MODALIDADES,
    UNIDADES,
    PLATAFORMAS,
    MODELOS_COMERCIAIS,
    BRIEFINGS,
    AUDIENCIAS,
    BRIEFING_AUDIENCIAS,
    OBJETIVOS,
    KPIS,
    INVENTARIOS,
    INVENTARIOS_OBJETIVOS,
    INVENTARIOS_KPIS,
    INVENTARIOS_METRICAS,
    CONSUMO,
    CENARIOS,
    SEGMENTOS,
    INTERESSES,
    JORNADAS,
    BIBLIOTECA_PUBLICOS,
    BIBLIOTECA_PUBLICOS_SEGMENTOS,
    BIBLIOTECA_PUBLICOS_INTERESSES,
    BIBLIOTECA_PUBLICOS_JORNADAS,
    UNIVERSOS,
)


def pode_ler(cliente, tabela):

    try:
        cliente.table(tabela).select("*").limit(1).execute()
        return True, ""
    except Exception as erro:
        return False, type(erro).__name__


def executar():

    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    chave_publica = os.getenv("SUPABASE_KEY")
    chave_servico = os.getenv("SUPABASE_SERVICE_KEY")

    if not all((url, chave_publica, chave_servico)):
        raise RuntimeError("Variáveis do Supabase não configuradas.")

    publico = create_client(url, chave_publica)
    servico = create_client(url, chave_servico)
    falhas = []

    for tabela in TABELAS:
        leitura_publica, _ = pode_ler(publico, tabela)
        leitura_servico, erro_servico = pode_ler(servico, tabela)

        estado_publico = "ACESSO INDEVIDO" if leitura_publica else "bloqueado"
        estado_servico = "ok" if leitura_servico else f"FALHA ({erro_servico})"
        print(f"{tabela}: público={estado_publico}; serviço={estado_servico}")

        if leitura_publica or not leitura_servico:
            falhas.append(tabela)

    if falhas:
        raise RuntimeError(
            "Permissões inconsistentes nas tabelas: " + ", ".join(falhas)
        )


if __name__ == "__main__":
    executar()
