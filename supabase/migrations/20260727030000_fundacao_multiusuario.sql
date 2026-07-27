-- Fundação multiusuário: perfis, espaços, membros e isolamento da cadeia de projetos.

create table if not exists public.perfis_usuarios (
    id uuid primary key references auth.users(id) on delete cascade,
    nome varchar(180),
    papel_global varchar(20) not null default 'USUARIO'
        check (papel_global in ('ADMINISTRADOR', 'USUARIO')),
    ativo boolean not null default true,
    trocar_senha boolean not null default true,
    criado_em timestamptz not null default now(),
    atualizado_em timestamptz not null default now()
);

create table if not exists public.espacos_trabalho (
    id uuid primary key default gen_random_uuid(),
    nome varchar(180) not null,
    slug varchar(120) not null unique,
    proprietario_id uuid references public.perfis_usuarios(id) on delete restrict,
    legado boolean not null default false,
    ativo boolean not null default true,
    criado_em timestamptz not null default now(),
    atualizado_em timestamptz not null default now()
);

create unique index if not exists uq_espaco_legado
    on public.espacos_trabalho (legado) where legado;

create table if not exists public.membros_espacos (
    espaco_id uuid not null
        references public.espacos_trabalho(id) on delete cascade,
    usuario_id uuid not null
        references public.perfis_usuarios(id) on delete cascade,
    papel varchar(20) not null
        check (papel in ('PROPRIETARIO', 'EDITOR', 'LEITOR')),
    criado_em timestamptz not null default now(),
    atualizado_em timestamptz not null default now(),
    primary key (espaco_id, usuario_id)
);

create or replace function public.criar_perfil_usuario()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
    insert into public.perfis_usuarios (id, nome)
    values (
        new.id,
        coalesce(new.raw_user_meta_data ->> 'nome', new.email)
    )
    on conflict (id) do nothing;
    return new;
end;
$$;

drop trigger if exists trg_criar_perfil_usuario on auth.users;
create trigger trg_criar_perfil_usuario
after insert on auth.users
for each row execute function public.criar_perfil_usuario();

insert into public.perfis_usuarios (id, nome)
select
    id,
    coalesce(raw_user_meta_data ->> 'nome', email)
from auth.users
on conflict (id) do nothing;

insert into public.espacos_trabalho (nome, slug, legado)
values ('Espaço legado', 'espaco-legado', true)
on conflict (slug) do update set legado = true;

alter table public.projetos
    add column if not exists espaco_id uuid
        references public.espacos_trabalho(id) on delete restrict;
alter table public.briefings_v3
    add column if not exists espaco_id uuid
        references public.espacos_trabalho(id) on delete restrict;
alter table public.planejamentos
    add column if not exists espaco_id uuid
        references public.espacos_trabalho(id) on delete restrict;
alter table public.artefatos_workflow
    add column if not exists espaco_id uuid
        references public.espacos_trabalho(id) on delete restrict;

update public.projetos
set espaco_id = (select id from public.espacos_trabalho where legado)
where espaco_id is null;

update public.briefings_v3 b
set espaco_id = coalesce(
    (select p.espaco_id from public.projetos p where p.id = b.projeto_id),
    (select id from public.espacos_trabalho where legado)
)
where espaco_id is null;

update public.planejamentos p
set espaco_id = coalesce(
    (select b.espaco_id from public.briefings_v3 b where b.id = p.briefing_id),
    (select id from public.espacos_trabalho where legado)
)
where espaco_id is null;

update public.artefatos_workflow a
set espaco_id = coalesce(
    (select p.espaco_id from public.projetos p where p.id = a.projeto_id),
    (select pl.espaco_id from public.planejamentos pl where pl.id = a.planejamento_id),
    (select id from public.espacos_trabalho where legado)
)
where espaco_id is null;

alter table public.projetos alter column espaco_id set not null;
alter table public.briefings_v3 alter column espaco_id set not null;
alter table public.planejamentos alter column espaco_id set not null;
alter table public.artefatos_workflow alter column espaco_id set not null;

create index if not exists idx_projetos_espaco
    on public.projetos (espaco_id, atualizado_em desc);
create index if not exists idx_briefings_espaco
    on public.briefings_v3 (espaco_id, criado_em desc);
create index if not exists idx_planejamentos_espaco
    on public.planejamentos (espaco_id, atualizado_em desc);
create index if not exists idx_artefatos_espaco
    on public.artefatos_workflow (espaco_id, atualizado_em desc);
create index if not exists idx_membros_usuario
    on public.membros_espacos (usuario_id, espaco_id);

create or replace function public.eh_admin()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select exists (
        select 1 from public.perfis_usuarios
        where id = auth.uid()
          and papel_global = 'ADMINISTRADOR'
          and ativo
    );
$$;

