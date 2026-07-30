-- Persistência canônica inicial de Campanha e Briefing do MediAd Planner.

create table public.campanhas_mediad (
    id uuid primary key,
    espaco_id uuid not null
        references public.espacos_trabalho(id) on delete restrict,
    codigo varchar(32) not null unique
        check (codigo ~ '^MP-[0-9]{6}-[0-9]{4,}$'),
    nome varchar(240) not null check (btrim(nome) <> ''),
    anunciante_id uuid not null,
    marca_id uuid,
    produto_servico_id uuid,
    planejador_responsavel_id uuid not null
        references public.perfis_usuarios(id) on delete restrict,
    observacao_inicial text,
    campanha_derivada_de_id uuid,
    snapshot_nome_anunciante varchar(240) not null,
    snapshot_nome_marca varchar(240),
    snapshot_nome_produto_servico varchar(240),
    snapshot_identificacao_planejador varchar(240) not null,
    criado_por uuid not null
        references public.perfis_usuarios(id) on delete restrict,
    criado_em timestamptz not null,
    atualizado_em timestamptz not null,
    situacao varchar(24) not null default 'RASCUNHO'
        check (
            situacao in (
                'RASCUNHO', 'EM_ANDAMENTO', 'CONCLUIDA',
                'CANCELADA', 'ARQUIVADA'
            )
        ),
    etapa_atual varchar(48) not null default 'ABERTURA'
        check (
            etapa_atual in (
                'ABERTURA', 'BRIEFING', 'TRADUCAO_ESTRATEGICA',
                'ARQUITETURA_DE_MIDIA', 'SIMULACAO',
                'CONSOLIDACAO_DO_PLANO', 'VALIDACAO_E_APROVACAO',
                'ACOMPANHAMENTO_E_RESULTADOS'
            )
        ),
    unique (id, espaco_id),
    foreign key (campanha_derivada_de_id, espaco_id)
        references public.campanhas_mediad(id, espaco_id) on delete restrict,
    check ((marca_id is null) = (snapshot_nome_marca is null)),
    check (
        (produto_servico_id is null)
        = (snapshot_nome_produto_servico is null)
    )
);

create table public.campanhas_mediad_equipe (
    campanha_id uuid not null
        references public.campanhas_mediad(id) on delete cascade,
    usuario_id uuid not null
        references public.perfis_usuarios(id) on delete restrict,
    criado_em timestamptz not null default now(),
    primary key (campanha_id, usuario_id)
);

create table public.briefings_mediad (
    id uuid primary key,
    campanha_id uuid not null,
    espaco_id uuid not null,
    versao integer not null default 1 check (versao >= 1),
    estado varchar(24) not null default 'RASCUNHO'
        check (estado in ('RASCUNHO')),
    criado_por uuid not null
        references public.perfis_usuarios(id) on delete restrict,
    criado_em timestamptz not null,
    unique (campanha_id, versao),
    foreign key (campanha_id, espaco_id)
        references public.campanhas_mediad(id, espaco_id) on delete cascade
);

create index idx_campanhas_mediad_espaco
    on public.campanhas_mediad (espaco_id, atualizado_em desc);
create index idx_campanhas_mediad_equipe_usuario
    on public.campanhas_mediad_equipe (usuario_id, campanha_id);
create index idx_briefings_mediad_espaco
    on public.briefings_mediad (espaco_id, criado_em desc);

alter table public.campanhas_mediad enable row level security;
alter table public.campanhas_mediad_equipe enable row level security;
alter table public.briefings_mediad enable row level security;

create trigger trg_campanhas_mediad_espaco
before update on public.campanhas_mediad
for each row execute function public.validar_espaco_relacional();

create trigger trg_briefings_mediad_espaco
before update on public.briefings_mediad
for each row execute function public.validar_espaco_relacional();

create policy campanhas_mediad_consulta on public.campanhas_mediad
for select to authenticated
using (public.eh_membro_espaco(espaco_id));

create policy campanhas_mediad_escrita on public.campanhas_mediad
for all to authenticated
using (public.pode_editar_espaco(espaco_id))
with check (public.pode_editar_espaco(espaco_id));

create policy campanhas_mediad_equipe_consulta
on public.campanhas_mediad_equipe
for select to authenticated
using (
    exists (
        select 1
        from public.campanhas_mediad c
        where c.id = campanha_id
          and public.eh_membro_espaco(c.espaco_id)
    )
);

create policy campanhas_mediad_equipe_escrita
on public.campanhas_mediad_equipe
for all to authenticated
using (
    exists (
        select 1
        from public.campanhas_mediad c
        where c.id = campanha_id
          and public.pode_editar_espaco(c.espaco_id)
    )
)
with check (
    exists (
        select 1
        from public.campanhas_mediad c
        where c.id = campanha_id
          and public.pode_editar_espaco(c.espaco_id)
    )
);

create policy briefings_mediad_consulta on public.briefings_mediad
for select to authenticated
using (public.eh_membro_espaco(espaco_id));

create policy briefings_mediad_escrita on public.briefings_mediad
for all to authenticated
using (public.pode_editar_espaco(espaco_id))
with check (public.pode_editar_espaco(espaco_id));

