-- Corrige compatibilidade com o schema legado e integra o MCP de papéis
-- ao ranking utilizado pelo planejamento.

alter table public.universos
    add column if not exists publico_alvo bigint not null default 0;
alter table public.universos
    add column if not exists ativo boolean not null default true;

alter table public.segmentos
    add column if not exists sexo varchar(30);
alter table public.segmentos
    add column if not exists faixa_etaria varchar(80);
alter table public.segmentos
    add column if not exists classe_social varchar(80);
alter table public.segmentos
    add column if not exists escolaridade varchar(120);
alter table public.segmentos
    add column if not exists populacao bigint not null default 0;
alter table public.segmentos
    add column if not exists ativo boolean not null default true;

create table if not exists public.inventarios_papeis (
    id uuid primary key default gen_random_uuid(),
    inventario_id uuid not null references public.inventarios_v3(id) on delete cascade,
    afinidade numeric(6,2) not null default 100 check (afinidade between 0 and 200),
    cobertura numeric(5,2) not null default 70 check (cobertura between 0 and 100),
    consumo numeric(5,2) not null default 60 check (consumo between 0 and 100),
    adequacao_objetivo numeric(5,2) not null default 80 check (adequacao_objetivo between 0 and 100),
    score numeric(6,2) not null default 0,
    papel varchar(30) not null default 'APOIO',
    atualizado_em timestamptz not null default now(),
    unique (inventario_id)
);

alter table public.inventarios_papeis enable row level security;
revoke all on table public.inventarios_papeis from anon, authenticated;
grant all on table public.inventarios_papeis to service_role;

-- Solicita ao PostgREST a atualização imediata do cache após o deploy.
notify pgrst, 'reload schema';
