-- Inventários globais administrados e inventários privados por espaço.

alter table public.inventarios_v3
    add column if not exists escopo varchar(20) not null default 'GLOBAL'
        check (escopo in ('GLOBAL', 'PRIVADO')),
    add column if not exists espaco_id uuid
        references public.espacos_trabalho(id) on delete restrict,
    add column if not exists criado_por uuid
        references public.perfis_usuarios(id) on delete set null,
    add column if not exists atualizado_por uuid
        references public.perfis_usuarios(id) on delete set null,
    add column if not exists arquivado_em timestamptz,
    add column if not exists arquivado_por uuid
        references public.perfis_usuarios(id) on delete set null;

alter table public.inventarios_v3
    drop constraint if exists inventarios_v3_escopo_espaco_check;
alter table public.inventarios_v3
    add constraint inventarios_v3_escopo_espaco_check check (
        (escopo = 'GLOBAL' and espaco_id is null)
        or (escopo = 'PRIVADO' and espaco_id is not null)
    );

create index if not exists idx_inventarios_escopo_espaco
    on public.inventarios_v3 (escopo, espaco_id, ativo, nome);

create or replace function public.pode_ler_inventario(p_inventario_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select exists (
        select 1 from public.inventarios_v3 i
        where i.id = p_inventario_id
          and (
              i.escopo = 'GLOBAL'
              or (
                  i.escopo = 'PRIVADO'
                  and public.eh_membro_espaco(i.espaco_id)
              )
          )
    );
$$;

create or replace function public.pode_editar_inventario(p_inventario_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select exists (
        select 1 from public.inventarios_v3 i
        where i.id = p_inventario_id
          and (
              (i.escopo = 'GLOBAL' and public.eh_admin())
              or (
                  i.escopo = 'PRIVADO'
                  and public.pode_editar_espaco(i.espaco_id)
              )
          )
    );
$$;

create or replace function public.validar_escopo_inventario()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
    if new.escopo = 'GLOBAL' then
        new.espaco_id := null;
    elsif new.espaco_id is null then
        raise exception 'Inventário privado exige espaço de trabalho';
    end if;
    if tg_op = 'UPDATE'
       and (
           old.escopo is distinct from new.escopo
           or old.espaco_id is distinct from new.espaco_id
       )
       and not public.eh_admin() then
        raise exception 'Somente administrador altera o escopo do inventário';
    end if;
    if tg_op = 'INSERT' then
        new.criado_por := coalesce(new.criado_por, auth.uid());
    end if;
    new.atualizado_por := coalesce(auth.uid(), new.atualizado_por);
    if new.ativo = false and old.ativo is distinct from false then
        new.arquivado_em := coalesce(new.arquivado_em, now());
        new.arquivado_por := coalesce(new.arquivado_por, auth.uid());
    elsif new.ativo = true then
        new.arquivado_em := null;
        new.arquivado_por := null;
    end if;
    return new;
end;
$$;

drop trigger if exists trg_validar_escopo_inventario
    on public.inventarios_v3;
create trigger trg_validar_escopo_inventario
before insert or update on public.inventarios_v3
for each row execute function public.validar_escopo_inventario();

alter table public.inventarios_v3 enable row level security;
drop policy if exists inventarios_select on public.inventarios_v3;
create policy inventarios_select on public.inventarios_v3
for select to authenticated
using (
    escopo = 'GLOBAL'
    or (escopo = 'PRIVADO' and public.eh_membro_espaco(espaco_id))
);
drop policy if exists inventarios_write on public.inventarios_v3;
create policy inventarios_write on public.inventarios_v3
for all to authenticated
using (
    (escopo = 'GLOBAL' and public.eh_admin())
    or (escopo = 'PRIVADO' and public.pode_editar_espaco(espaco_id))
)
with check (
    (escopo = 'GLOBAL' and public.eh_admin())
    or (escopo = 'PRIVADO' and public.pode_editar_espaco(espaco_id))
);

do $$
declare
    v_tabela text;
begin
    foreach v_tabela in array array[
        'inventarios_objetivos_v3',
        'inventarios_kpis_v3',
        'inventarios_metricas_v3',
        'inventarios_papeis',
        'medicoes_inventario',
        'precos_inventario'
    ] loop
        execute format('alter table public.%I enable row level security', v_tabela);
        execute format('drop policy if exists inventario_pai_select on public.%I', v_tabela);
        execute format(
            'create policy inventario_pai_select on public.%I '
            'for select to authenticated '
            'using (public.pode_ler_inventario(inventario_id))',
            v_tabela
        );
        execute format('drop policy if exists inventario_pai_write on public.%I', v_tabela);
        execute format(
            'create policy inventario_pai_write on public.%I '
            'for all to authenticated '
            'using (public.pode_editar_inventario(inventario_id)) '
            'with check (public.pode_editar_inventario(inventario_id))',
            v_tabela
        );
        execute format(
            'grant select, insert, update, delete on public.%I to authenticated',
            v_tabela
        );
    end loop;
end;
$$;

grant select, insert, update, delete on public.inventarios_v3 to authenticated;

create or replace function public.proximo_codigo_copia_inventario(
    p_codigo_origem varchar,
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
    v_codigo varchar;
    v_escopo varchar;
    v_espaco uuid;
begin
    select escopo, espaco_id into v_escopo, v_espaco
    from public.inventarios_v3 where id = p_origem_id;
    if v_escopo is null or not public.pode_ler_inventario(p_origem_id) then
        raise exception 'Inventário de origem não autorizado';
    end if;
    if v_escopo = 'GLOBAL' then
        if not public.eh_admin() then
            raise exception 'Somente administrador duplica inventário global';
        end if;
    elsif v_espaco is distinct from p_espaco_id
       or not public.pode_editar_espaco(v_espaco) then
        raise exception 'Espaço privado não autorizado';
    end if;
    select public.proximo_codigo_copia(
        p_codigo_origem, 'inventarios_v3', p_id
    ) into v_codigo;
    return v_codigo;
end;
$$;

revoke execute on function public.proximo_codigo_copia_inventario(
    varchar, uuid, uuid, uuid
) from public, anon;
grant execute on function public.proximo_codigo_copia_inventario(
    varchar, uuid, uuid, uuid
) to authenticated;

notify pgrst, 'reload schema';