create or replace function public.eh_membro_espaco(p_espaco_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select public.eh_admin() or exists (
        select 1 from public.membros_espacos m
        join public.perfis_usuarios p on p.id = m.usuario_id
        where m.espaco_id = p_espaco_id
          and m.usuario_id = auth.uid()
          and p.ativo
    );
$$;

create or replace function public.pode_editar_espaco(p_espaco_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select public.eh_admin() or exists (
        select 1 from public.membros_espacos m
        join public.perfis_usuarios p on p.id = m.usuario_id
        where m.espaco_id = p_espaco_id
          and m.usuario_id = auth.uid()
          and m.papel in ('PROPRIETARIO', 'EDITOR')
          and p.ativo
    );
$$;

create or replace function public.eh_proprietario_espaco(p_espaco_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select public.eh_admin() or exists (
        select 1 from public.espacos_trabalho e
        join public.perfis_usuarios p on p.id = e.proprietario_id
        where e.id = p_espaco_id
          and e.proprietario_id = auth.uid()
          and p.ativo
    );
$$;

create or replace function public.validar_espaco_relacional()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
    if tg_op = 'UPDATE' and old.espaco_id is distinct from new.espaco_id then
        raise exception 'O espaço de um registro não pode ser alterado';
    end if;
    if tg_table_name = 'briefings_v3' then
        if new.projeto_id is not null and not exists (
            select 1 from public.projetos
            where id = new.projeto_id and espaco_id = new.espaco_id
        ) then
            raise exception 'Projeto e briefing pertencem a espaços diferentes';
        end if;
    elsif tg_table_name = 'planejamentos' then
        if new.briefing_id is not null and not exists (
            select 1 from public.briefings_v3
            where id = new.briefing_id and espaco_id = new.espaco_id
        ) then
            raise exception 'Briefing e planejamento pertencem a espaços diferentes';
        end if;
    elsif tg_table_name = 'artefatos_workflow' then
        if new.projeto_id is not null and not exists (
            select 1 from public.projetos
            where id = new.projeto_id and espaco_id = new.espaco_id
        ) then
            raise exception 'Projeto e artefato pertencem a espaços diferentes';
        end if;
        if new.planejamento_id is not null and not exists (
            select 1 from public.planejamentos
            where id = new.planejamento_id and espaco_id = new.espaco_id
        ) then
            raise exception 'Planejamento e artefato pertencem a espaços diferentes';
        end if;
    end if;
    return new;
end;
$$;

drop trigger if exists trg_projeto_espaco on public.projetos;
create trigger trg_projeto_espaco
before update on public.projetos
for each row execute function public.validar_espaco_relacional();

drop trigger if exists trg_briefing_espaco on public.briefings_v3;
create trigger trg_briefing_espaco
before insert or update on public.briefings_v3
for each row execute function public.validar_espaco_relacional();

drop trigger if exists trg_planejamento_espaco on public.planejamentos;
create trigger trg_planejamento_espaco
before insert or update on public.planejamentos
for each row execute function public.validar_espaco_relacional();

drop trigger if exists trg_artefato_espaco on public.artefatos_workflow;
create trigger trg_artefato_espaco
before insert or update on public.artefatos_workflow
for each row execute function public.validar_espaco_relacional();

alter table public.perfis_usuarios enable row level security;
alter table public.espacos_trabalho enable row level security;
alter table public.membros_espacos enable row level security;
alter table public.projetos enable row level security;
alter table public.briefings_v3 enable row level security;
alter table public.planejamentos enable row level security;
alter table public.artefatos_workflow enable row level security;
alter table public.versoes_planejamento enable row level security;

drop policy if exists perfis_select on public.perfis_usuarios;
create policy perfis_select on public.perfis_usuarios
for select to authenticated
using (id = auth.uid() or public.eh_admin());

drop policy if exists perfis_update on public.perfis_usuarios;
create policy perfis_update on public.perfis_usuarios
for update to authenticated
using (id = auth.uid() or public.eh_admin())
with check (id = auth.uid() or public.eh_admin());

drop policy if exists espacos_select on public.espacos_trabalho;
create policy espacos_select on public.espacos_trabalho
for select to authenticated
using (public.eh_membro_espaco(id));

drop policy if exists espacos_update on public.espacos_trabalho;
create policy espacos_update on public.espacos_trabalho
for update to authenticated
using (public.eh_proprietario_espaco(id))
with check (public.eh_proprietario_espaco(id));

drop policy if exists membros_select on public.membros_espacos;
create policy membros_select on public.membros_espacos
for select to authenticated
using (public.eh_membro_espaco(espaco_id));

drop policy if exists membros_write on public.membros_espacos;
create policy membros_write on public.membros_espacos
for all to authenticated
using (
    public.eh_proprietario_espaco(espaco_id)
)
with check (
    public.eh_proprietario_espaco(espaco_id)
);

drop policy if exists projetos_membros on public.projetos;
create policy projetos_membros on public.projetos
for select to authenticated using (public.eh_membro_espaco(espaco_id));
drop policy if exists projetos_editores on public.projetos;
create policy projetos_editores on public.projetos
for all to authenticated
using (public.pode_editar_espaco(espaco_id))
with check (public.pode_editar_espaco(espaco_id));

drop policy if exists briefings_membros on public.briefings_v3;
create policy briefings_membros on public.briefings_v3
for select to authenticated using (public.eh_membro_espaco(espaco_id));
drop policy if exists briefings_editores on public.briefings_v3;
create policy briefings_editores on public.briefings_v3
for all to authenticated
using (public.pode_editar_espaco(espaco_id))
with check (public.pode_editar_espaco(espaco_id));

drop policy if exists planejamentos_membros on public.planejamentos;
create policy planejamentos_membros on public.planejamentos
for select to authenticated using (public.eh_membro_espaco(espaco_id));
drop policy if exists planejamentos_editores on public.planejamentos;
create policy planejamentos_editores on public.planejamentos
for all to authenticated
using (public.pode_editar_espaco(espaco_id))
with check (public.pode_editar_espaco(espaco_id));

drop policy if exists artefatos_membros on public.artefatos_workflow;
create policy artefatos_membros on public.artefatos_workflow
for select to authenticated using (public.eh_membro_espaco(espaco_id));
drop policy if exists artefatos_editores on public.artefatos_workflow;
create policy artefatos_editores on public.artefatos_workflow
for all to authenticated
using (public.pode_editar_espaco(espaco_id))
with check (public.pode_editar_espaco(espaco_id));

drop policy if exists versoes_membros on public.versoes_planejamento;
create policy versoes_membros on public.versoes_planejamento
for select to authenticated
using (
    exists (
        select 1 from public.planejamentos p
        where p.id = planejamento_id
          and public.eh_membro_espaco(p.espaco_id)
    )
);

grant usage on schema public to authenticated;
grant select on public.perfis_usuarios to authenticated;
grant update (nome, atualizado_em)
    on public.perfis_usuarios to authenticated;
grant select on public.espacos_trabalho to authenticated;
grant update (nome, atualizado_em)
    on public.espacos_trabalho to authenticated;
grant select, insert, update, delete on public.membros_espacos to authenticated;
grant select, insert, update, delete on public.projetos to authenticated;
grant select, insert, update, delete on public.briefings_v3 to authenticated;
grant select, insert, update, delete on public.planejamentos to authenticated;
grant select, insert, update, delete on public.artefatos_workflow to authenticated;
grant select on public.versoes_planejamento to authenticated;

create or replace function public.confirmar_troca_senha()
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
    if auth.uid() is null then
        raise exception 'Autenticação obrigatória';
    end if;
    update public.perfis_usuarios
    set trocar_senha = false, atualizado_em = now()
    where id = auth.uid() and ativo;
    if not found then
        raise exception 'Perfil ativo não encontrado';
    end if;
end;
$$;
revoke execute on function public.confirmar_troca_senha() from public, anon;
grant execute on function public.confirmar_troca_senha() to authenticated;

create or replace function public.proximo_codigo_copia_espaco(
    p_codigo_origem varchar,
    p_tabela text,
    p_id uuid,
    p_origem_id uuid,
    p_espaco_id uuid
)
returns varchar
language plpgsql
security definer
set search_path = public
as $$
declare
    v_origem_valida boolean := false;
begin
    if auth.uid() is null or not public.pode_editar_espaco(p_espaco_id) then
        raise exception 'Sem permissão para copiar neste espaço';
    end if;

    case p_tabela
        when 'projetos' then
            select exists (
                select 1 from public.projetos
                where id = p_origem_id
                  and espaco_id = p_espaco_id
                  and codigo = p_codigo_origem
            ) into v_origem_valida;
        when 'briefings_v3' then
            select exists (
                select 1 from public.briefings_v3
                where id = p_origem_id
                  and espaco_id = p_espaco_id
                  and codigo = p_codigo_origem
            ) into v_origem_valida;
        when 'planejamentos' then
            select exists (
                select 1 from public.planejamentos
                where id = p_origem_id
                  and espaco_id = p_espaco_id
                  and codigo = p_codigo_origem
            ) into v_origem_valida;
        else
            raise exception 'Tabela não autorizada para cópia contextual';
    end case;

    if not v_origem_valida then
        raise exception 'Registro de origem não pertence ao espaço informado';
    end if;

    return public.proximo_codigo_copia(
        p_codigo_origem,
        p_tabela,
        p_id
    );
end;
$$;
revoke execute on function public.proximo_codigo_copia_espaco(
    varchar, text, uuid, uuid, uuid
) from public, anon;
grant execute on function public.proximo_codigo_copia_espaco(
    varchar, text, uuid, uuid, uuid
) to authenticated;

-- A reserva de códigos é SECURITY DEFINER e ainda não valida o espaço de
-- origem. Até sua substituição por uma RPC contextual, apenas operações
-- administrativas explícitas podem executá-la.
revoke execute on function public.proximo_codigo_copia(varchar, text, uuid)
    from public, anon, authenticated;
grant execute on function public.proximo_codigo_copia(varchar, text, uuid)
    to service_role;

notify pgrst, 'reload schema';
