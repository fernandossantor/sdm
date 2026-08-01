-- Conteúdo canônico, auditoria e versionamento transacional do Briefing.

alter table public.briefings_mediad
    drop constraint briefings_mediad_estado_check;
alter table public.briefings_mediad
    add constraint briefings_mediad_estado_check check (
        estado in (
            'RASCUNHO', 'EM_PREENCHIMENTO', 'EM_REVISAO',
            'CONCLUIDO', 'SUBSTITUIDO'
        )
    ),
    add column conteudo jsonb not null default '{}'::jsonb
        check (jsonb_typeof(conteudo) = 'object'),
    add column atualizado_por uuid
        references public.perfis_usuarios(id) on delete restrict,
    add column atualizado_em timestamptz,
    add column motivo_ultima_alteracao text;

create table public.briefings_mediad_revisoes (
    id bigint generated always as identity primary key,
    briefing_id uuid not null
        references public.briefings_mediad(id) on delete restrict,
    espaco_id uuid not null
        references public.espacos_trabalho(id) on delete restrict,
    versao integer not null,
    motivo text not null check (btrim(motivo) <> ''),
    alterado_por uuid not null
        references public.perfis_usuarios(id) on delete restrict,
    alterado_em timestamptz not null,
    valores_anteriores jsonb not null,
    valores_novos jsonb not null
);

alter table public.briefings_mediad_revisoes enable row level security;
create policy briefings_mediad_revisoes_consulta
on public.briefings_mediad_revisoes for select to authenticated
using (public.eh_membro_espaco(espaco_id));
revoke all on table public.briefings_mediad_revisoes from anon;
revoke insert, update, delete on table public.briefings_mediad_revisoes
from authenticated;
grant select on table public.briefings_mediad_revisoes to authenticated;

create function public.editar_briefing_mediad(
    p_briefing_id uuid, p_espaco_id uuid, p_conteudo jsonb,
    p_motivo text, p_usuario_id uuid, p_instante timestamptz
) returns uuid language plpgsql security definer set search_path = public as $$
declare v_antes public.briefings_mediad%rowtype;
begin
    if auth.uid() is null or auth.uid() <> p_usuario_id then
        raise exception 'Autoria da edição não corresponde ao usuário autenticado';
    end if;
    if not public.pode_editar_espaco(p_espaco_id) then
        raise exception 'Usuário sem permissão para editar briefing';
    end if;
    select * into v_antes from public.briefings_mediad
    where id = p_briefing_id and espaco_id = p_espaco_id for update;
    if not found then raise exception 'Briefing não encontrado'; end if;
    if v_antes.estado not in ('RASCUNHO', 'EM_PREENCHIMENTO') then
        raise exception 'Estado exige criação de nova versão';
    end if;
    if btrim(coalesce(p_motivo, '')) = '' then
        raise exception 'Motivo da alteração é obrigatório';
    end if;
    update public.briefings_mediad set
        conteudo = p_conteudo, estado = 'EM_PREENCHIMENTO',
        atualizado_por = p_usuario_id, atualizado_em = p_instante,
        motivo_ultima_alteracao = btrim(p_motivo)
    where id = p_briefing_id;
    insert into public.briefings_mediad_revisoes (
        briefing_id, espaco_id, versao, motivo, alterado_por, alterado_em,
        valores_anteriores, valores_novos
    ) values (
        p_briefing_id, p_espaco_id, v_antes.versao, btrim(p_motivo),
        p_usuario_id, p_instante, to_jsonb(v_antes),
        (select to_jsonb(b) from public.briefings_mediad b where b.id=p_briefing_id)
    );
    return p_briefing_id;
end; $$;

create function public.versionar_briefing_mediad(
    p_briefing_origem_id uuid, p_novo_briefing_id uuid, p_espaco_id uuid,
    p_conteudo jsonb, p_motivo text, p_usuario_id uuid, p_instante timestamptz
) returns uuid language plpgsql security definer set search_path = public as $$
declare v_origem public.briefings_mediad%rowtype;
begin
    if auth.uid() is null or auth.uid() <> p_usuario_id then
        raise exception 'Autoria da versão não corresponde ao usuário autenticado';
    end if;
    if not public.pode_editar_espaco(p_espaco_id) then
        raise exception 'Usuário sem permissão para versionar briefing';
    end if;
    if btrim(coalesce(p_motivo, '')) = '' then
        raise exception 'Motivo da nova versão é obrigatório';
    end if;
    select * into v_origem from public.briefings_mediad
    where id=p_briefing_origem_id and espaco_id=p_espaco_id for update;
    if not found then raise exception 'Briefing de origem não encontrado'; end if;
    if exists (
        select 1 from public.briefings_mediad
        where campanha_id=v_origem.campanha_id and estado <> 'SUBSTITUIDO'
          and id <> v_origem.id
    ) then raise exception 'Já existe versão ativa posterior'; end if;
    update public.briefings_mediad set estado='SUBSTITUIDO',
        atualizado_por=p_usuario_id, atualizado_em=p_instante,
        motivo_ultima_alteracao=btrim(p_motivo)
    where id=v_origem.id;
    insert into public.briefings_mediad (
        id, campanha_id, espaco_id, versao, estado, criado_por, criado_em,
        conteudo, atualizado_por, atualizado_em, motivo_ultima_alteracao
    ) values (
        p_novo_briefing_id, v_origem.campanha_id, p_espaco_id,
        v_origem.versao + 1, 'EM_PREENCHIMENTO', p_usuario_id, p_instante,
        p_conteudo, p_usuario_id, p_instante, btrim(p_motivo)
    );
    return p_novo_briefing_id;
end; $$;

revoke all on function public.editar_briefing_mediad(
    uuid, uuid, jsonb, text, uuid, timestamptz
) from public;
revoke all on function public.versionar_briefing_mediad(
    uuid, uuid, uuid, jsonb, text, uuid, timestamptz
) from public;
grant execute on function public.editar_briefing_mediad(
    uuid, uuid, jsonb, text, uuid, timestamptz
) to authenticated;
grant execute on function public.versionar_briefing_mediad(
    uuid, uuid, uuid, jsonb, text, uuid, timestamptz
) to authenticated;
