drop function if exists public.transicionar_briefing_mediad(
    uuid, uuid, text, text, jsonb, uuid, timestamptz
);
alter table public.briefings_mediad
    drop column if exists alertas_reconhecidos;
