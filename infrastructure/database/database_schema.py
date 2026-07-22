"""
SDM
Esquema lógico do banco de dados.

Toda referência a tabelas deve utilizar este módulo.

Nunca utilizar nomes literais ("inventarios_v3", etc.)
diretamente nos repositories.
"""


# ==========================================================
# CATÁLOGOS
# ==========================================================

CANAIS = "canais_v3"

AMBIENTES = "ambientes_v3"

ESTRUTURAS = "estruturas_v3"

FORMATOS = "formatos_v3"

FORMATOS_AMBIENTES = "formatos_ambientes"

TECNOLOGIAS = "tecnologias_v3"

# Não existe perfis_v3
PERFIS = "perfis_editoriais"

MODALIDADES = "modalidades_compra_v3"

UNIDADES = "unidades_compra_v3"

MODALIDADES_UNIDADES = "modalidades_unidades_compra"

PLATAFORMAS = "plataformas_v3"

MODELOS_COMERCIAIS = "modelos_comerciais_v3"


# ==========================================================
# PLANEJAMENTO
# ==========================================================

BRIEFINGS = "briefings_v3"

AUDIENCIAS = "audiencias_v3"

BRIEFING_AUDIENCIAS = "briefing_audiencias_v3"

OBJETIVOS = "objetivos_campanha_v3"

KPIS = "kpis_v3"


# ==========================================================
# INVENTÁRIOS
# ==========================================================

INVENTARIOS = "inventarios_v3"

INVENTARIOS_OBJETIVOS = "inventarios_objetivos_v3"

INVENTARIOS_KPIS = "inventarios_kpis_v3"

INVENTARIOS_METRICAS = "inventarios_metricas_v3"


# ==========================================================
# CONSUMO
# ==========================================================

CONSUMO = "consumo_midia_v3"

CENARIOS = "cenarios_v3"

UNIVERSOS = "universos"


# ==========================================================
# BIBLIOTECA DE PÚBLICOS
# ==========================================================

SEGMENTOS = "segmentos"

INTERESSES = "interesses"

JORNADAS = "jornadas"

BIBLIOTECA_PUBLICOS = "biblioteca_publicos"

BIBLIOTECA_PUBLICOS_SEGMENTOS = "biblioteca_publicos_segmentos"

BIBLIOTECA_PUBLICOS_INTERESSES = "biblioteca_publicos_interesses"

BIBLIOTECA_PUBLICOS_JORNADAS = "biblioteca_publicos_jornadas"

INTERESSES_AMBIENTES_AFINIDADE = "interesses_ambientes_afinidade"

PRECOS_INVENTARIO = "precos_inventario"

INVENTARIOS_PAPEIS = "inventarios_papeis"

PLANEJAMENTOS = "planejamentos"

ARTEFATOS_WORKFLOW = "artefatos_workflow"

PROJETOS = "projetos"
