-- ==========================================================
-- SEGURANÇA E ROW LEVEL SECURITY
-- ==========================================================
--
-- O SDM 1.0 não possui autenticação de usuários. Por isso, o acesso direto
-- pela API pública fica bloqueado por padrão. O backend Streamlit e os
-- scripts administrativos usam exclusivamente a role service_role.

alter table if exists public.canais_v3 enable row level security;
alter table if exists public.ambientes_v3 enable row level security;
alter table if exists public.estruturas_v3 enable row level security;
alter table if exists public.formatos_v3 enable row level security;
alter table if exists public.tecnologias_v3 enable row level security;
alter table if exists public.perfis_editoriais enable row level security;
alter table if exists public.modalidades_compra_v3 enable row level security;
alter table if exists public.unidades_compra_v3 enable row level security;
alter table if exists public.plataformas_v3 enable row level security;
alter table if exists public.modelos_comerciais_v3 enable row level security;
alter table if exists public.briefings_v3 enable row level security;
alter table if exists public.audiencias_v3 enable row level security;
alter table if exists public.briefing_audiencias_v3 enable row level security;
alter table if exists public.objetivos_campanha_v3 enable row level security;
alter table if exists public.kpis_v3 enable row level security;
alter table if exists public.inventarios_v3 enable row level security;
alter table if exists public.inventarios_objetivos_v3 enable row level security;
alter table if exists public.inventarios_kpis_v3 enable row level security;
alter table if exists public.inventarios_metricas_v3 enable row level security;
alter table if exists public.consumo_midia_v3 enable row level security;
alter table if exists public.cenarios_v3 enable row level security;
alter table if exists public.segmentos enable row level security;
alter table if exists public.interesses enable row level security;
alter table if exists public.jornadas enable row level security;
alter table if exists public.biblioteca_publicos enable row level security;
alter table if exists public.biblioteca_publicos_segmentos enable row level security;
alter table if exists public.biblioteca_publicos_interesses enable row level security;
alter table if exists public.biblioteca_publicos_jornadas enable row level security;

revoke all on all tables in schema public from anon, authenticated;
grant all on all tables in schema public to service_role;
grant usage on schema public to service_role;

-- Novas tabelas também nascem sem acesso público. Quando o SDM ganhar
-- autenticação, permissões específicas deverão ser adicionadas por migration.
alter default privileges in schema public
    revoke all on tables from anon, authenticated;
alter default privileges in schema public
    grant all on tables to service_role;
