create table if not exists public.projetos (
    id uuid primary key default gen_random_uuid(),
    nome varchar(180) not null,
    briefing_id uuid references public.briefings_v3(id) on delete set null,
    etapa_atual varchar(40) not null default 'briefing',
    progresso jsonb not null default '{}'::jsonb,
    ativo boolean not null default true,
    criado_em timestamptz not null default now(),
    atualizado_em timestamptz not null default now()
);

alter table public.briefings_v3
    add column if not exists projeto_id uuid references public.projetos(id) on delete set null,
    add column if not exists marca varchar(180),
    add column if not exists produto varchar(180),
    add column if not exists tipo_flight varchar(20) not null default 'LINEAR',
    add column if not exists frequencia_objetivo varchar(20) not null default 'MEDIA',
    add column if not exists frequencia_alvo integer not null default 5,
    add column if not exists publicos jsonb not null default '[]'::jsonb,
    add column if not exists kpis jsonb not null default '[]'::jsonb;

alter table public.artefatos_workflow
    add column if not exists projeto_id uuid references public.projetos(id) on delete cascade;

create index if not exists idx_projetos_atualizado on public.projetos(atualizado_em desc);
create index if not exists idx_briefings_projeto on public.briefings_v3(projeto_id);
create index if not exists idx_artefatos_projeto on public.artefatos_workflow(projeto_id, tipo);

alter table public.projetos enable row level security;
revoke all on table public.projetos from anon, authenticated;
grant all on table public.projetos to service_role;

delete from public.briefing_audiencias_v3
where briefing_id in (select id from public.briefings_v3 where nome = 'Lançamento SDM');
update public.planejamentos set briefing_id = null
where briefing_id in (select id from public.briefings_v3 where nome = 'Lançamento SDM');
delete from public.briefings_v3 where nome = 'Lançamento SDM';

notify pgrst, 'reload schema';
