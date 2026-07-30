-- Rollback da persistência inicial de Campanha e Briefing.
-- Executar apenas com confirmação explícita e após backup.

drop function if exists public.iniciar_briefing_mediad(
    uuid, uuid, uuid, uuid, timestamptz
);
drop function if exists public.abrir_campanha_mediad(jsonb, uuid);
drop table if exists public.briefings_mediad;
drop table if exists public.campanhas_mediad_equipe;
drop table if exists public.campanhas_mediad;
