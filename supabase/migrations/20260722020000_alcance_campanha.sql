-- Inclui a meta de alcance da campanha no briefing persistido.

alter table public.briefings_v3
    add column if not exists alcance_objetivo varchar(20) not null default 'MEDIO';
alter table public.briefings_v3
    add column if not exists alcance_percentual smallint not null default 60;

do $$
begin
    if not exists (
        select 1
        from pg_constraint
        where conname = 'briefings_v3_alcance_objetivo_check'
          and conrelid = 'public.briefings_v3'::regclass
    ) then
        alter table public.briefings_v3
            add constraint briefings_v3_alcance_objetivo_check
            check (alcance_objetivo in ('BAIXO', 'MEDIO', 'ALTO'));
    end if;

    if not exists (
        select 1
        from pg_constraint
        where conname = 'briefings_v3_alcance_percentual_check'
          and conrelid = 'public.briefings_v3'::regclass
    ) then
        alter table public.briefings_v3
            add constraint briefings_v3_alcance_percentual_check
            check (
                (alcance_objetivo = 'BAIXO' and alcance_percentual between 0 and 50)
                or (alcance_objetivo = 'MEDIO' and alcance_percentual between 51 and 69)
                or (alcance_objetivo = 'ALTO' and alcance_percentual between 70 and 100)
            );
    end if;
end $$;

notify pgrst, 'reload schema';
