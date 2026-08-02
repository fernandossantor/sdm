-- Persistencia aditiva da primeira fatia vertical da Traducao Estrategica.
-- As tabelas versionadas abaixo nao reutilizam as estruturas legadas.

create table public.traducao_v1_campanhas (
    id text primary key,
    espaco_id uuid not null references public.espacos_trabalho(id) on delete restrict,
    nome text not null check (btrim(nome) <> ''),
    marca text not null check (btrim(marca) <> ''),
    produto_servico text,
    versao_schema text not null,
    criado_por uuid not null references public.perfis_usuarios(id) on delete restrict,
    criado_em timestamptz not null default now(),
    unique (id, espaco_id)
);

create table public.traducao_v1_briefing_snapshots (
    id text primary key,
    campanha_id text not null,
    espaco_id uuid not null,
    versao_schema text not null,
    conteudo jsonb not null check (jsonb_typeof(conteudo) = 'object'),
    criado_por uuid not null references public.perfis_usuarios(id) on delete restrict,
    criado_em timestamptz not null default now(),
    unique (id, espaco_id),
    unique (campanha_id, versao_schema),
    foreign key (campanha_id, espaco_id)
        references public.traducao_v1_campanhas(id, espaco_id) on delete restrict
);

create table public.traducao_v1_comandos (
    id text primary key,
    campanha_id text not null,
    briefing_snapshot_id text not null,
    espaco_id uuid not null,
    modo text not null check (modo = 'TRADUZIR_BRIEFING'),
    versao_schema text not null,
    conteudo jsonb not null check (jsonb_typeof(conteudo) = 'object'),
    solicitado_por uuid not null references public.perfis_usuarios(id) on delete restrict,
    solicitado_em timestamptz not null,
    unique (id, espaco_id),
    foreign key (campanha_id, espaco_id)
        references public.traducao_v1_campanhas(id, espaco_id) on delete restrict,
    foreign key (briefing_snapshot_id, espaco_id)
        references public.traducao_v1_briefing_snapshots(id, espaco_id) on delete restrict
);

create table public.traducao_v1_execucoes (
    id text primary key,
    comando_id text not null,
    espaco_id uuid not null,
    estado text not null check (estado in ('CONCLUIDA', 'CONCLUIDA_COM_RESSALVAS')),
    confianca numeric(5, 2) not null check (confianca between 0 and 100),
    alertas jsonb not null default '[]'::jsonb check (jsonb_typeof(alertas) = 'array'),
    iniciado_em timestamptz not null,
    concluido_em timestamptz not null check (concluido_em >= iniciado_em),
    unique (id, espaco_id),
    unique (comando_id),
    foreign key (comando_id, espaco_id)
        references public.traducao_v1_comandos(id, espaco_id) on delete restrict
);

create table public.traducao_v1_contratos_estrategicos (
    id text primary key,
    execucao_id text not null,
    campanha_id text not null,
    briefing_snapshot_id text not null,
    espaco_id uuid not null,
    versao_schema text not null,
    estado text not null,
    conteudo jsonb not null check (jsonb_typeof(conteudo) = 'object'),
    criado_em timestamptz not null default now(),
    unique (id, espaco_id),
    unique (execucao_id),
    foreign key (execucao_id, espaco_id)
        references public.traducao_v1_execucoes(id, espaco_id) on delete restrict,
    foreign key (campanha_id, espaco_id)
        references public.traducao_v1_campanhas(id, espaco_id) on delete restrict,
    foreign key (briefing_snapshot_id, espaco_id)
        references public.traducao_v1_briefing_snapshots(id, espaco_id) on delete restrict
);

create table public.traducao_v1_rastreabilidade (
    id text primary key,
    execucao_id text not null,
    espaco_id uuid not null,
    ordem integer not null check (ordem >= 0),
    tipo text not null check (btrim(tipo) <> ''),
    referencia text not null check (btrim(referencia) <> ''),
    versao text,
    detalhes jsonb not null default '{}'::jsonb check (jsonb_typeof(detalhes) = 'object'),
    unique (execucao_id, ordem),
    foreign key (execucao_id, espaco_id)
        references public.traducao_v1_execucoes(id, espaco_id) on delete restrict
);

create index traducao_v1_campanhas_espaco_idx
    on public.traducao_v1_campanhas (espaco_id, criado_em desc);
create index traducao_v1_briefings_campanha_idx
    on public.traducao_v1_briefing_snapshots (campanha_id, criado_em desc);
create index traducao_v1_comandos_campanha_idx
    on public.traducao_v1_comandos (campanha_id, solicitado_em desc);
create index traducao_v1_execucoes_espaco_idx
    on public.traducao_v1_execucoes (espaco_id, concluido_em desc);
create index traducao_v1_contratos_campanha_idx
    on public.traducao_v1_contratos_estrategicos (campanha_id, criado_em desc);

alter table public.traducao_v1_campanhas enable row level security;
alter table public.traducao_v1_briefing_snapshots enable row level security;
alter table public.traducao_v1_comandos enable row level security;
alter table public.traducao_v1_execucoes enable row level security;
alter table public.traducao_v1_contratos_estrategicos enable row level security;
alter table public.traducao_v1_rastreabilidade enable row level security;

create policy traducao_v1_campanhas_leitura
    on public.traducao_v1_campanhas for select to authenticated
    using (public.eh_membro_espaco(espaco_id));
create policy traducao_v1_briefings_leitura
    on public.traducao_v1_briefing_snapshots for select to authenticated
    using (public.eh_membro_espaco(espaco_id));
