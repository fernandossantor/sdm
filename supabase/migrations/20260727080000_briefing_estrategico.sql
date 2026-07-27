-- Contexto estratégico do briefing, aditivo e compatível com legados.

alter table public.briefings_v3
    add column if not exists contexto_mercado text,
    add column if not exists concorrentes jsonb not null default '[]'::jsonb,
    add column if not exists situacao_marca text,
    add column if not exists situacao_categoria text,
    add column if not exists objetivo_negocio text,
    add column if not exists objetivo_comunicacao text,
    add column if not exists objetivo_midia text,
    add column if not exists jornada_compra text,
    add column if not exists ciclo_compra text,
    add column if not exists sazonalidade text,
    add column if not exists capacidade_distribuicao text,
    add column if not exists criterios_criativos text,
    add column if not exists riscos_regulatorios text;

alter table public.briefings_v3
    drop constraint if exists briefings_v3_concorrentes_array_check;
alter table public.briefings_v3
    add constraint briefings_v3_concorrentes_array_check
    check (jsonb_typeof(concorrentes) = 'array');

notify pgrst, 'reload schema';
