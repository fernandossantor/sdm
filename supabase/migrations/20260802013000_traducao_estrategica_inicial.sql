-- Primeiro contrato estratégico versionado, vinculado a Briefing concluído.

create table public.traducoes_estrategicas_mediad (
    id uuid primary key,
    campanha_id uuid not null,
    briefing_id uuid not null references public.briefings_mediad(id) on delete restrict,
    espaco_id uuid not null references public.espacos_trabalho(id) on delete restrict,
    versao integer not null default 1 check (versao >= 1),
    estado varchar(20) not null check (
        estado in ('DEFINITIVO','PROVISORIO','PARCIAL','INSUFICIENTE','SUPERADO')
    ),
    resultado jsonb not null check (jsonb_typeof(resultado)='object'),
    criado_por uuid not null references public.perfis_usuarios(id) on delete restrict,
    criado_em timestamptz not null,
    unique (briefing_id, versao),
    foreign key (campanha_id, espaco_id)
        references public.campanhas_mediad(id, espaco_id) on delete restrict
);
alter table public.traducoes_estrategicas_mediad enable row level security;
create policy traducoes_estrategicas_mediad_consulta
on public.traducoes_estrategicas_mediad for select to authenticated
using (public.eh_membro_espaco(espaco_id));
revoke all on table public.traducoes_estrategicas_mediad from anon;
revoke insert, update, delete on table public.traducoes_estrategicas_mediad
from authenticated;
grant select on table public.traducoes_estrategicas_mediad to authenticated;

create function public.criar_traducao_estrategica_mediad(
    p_id uuid, p_briefing_id uuid, p_espaco_id uuid, p_resultado jsonb,
    p_usuario_id uuid, p_instante timestamptz
) returns uuid language plpgsql security definer set search_path=public as $$
declare v_briefing public.briefings_mediad%rowtype;
begin
    if auth.uid() is null or auth.uid() <> p_usuario_id then
        raise exception 'Autoria não corresponde ao usuário autenticado';
    end if;
    if not public.pode_editar_espaco(p_espaco_id) then
        raise exception 'Usuário sem permissão para criar tradução';
    end if;
    select * into v_briefing from public.briefings_mediad
    where id=p_briefing_id and espaco_id=p_espaco_id and estado='CONCLUIDO';
    if not found then raise exception 'Briefing concluído não encontrado'; end if;
    insert into public.traducoes_estrategicas_mediad (
        id, campanha_id, briefing_id, espaco_id, versao, estado,
        resultado, criado_por, criado_em
    ) values (
        p_id, v_briefing.campanha_id, p_briefing_id, p_espaco_id,
        (p_resultado->>'versao')::integer, p_resultado->>'estado',
        p_resultado, p_usuario_id, p_instante
    );
    return p_id;
end; $$;
revoke all on function public.criar_traducao_estrategica_mediad(
    uuid, uuid, uuid, jsonb, uuid, timestamptz
) from public;
grant execute on function public.criar_traducao_estrategica_mediad(
    uuid, uuid, uuid, jsonb, uuid, timestamptz
) to authenticated;
