drop function if exists public.versionar_briefing_mediad(
    uuid, uuid, uuid, jsonb, text, uuid, timestamptz
);
drop function if exists public.editar_briefing_mediad(
    uuid, uuid, jsonb, text, uuid, timestamptz
);
drop table if exists public.briefings_mediad_revisoes;
alter table public.briefings_mediad
    drop column if exists motivo_ultima_alteracao,
    drop column if exists atualizado_em,
    drop column if exists atualizado_por,
    drop column if exists conteudo,
    drop constraint if exists briefings_mediad_estado_check;
alter table public.briefings_mediad
    add constraint briefings_mediad_estado_check check (estado in ('RASCUNHO'));
