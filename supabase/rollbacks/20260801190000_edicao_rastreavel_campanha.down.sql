drop function if exists public.atualizar_campanha_mediad(
    uuid, uuid, jsonb, text, uuid, timestamptz
);
drop table if exists public.campanhas_mediad_revisoes;
drop trigger if exists trg_preencher_contexto_atual_campanha_mediad
    on public.campanhas_mediad;
drop function if exists public.preencher_contexto_atual_campanha_mediad();
alter table public.campanhas_mediad
    drop constraint if exists campanhas_mediad_marca_atual_coerente,
    drop constraint if exists campanhas_mediad_produto_atual_coerente;
alter table public.campanhas_mediad
    drop column if exists nome_anunciante_atual,
    drop column if exists nome_marca_atual,
    drop column if exists nome_produto_servico_atual,
    drop column if exists identificacao_planejador_atual;
alter table public.campanhas_mediad
    add check ((marca_id is null) = (snapshot_nome_marca is null)),
    add check (
        (produto_servico_id is null)
        = (snapshot_nome_produto_servico is null)
    );

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
