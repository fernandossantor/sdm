-- Correções rastreáveis da Campanha e identificação pessoal do planejador.

alter table public.campanhas_mediad
    add column nome_anunciante_atual varchar(240),
    add column nome_marca_atual varchar(240),
    add column nome_produto_servico_atual varchar(240),
    add column identificacao_planejador_atual varchar(240);

update public.campanhas_mediad
set nome_anunciante_atual = snapshot_nome_anunciante,
    nome_marca_atual = snapshot_nome_marca,
    nome_produto_servico_atual = snapshot_nome_produto_servico,
    identificacao_planejador_atual = snapshot_identificacao_planejador;

alter table public.campanhas_mediad
    alter column nome_anunciante_atual set not null,
    alter column identificacao_planejador_atual set not null;

-- Os vínculos atuais evoluem; os snapshots de criação permanecem imutáveis.
do $$
declare
    v_constraint record;
begin
    for v_constraint in
        select conname
        from pg_constraint
        where conrelid = 'public.campanhas_mediad'::regclass
          and contype = 'c'
          and (
              pg_get_constraintdef(oid) like '%snapshot_nome_marca%'
              or pg_get_constraintdef(oid) like '%snapshot_nome_produto_servico%'
          )
    loop
        execute format(
            'alter table public.campanhas_mediad drop constraint %I',
            v_constraint.conname
        );
    end loop;
end;
$$;

alter table public.campanhas_mediad
    add constraint campanhas_mediad_marca_atual_coerente
        check ((marca_id is null) = (nome_marca_atual is null)),
    add constraint campanhas_mediad_produto_atual_coerente
        check (
            (produto_servico_id is null)
            = (nome_produto_servico_atual is null)
        );

create function public.preencher_contexto_atual_campanha_mediad()
returns trigger
language plpgsql
set search_path = public
as $$
begin
    new.nome_anunciante_atual := coalesce(
        new.nome_anunciante_atual, new.snapshot_nome_anunciante
    );
    new.nome_marca_atual := coalesce(
        new.nome_marca_atual, new.snapshot_nome_marca
    );
    new.nome_produto_servico_atual := coalesce(
        new.nome_produto_servico_atual, new.snapshot_nome_produto_servico
    );
    new.identificacao_planejador_atual := coalesce(
        new.identificacao_planejador_atual,
        new.snapshot_identificacao_planejador
    );
    return new;
end;
$$;

create trigger trg_preencher_contexto_atual_campanha_mediad
before insert on public.campanhas_mediad
for each row execute function public.preencher_contexto_atual_campanha_mediad();

create table public.campanhas_mediad_revisoes (
    id bigint generated always as identity primary key,
    campanha_id uuid not null references public.campanhas_mediad(id)
        on delete cascade,
    espaco_id uuid not null references public.espacos_trabalho(id)
        on delete restrict,
    motivo text not null check (btrim(motivo) <> ''),
    antes jsonb not null,
    depois jsonb not null,
    alterado_por uuid not null references public.perfis_usuarios(id)
        on delete restrict,
    alterado_em timestamptz not null,
    foreign key (campanha_id, espaco_id)
        references public.campanhas_mediad(id, espaco_id) on delete cascade
);

create index idx_campanhas_mediad_revisoes_campanha
    on public.campanhas_mediad_revisoes (campanha_id, alterado_em desc);

alter table public.campanhas_mediad_revisoes enable row level security;

create policy campanhas_mediad_revisoes_consulta
on public.campanhas_mediad_revisoes for select to authenticated
using (public.eh_membro_espaco(espaco_id));

revoke insert, update, delete on public.campanhas_mediad_revisoes
from authenticated;
grant select on public.campanhas_mediad_revisoes to authenticated;

