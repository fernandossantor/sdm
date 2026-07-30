-- A abertura da campanha deve aceitar o proprietário ativo do espaço como
-- planejador, mesmo nos espaços legados sem linha em membros_espacos.

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
              exists (
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

create or replace function public.abrir_campanha_mediad(
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
    if not public.usuario_eh_membro_ativo_espaco(
        (p_campanha ->> 'planejador_responsavel_id')::uuid,
        p_espaco_id
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
        v_id, p_espaco_id, p_campanha ->> 'codigo', p_campanha ->> 'nome',
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
        'RASCUNHO', 'ABERTURA'
    );

    for v_usuario_id in
        select value::uuid
        from jsonb_array_elements_text(
            coalesce(p_campanha -> 'equipe_ids', '[]'::jsonb)
        )
    loop
        if not public.usuario_eh_membro_ativo_espaco(
            v_usuario_id, p_espaco_id
        ) then
            raise exception 'Integrante da equipe não é membro ativo do espaço';
        end if;
        insert into public.campanhas_mediad_equipe (campanha_id, usuario_id)
        values (v_id, v_usuario_id);
    end loop;

    return v_id;
end;
$$;

revoke all on function public.usuario_eh_membro_ativo_espaco(uuid, uuid)
from public;