create function public.abrir_campanha_mediad(
    p_campanha jsonb,
    p_espaco_id uuid
)
returns uuid
language plpgsql
security definer
set search_path = public
as $$
declare
    v_id uuid := (p_campanha ->> 'id')::uuid;
    v_criado_por uuid := (p_campanha ->> 'criado_por')::uuid;
    v_usuario_id uuid;
begin
    if auth.uid() is null or auth.uid() <> v_criado_por then
        raise exception 'Autoria da campanha não corresponde ao usuário autenticado';
    end if;
    if not public.pode_editar_espaco(p_espaco_id) then
        raise exception 'Usuário sem permissão para criar campanha no espaço';
    end if;
    if not exists (
        select 1
        from public.membros_espacos m
        join public.perfis_usuarios u on u.id = m.usuario_id and u.ativo
        where m.espaco_id = p_espaco_id
          and m.usuario_id =
              (p_campanha ->> 'planejador_responsavel_id')::uuid
    ) then
        raise exception 'Planejador responsável não é membro ativo do espaço';
    end if;

    insert into public.campanhas_mediad (
        id, espaco_id, codigo, nome, anunciante_id, marca_id,
        produto_servico_id, planejador_responsavel_id, observacao_inicial,
        campanha_derivada_de_id, snapshot_nome_anunciante,
        snapshot_nome_marca, snapshot_nome_produto_servico,
        snapshot_identificacao_planejador, criado_por, criado_em,
        atualizado_em, situacao, etapa_atual
    )
    values (
        v_id,
        p_espaco_id,
        p_campanha ->> 'codigo',
        p_campanha ->> 'nome',
        (p_campanha ->> 'anunciante_id')::uuid,
        (p_campanha ->> 'marca_id')::uuid,
        (p_campanha ->> 'produto_servico_id')::uuid,
        (p_campanha ->> 'planejador_responsavel_id')::uuid,
        p_campanha ->> 'observacao_inicial',
        (p_campanha ->> 'campanha_derivada_de_id')::uuid,
        p_campanha ->> 'snapshot_nome_anunciante',
        p_campanha ->> 'snapshot_nome_marca',
        p_campanha ->> 'snapshot_nome_produto_servico',
        p_campanha ->> 'snapshot_identificacao_planejador',
        v_criado_por,
        (p_campanha ->> 'criado_em')::timestamptz,
        (p_campanha ->> 'atualizado_em')::timestamptz,
        'RASCUNHO',
        'ABERTURA'
    );

    for v_usuario_id in
        select value::uuid
        from jsonb_array_elements_text(
            coalesce(p_campanha -> 'equipe_ids', '[]'::jsonb)
        )
    loop
        if not exists (
            select 1
            from public.membros_espacos m
            join public.perfis_usuarios u on u.id = m.usuario_id and u.ativo
            where m.espaco_id = p_espaco_id
              and m.usuario_id = v_usuario_id
        ) then
            raise exception 'Integrante da equipe não é membro ativo do espaço';
        end if;
        insert into public.campanhas_mediad_equipe (campanha_id, usuario_id)
        values (v_id, v_usuario_id);
    end loop;

    return v_id;
end;
$$;

create function public.iniciar_briefing_mediad(
    p_campanha_id uuid,
    p_espaco_id uuid,
    p_briefing_id uuid,
    p_usuario_id uuid,
    p_instante timestamptz
)
returns uuid
language plpgsql
security definer
set search_path = public
as $$
begin
    if auth.uid() is null or auth.uid() <> p_usuario_id then
        raise exception 'Autoria do briefing não corresponde ao usuário autenticado';
    end if;
    if not public.pode_editar_espaco(p_espaco_id) then
        raise exception 'Usuário sem permissão para iniciar briefing no espaço';
    end if;

    update public.campanhas_mediad
    set
        situacao = 'EM_ANDAMENTO',
        etapa_atual = 'BRIEFING',
        atualizado_em = p_instante
    where id = p_campanha_id
      and espaco_id = p_espaco_id
      and situacao = 'RASCUNHO'
      and etapa_atual = 'ABERTURA';

    if not found then
        raise exception 'Campanha ausente ou abertura já concluída';
    end if;

    insert into public.briefings_mediad (
        id, campanha_id, espaco_id, versao, estado, criado_por, criado_em
    )
    values (
        p_briefing_id, p_campanha_id, p_espaco_id, 1, 'RASCUNHO',
        p_usuario_id, p_instante
    );

    return p_briefing_id;
end;
$$;

revoke all on function public.abrir_campanha_mediad(jsonb, uuid) from public;
revoke all on function public.iniciar_briefing_mediad(
    uuid, uuid, uuid, uuid, timestamptz
) from public;
grant execute on function public.abrir_campanha_mediad(jsonb, uuid)
to authenticated;
grant execute on function public.iniciar_briefing_mediad(
    uuid, uuid, uuid, uuid, timestamptz
) to authenticated;


revoke all on table public.campanhas_mediad from anon;
revoke all on table public.campanhas_mediad_equipe from anon;
revoke all on table public.briefings_mediad from anon;
revoke insert, update, delete on table public.campanhas_mediad
from authenticated;
revoke insert, update, delete on table public.campanhas_mediad_equipe
from authenticated;
revoke insert, update, delete on table public.briefings_mediad
from authenticated;
grant select on table public.campanhas_mediad to authenticated;
grant select on table public.campanhas_mediad_equipe to authenticated;
grant select on table public.briefings_mediad to authenticated;
