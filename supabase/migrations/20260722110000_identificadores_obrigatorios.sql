-- Após o backfill da migration anterior, códigos passam a ser obrigatórios.
alter table public.projetos alter column codigo set not null;
alter table public.briefings_v3 alter column codigo set not null;
alter table public.planejamentos alter column codigo set not null;
alter table public.inventarios_v3 alter column codigo set not null;
alter table public.universos alter column codigo set not null;
alter table public.segmentos alter column codigo set not null;
alter table public.biblioteca_publicos alter column codigo set not null;
notify pgrst, 'reload schema';
