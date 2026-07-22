-- Suporta seleção de inventários por campanha e persistência dos artefatos
-- gerados nas etapas posteriores do workflow.

alter table public.inventarios_papeis
    add column if not exists selecionado boolean not null default true;

create table if not exists public.artefatos_workflow (
    id uuid primary key default gen_random_uuid(),
    tipo varchar(40) not null,
    nome varchar(180) not null,
    planejamento_id uuid references public.planejamentos(id) on delete cascade,
    dados jsonb not null default '{}'::jsonb,
    criado_em timestamptz not null default now(),
    atualizado_em timestamptz not null default now()
);

create index if not exists idx_artefatos_workflow_tipo
    on public.artefatos_workflow(tipo, atualizado_em desc);

alter table public.artefatos_workflow enable row level security;
revoke all on table public.artefatos_workflow from anon, authenticated;
grant all on table public.artefatos_workflow to service_role;

notify pgrst, 'reload schema';
