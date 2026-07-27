-- Auditoria própria das ações administrativas do MediAd Planner.

create table if not exists public.logs_auditoria (
    id bigint generated always as identity primary key,
    ator_id uuid references public.perfis_usuarios(id) on delete set null,
    acao varchar(80) not null,
    alvo_tipo varchar(80) not null,
    alvo_id uuid,
    detalhes jsonb not null default '{}'::jsonb,
    criado_em timestamptz not null default now()
);

create index if not exists idx_logs_auditoria_criado
    on public.logs_auditoria (criado_em desc);
create index if not exists idx_logs_auditoria_ator
    on public.logs_auditoria (ator_id, criado_em desc);
create index if not exists idx_logs_auditoria_alvo
    on public.logs_auditoria (alvo_tipo, alvo_id, criado_em desc);

alter table public.logs_auditoria enable row level security;

drop policy if exists logs_auditoria_admin_select
    on public.logs_auditoria;
create policy logs_auditoria_admin_select
on public.logs_auditoria
for select to authenticated
using (public.eh_admin());

revoke all on public.logs_auditoria from anon, authenticated;
grant select on public.logs_auditoria to authenticated;
grant all on public.logs_auditoria to service_role;
grant usage, select on sequence public.logs_auditoria_id_seq to service_role;

notify pgrst, 'reload schema';
