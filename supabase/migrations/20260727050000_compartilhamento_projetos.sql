-- Compartilhamento de projetos sem duplicação, com autorização contextual.

alter table public.projetos
    add column if not exists proprietario_id uuid
        references public.perfis_usuarios(id) on delete restrict;

update public.projetos p
set proprietario_id = coalesce(
    (select e.proprietario_id
       from public.espacos_trabalho e
      where e.id = p.espaco_id),
    (select u.id
       from public.perfis_usuarios u
      where u.papel_global = 'ADMINISTRADOR' and u.ativo
      order by u.criado_em
      limit 1)
)
where p.proprietario_id is null;

do $$
begin
    if exists (select 1 from public.projetos where proprietario_id is null) then
        raise exception 'Projetos sem proprietário após o preenchimento';
    end if;
end;
$$;

alter table public.projetos alter column proprietario_id set not null;
create index if not exists idx_projetos_proprietario
    on public.projetos (proprietario_id, atualizado_em desc);

create table if not exists public.projetos_membros (
    projeto_id uuid not null
        references public.projetos(id) on delete cascade,
    usuario_id uuid not null
        references public.perfis_usuarios(id) on delete cascade,
    papel varchar(20) not null
        check (papel in ('PROPRIETARIO', 'EDITOR', 'LEITOR')),
    concedido_por uuid references public.perfis_usuarios(id) on delete set null,
    criado_em timestamptz not null default now(),
    atualizado_em timestamptz not null default now(),
    primary key (projeto_id, usuario_id)
);

create index if not exists idx_projetos_membros_usuario
    on public.projetos_membros (usuario_id, projeto_id);

insert into public.projetos_membros (
    projeto_id, usuario_id, papel, concedido_por
)
select id, proprietario_id, 'PROPRIETARIO', proprietario_id
from public.projetos
on conflict (projeto_id, usuario_id) do update
set papel = 'PROPRIETARIO', atualizado_em = now();