create function public.atualizar_campanha_mediad(
    p_campanha_id uuid,
    p_espaco_id uuid,
    p_alteracoes jsonb,
    p_motivo text,
    p_usuario_id uuid,
    p_instante timestamptz
)
returns uuid
language plpgsql
security definer
set search_path = public
as $$
declare
    v_antes public.campanhas_mediad%rowtype;
    v_depois public.campanhas_mediad%rowtype;
    v_planejador_id uuid :=
        (p_alteracoes ->> 'planejador_responsavel_id')::uuid;
begin
    if auth.uid() is null or auth.uid() <> p_usuario_id then
        raise exception 'Autoria da correção não corresponde ao usuário autenticado';
    end if;
    if not public.pode_editar_espaco(p_espaco_id) then
        raise exception 'Usuário sem permissão para editar campanha no espaço';
    end if;
    if not (
        public.usuario_eh_membro_ativo_espaco(v_planejador_id, p_espaco_id)
        or (v_planejador_id = auth.uid() and public.eh_admin())
    ) then
        raise exception 'Planejador responsável não possui acesso válido ao espaço';
    end if;
    if btrim(coalesce(p_motivo, '')) = '' then
        raise exception 'Motivo da correção é obrigatório';
    end if;

    select * into v_antes from public.campanhas_mediad
    where id = p_campanha_id and espaco_id = p_espaco_id
    for update;

    if not found then
        raise exception 'Campanha não encontrada';
    end if;
    if v_antes.situacao in ('CONCLUIDA', 'CANCELADA', 'ARQUIVADA') then
        raise exception 'Campanha não pode ser corrigida neste estado';
    end if;

    update public.campanhas_mediad set
        nome = btrim(p_alteracoes ->> 'nome'),
        anunciante_id = (p_alteracoes ->> 'anunciante_id')::uuid,
        marca_id = (p_alteracoes ->> 'marca_id')::uuid,
        produto_servico_id =
            (p_alteracoes ->> 'produto_servico_id')::uuid,
        planejador_responsavel_id = v_planejador_id,
        observacao_inicial = nullif(
            btrim(p_alteracoes ->> 'observacao_inicial'), ''),
        nome_anunciante_atual = btrim(
            p_alteracoes ->> 'nome_anunciante_atual'),
        nome_marca_atual = nullif(
            btrim(p_alteracoes ->> 'nome_marca_atual'), ''),
        nome_produto_servico_atual = nullif(
            btrim(p_alteracoes ->> 'nome_produto_servico_atual'), ''),
        identificacao_planejador_atual = btrim(
            p_alteracoes ->> 'identificacao_planejador_atual'),
        atualizado_em = p_instante
    where id = p_campanha_id and espaco_id = p_espaco_id
    returning * into v_depois;

    insert into public.campanhas_mediad_revisoes (
        campanha_id, espaco_id, motivo, antes, depois,
        alterado_por, alterado_em
    ) values (
        p_campanha_id, p_espaco_id, btrim(p_motivo),
        to_jsonb(v_antes), to_jsonb(v_depois), p_usuario_id, p_instante
    );

    return p_campanha_id;
end;
$$;

revoke all on function public.atualizar_campanha_mediad(
    uuid, uuid, jsonb, text, uuid, timestamptz
) from public;
grant execute on function public.atualizar_campanha_mediad(
    uuid, uuid, jsonb, text, uuid, timestamptz
) to authenticated;

-- Administrador autenticado pode assumir pessoalmente a responsabilidade.
create or replace function public.usuario_eh_membro_ativo_espaco(
    p_usuario_id uuid,
    p_espaco_id uuid
)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select exists (
        select 1
        from public.perfis_usuarios p
        where p.id = p_usuario_id
          and p.ativo
          and (
              (p_usuario_id = auth.uid() and public.eh_admin())
              or exists (
                  select 1
                  from public.espacos_trabalho e
                  where e.id = p_espaco_id
                    and e.ativo
                    and e.proprietario_id = p_usuario_id
              )
              or exists (
                  select 1
                  from public.membros_espacos m
                  where m.espaco_id = p_espaco_id
                    and m.usuario_id = p_usuario_id
              )
          )
    );
$$;