create policy traducao_v1_comandos_leitura
    on public.traducao_v1_comandos for select to authenticated
    using (public.eh_membro_espaco(espaco_id));
create policy traducao_v1_execucoes_leitura
    on public.traducao_v1_execucoes for select to authenticated
    using (public.eh_membro_espaco(espaco_id));
create policy traducao_v1_contratos_leitura
    on public.traducao_v1_contratos_estrategicos for select to authenticated
    using (public.eh_membro_espaco(espaco_id));
create policy traducao_v1_rastreabilidade_leitura
    on public.traducao_v1_rastreabilidade for select to authenticated
    using (public.eh_membro_espaco(espaco_id));

create or replace function public.persistir_traducao_estrategica_v1(
    p_espaco_id uuid,
    p_usuario_id uuid,
    p_registro jsonb
)
returns text
language plpgsql
security definer
set search_path = public, pg_temp
as $$
declare
    v_rastro jsonb;
begin
    if p_registro is null or jsonb_typeof(p_registro) <> 'object' then
        raise exception 'registro de persistencia invalido';
    end if;

    if auth.uid() is distinct from p_usuario_id then
        raise exception 'usuario autenticado divergente';
    end if;

    if not public.pode_editar_espaco(p_espaco_id) then
        raise exception 'usuario sem permissao de edicao no espaco';
    end if;

    insert into public.traducao_v1_campanhas (
        id, espaco_id, nome, marca, produto_servico, versao_schema, criado_por
    ) values (
        p_registro #>> '{campanha,id}',
        p_espaco_id,
        p_registro #>> '{campanha,nome}',
        p_registro #>> '{campanha,marca}',
        p_registro #>> '{campanha,produto_servico}',
        p_registro #>> '{campanha,versao_schema}',
        p_usuario_id
    );

    insert into public.traducao_v1_briefing_snapshots (
        id, campanha_id, espaco_id, versao_schema, conteudo, criado_por
    ) values (
        p_registro #>> '{briefing_snapshot,id}',
        p_registro #>> '{briefing_snapshot,campanha_id}',
        p_espaco_id,
        p_registro #>> '{briefing_snapshot,versao_schema}',
        p_registro #> '{briefing_snapshot,conteudo}',
        p_usuario_id
    );

    insert into public.traducao_v1_comandos (
        id, campanha_id, briefing_snapshot_id, espaco_id, modo,
        versao_schema, conteudo, solicitado_por, solicitado_em
    ) values (
        p_registro #>> '{comando,id}',
        p_registro #>> '{comando,campanha_id}',
        p_registro #>> '{comando,briefing_snapshot_id}',
        p_espaco_id,
        p_registro #>> '{comando,modo}',
        p_registro #>> '{comando,versao_schema}',
        p_registro #> '{comando,conteudo}',
        p_usuario_id,
        (p_registro #>> '{comando,solicitado_em}')::timestamptz
    );

    insert into public.traducao_v1_execucoes (
        id, comando_id, espaco_id, estado, confianca, alertas,
        iniciado_em, concluido_em
    ) values (
        p_registro #>> '{execucao,id}',
        p_registro #>> '{execucao,comando_id}',
        p_espaco_id,
        p_registro #>> '{execucao,estado}',
        (p_registro #>> '{execucao,confianca}')::numeric,
        p_registro #> '{execucao,alertas}',
        (p_registro #>> '{execucao,iniciado_em}')::timestamptz,
        (p_registro #>> '{execucao,concluido_em}')::timestamptz
    );

    insert into public.traducao_v1_contratos_estrategicos (
        id, execucao_id, campanha_id, briefing_snapshot_id, espaco_id,
        versao_schema, estado, conteudo
    ) values (
        p_registro #>> '{contrato,id}',
        p_registro #>> '{contrato,execucao_id}',
        p_registro #>> '{contrato,campanha_id}',
        p_registro #>> '{contrato,briefing_snapshot_id}',
        p_espaco_id,
        p_registro #>> '{contrato,versao_schema}',
        p_registro #>> '{contrato,estado}',
        p_registro #> '{contrato,conteudo}'
    );

    for v_rastro in
        select value from jsonb_array_elements(p_registro -> 'rastreabilidade')
    loop
        insert into public.traducao_v1_rastreabilidade (
            id, execucao_id, espaco_id, ordem, tipo, referencia, versao, detalhes
        ) values (
            v_rastro ->> 'id',
            p_registro #>> '{execucao,id}',
            p_espaco_id,
            (v_rastro ->> 'ordem')::integer,
            v_rastro ->> 'tipo',
            v_rastro ->> 'referencia',
            v_rastro ->> 'versao',
            coalesce(v_rastro -> 'detalhes', '{}'::jsonb)
        );
    end loop;

    return p_registro #>> '{contrato,id}';
end;
$$;

revoke all on function public.persistir_traducao_estrategica_v1(uuid, uuid, jsonb)
    from public, anon;
grant execute on function public.persistir_traducao_estrategica_v1(uuid, uuid, jsonb)
    to authenticated, service_role;

grant select on public.traducao_v1_campanhas to authenticated, service_role;
grant select on public.traducao_v1_briefing_snapshots to authenticated, service_role;
grant select on public.traducao_v1_comandos to authenticated, service_role;
grant select on public.traducao_v1_execucoes to authenticated, service_role;
grant select on public.traducao_v1_contratos_estrategicos to authenticated, service_role;
grant select on public.traducao_v1_rastreabilidade to authenticated, service_role;