create or replace function public.eh_membro_projeto(p_projeto_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select public.eh_admin() or exists (
        select 1
        from public.projetos p
        join public.perfis_usuarios u on u.id = auth.uid() and u.ativo
        left join public.projetos_membros m
          on m.projeto_id = p.id and m.usuario_id = auth.uid()
        where p.id = p_projeto_id
          and (p.proprietario_id = auth.uid() or m.usuario_id is not null)
    );
$$;

create or replace function public.pode_editar_projeto(p_projeto_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select public.eh_admin() or exists (
        select 1
        from public.projetos p
        join public.perfis_usuarios u on u.id = auth.uid() and u.ativo
        left join public.projetos_membros m
          on m.projeto_id = p.id and m.usuario_id = auth.uid()
        where p.id = p_projeto_id
          and (
              p.proprietario_id = auth.uid()
              or m.papel in ('PROPRIETARIO', 'EDITOR')
          )
    );
$$;

create or replace function public.pode_gerenciar_projeto(p_projeto_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select public.eh_admin() or exists (
        select 1
        from public.projetos p
        join public.perfis_usuarios u
          on u.id = p.proprietario_id and u.ativo
        where p.id = p_projeto_id
          and p.proprietario_id = auth.uid()
    );
$$;

create or replace function public.eh_convidado_espaco(p_espaco_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select exists (
        select 1
        from public.projetos p
        join public.projetos_membros m on m.projeto_id = p.id
        join public.perfis_usuarios u on u.id = m.usuario_id and u.ativo
        where p.espaco_id = p_espaco_id
          and m.usuario_id = auth.uid()
    );
$$;

drop policy if exists espacos_select on public.espacos_trabalho;
create policy espacos_select on public.espacos_trabalho
for select to authenticated
using (
    public.eh_membro_espaco(id)
    or public.eh_convidado_espaco(id)
);

create or replace function public.validar_proprietario_projeto()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
    if new.proprietario_id is null then
        new.proprietario_id := coalesce(
            auth.uid(),
            (select proprietario_id
               from public.espacos_trabalho
              where id = new.espaco_id)
        );
    end if;
    if not exists (
        select 1 from public.perfis_usuarios
        where id = new.proprietario_id and ativo
    ) then
        raise exception 'O proprietário do projeto deve ser um usuário ativo';
    end if;
    if tg_op = 'UPDATE'
       and old.proprietario_id is distinct from new.proprietario_id
       and not public.pode_gerenciar_projeto(old.id) then
        raise exception 'Somente o proprietário ou administrador transfere o projeto';
    end if;
    return new;
end;
$$;

drop trigger if exists trg_validar_proprietario_projeto on public.projetos;
create trigger trg_validar_proprietario_projeto
before insert or update of proprietario_id on public.projetos
for each row execute function public.validar_proprietario_projeto();

alter table public.projetos_membros enable row level security;

drop policy if exists projetos_membros_select on public.projetos_membros;
create policy projetos_membros_select on public.projetos_membros
for select to authenticated
using (public.eh_membro_projeto(projeto_id));

drop policy if exists projetos_membros_write on public.projetos_membros;
create policy projetos_membros_write on public.projetos_membros
for all to authenticated
using (public.pode_gerenciar_projeto(projeto_id))
with check (public.pode_gerenciar_projeto(projeto_id));

drop policy if exists projetos_membros on public.projetos;
create policy projetos_membros on public.projetos
for select to authenticated
using (
    public.eh_membro_espaco(espaco_id)
    or public.eh_membro_projeto(id)
);

drop policy if exists projetos_editores on public.projetos;
create policy projetos_editores on public.projetos
for all to authenticated
using (
    public.pode_editar_espaco(espaco_id)
    or public.pode_editar_projeto(id)
)
with check (
    public.pode_editar_espaco(espaco_id)
    or public.pode_editar_projeto(id)
);

drop policy if exists briefings_membros on public.briefings_v3;
create policy briefings_membros on public.briefings_v3
for select to authenticated
using (
    public.eh_membro_espaco(espaco_id)
    or (projeto_id is not null and public.eh_membro_projeto(projeto_id))
);

drop policy if exists briefings_editores on public.briefings_v3;
create policy briefings_editores on public.briefings_v3
for all to authenticated
using (
    public.pode_editar_espaco(espaco_id)
    or (projeto_id is not null and public.pode_editar_projeto(projeto_id))
)
with check (
    public.pode_editar_espaco(espaco_id)
    or (projeto_id is not null and public.pode_editar_projeto(projeto_id))
);

create or replace function public.eh_membro_planejamento(p_planejamento_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select exists (
        select 1 from public.planejamentos pl
        join public.briefings_v3 b on b.id = pl.briefing_id
        where pl.id = p_planejamento_id
          and b.projeto_id is not null
          and public.eh_membro_projeto(b.projeto_id)
    );
$$;

create or replace function public.pode_editar_planejamento(p_planejamento_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select exists (
        select 1 from public.planejamentos pl
        join public.briefings_v3 b on b.id = pl.briefing_id
        where pl.id = p_planejamento_id
          and b.projeto_id is not null
          and public.pode_editar_projeto(b.projeto_id)
    );
$$;

drop policy if exists planejamentos_membros on public.planejamentos;
create policy planejamentos_membros on public.planejamentos
for select to authenticated
using (
    public.eh_membro_espaco(espaco_id)
    or public.eh_membro_planejamento(id)
);

drop policy if exists planejamentos_editores on public.planejamentos;
create policy planejamentos_editores on public.planejamentos
for all to authenticated
using (
    public.pode_editar_espaco(espaco_id)
    or public.pode_editar_planejamento(id)
)
with check (
    public.pode_editar_espaco(espaco_id)
    or public.pode_editar_planejamento(id)
);

drop policy if exists artefatos_membros on public.artefatos_workflow;
create policy artefatos_membros on public.artefatos_workflow
for select to authenticated
using (
    public.eh_membro_espaco(espaco_id)
    or (projeto_id is not null and public.eh_membro_projeto(projeto_id))
    or (
        planejamento_id is not null
        and public.eh_membro_planejamento(planejamento_id)
    )
);

drop policy if exists artefatos_editores on public.artefatos_workflow;
create policy artefatos_editores on public.artefatos_workflow
for all to authenticated
using (
    public.pode_editar_espaco(espaco_id)
    or (projeto_id is not null and public.pode_editar_projeto(projeto_id))
    or (
        planejamento_id is not null
        and public.pode_editar_planejamento(planejamento_id)
    )
)
with check (
    public.pode_editar_espaco(espaco_id)
    or (projeto_id is not null and public.pode_editar_projeto(projeto_id))
    or (
        planejamento_id is not null
        and public.pode_editar_planejamento(planejamento_id)
    )
);

create or replace function public.compartilhar_projeto(
    p_projeto_id uuid,
    p_email text,
    p_papel text
)
returns uuid
language plpgsql
security definer
set search_path = public, auth
as $$
declare
    v_usuario_id uuid;
    v_proprietario_anterior uuid;
begin
    if not public.pode_gerenciar_projeto(p_projeto_id) then
        raise exception 'Sem permissão para compartilhar o projeto';
    end if;
    if p_papel not in ('PROPRIETARIO', 'EDITOR', 'LEITOR') then
        raise exception 'Papel de projeto inválido';
    end if;
    select u.id into v_usuario_id
    from auth.users u
    join public.perfis_usuarios p on p.id = u.id and p.ativo
    where lower(u.email) = lower(trim(p_email));
    if v_usuario_id is null then
        raise exception 'Usuário ativo não encontrado';
    end if;

    select proprietario_id into v_proprietario_anterior
    from public.projetos where id = p_projeto_id for update;

    if p_papel = 'PROPRIETARIO' then
        update public.projetos
        set proprietario_id = v_usuario_id, atualizado_em = now()
        where id = p_projeto_id;
        insert into public.projetos_membros (
            projeto_id, usuario_id, papel, concedido_por
        ) values (
            p_projeto_id, v_proprietario_anterior, 'EDITOR', auth.uid()
        )
        on conflict (projeto_id, usuario_id) do update
        set papel = 'EDITOR', concedido_por = auth.uid(), atualizado_em = now();
    end if;

    insert into public.projetos_membros (
        projeto_id, usuario_id, papel, concedido_por
    ) values (
        p_projeto_id, v_usuario_id, p_papel, auth.uid()
    )
    on conflict (projeto_id, usuario_id) do update
    set papel = excluded.papel,
        concedido_por = auth.uid(),
        atualizado_em = now();

    insert into public.logs_auditoria (
        ator_id, acao, alvo_tipo, alvo_id, detalhes
    ) values (
        auth.uid(),
        case when p_papel = 'PROPRIETARIO'
             then 'PROJETO_TRANSFERIDO' else 'PROJETO_COMPARTILHADO' end,
        'PROJETO',
        p_projeto_id,
        jsonb_build_object('usuario_id', v_usuario_id, 'papel', p_papel)
    );
    return v_usuario_id;
end;
$$;

create or replace function public.revogar_compartilhamento_projeto(
    p_projeto_id uuid,
    p_usuario_id uuid
)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
    if not public.pode_gerenciar_projeto(p_projeto_id) then
        raise exception 'Sem permissão para revogar o compartilhamento';
    end if;
    if exists (
        select 1 from public.projetos
        where id = p_projeto_id and proprietario_id = p_usuario_id
    ) then
        raise exception 'O proprietário atual não pode ser removido';
    end if;
    delete from public.projetos_membros
    where projeto_id = p_projeto_id and usuario_id = p_usuario_id;
    if not found then
        raise exception 'Compartilhamento não encontrado';
    end if;
    insert into public.logs_auditoria (
        ator_id, acao, alvo_tipo, alvo_id, detalhes
    ) values (
        auth.uid(), 'PROJETO_COMPARTILHAMENTO_REVOGADO', 'PROJETO',
        p_projeto_id, jsonb_build_object('usuario_id', p_usuario_id)
    );
end;
$$;

create or replace function public.listar_compartilhamentos_projeto(
    p_projeto_id uuid
)
returns table (
    usuario_id uuid,
    nome text,
    email text,
    papel text
)
language plpgsql
stable
security definer
set search_path = public, auth
as $$
begin
    if not public.pode_gerenciar_projeto(p_projeto_id) then
        raise exception 'Sem permissão para listar compartilhamentos';
    end if;
    return query
    select m.usuario_id, p.nome::text, u.email::text, m.papel::text
    from public.projetos_membros m
    join public.perfis_usuarios p on p.id = m.usuario_id
    join auth.users u on u.id = m.usuario_id
    where m.projeto_id = p_projeto_id
    order by
        case m.papel when 'PROPRIETARIO' then 1 when 'EDITOR' then 2 else 3 end,
        p.nome;
end;
$$;

revoke all on table public.projetos_membros from anon;
grant select, insert, update, delete on public.projetos_membros to authenticated;
revoke execute on function public.compartilhar_projeto(uuid, text, text)
    from public, anon;
grant execute on function public.compartilhar_projeto(uuid, text, text)
    to authenticated;
revoke execute on function public.revogar_compartilhamento_projeto(uuid, uuid)
    from public, anon;
grant execute on function public.revogar_compartilhamento_projeto(uuid, uuid)
    to authenticated;
revoke execute on function public.listar_compartilhamentos_projeto(uuid)
    from public, anon;
grant execute on function public.listar_compartilhamentos_projeto(uuid)
    to authenticated;

notify pgrst, 'reload schema';
